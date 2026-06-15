"""WE BUILD CS-06 ACME façade — minimal interop-test implementation.

What's here
-----------
* /acme-eudi-wrpac/directory with `wrp-id` and `registrar-api-01` in meta
* JWS-signed requests per RFC 8555 §6
* newAccount with EAB carrying a (simulated) EBWOID {id, name} claim
  (CS-06 §5.4 MVP path — EAB blob required, HMAC not verified)
* newOrder accepting `{type:"wrp-id", value: <wrp_id>}`
* registrar-api-01 challenge: fetches RP List, compares key-authorization,
  and enforces the EBWOID↔wrp-id match (CS-06 §7.2 #9: EBWOID.id == wrp-id,
  EBWOID.name == RP List legal name)
* finalize: verifies CSR Subject DN matches the RP List entry, forwards CSR to
  Dogtag (`pki ca-cert-request-submit --profile wrpacCert`), returns issued PEM

What's deliberately out of scope (see deployment/README.md)
----------------------------------------------------------
* HTTPS, nonce replay protection, real EAB HMAC, keyChange, multi-instance,
  registrationCertificate co-issuance, CT logging
"""
from __future__ import annotations

import json
import os
import secrets
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import httpx
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from jwcrypto import jwk

from .crypto import key_authorization, parse_and_verify
from .dogtag import submit_csr
from .storage import Store

ROOT = "/acme-eudi-wrpac"
RP_LIST_URL = os.getenv("WRPAC_RP_LIST_URL", "http://localhost:9000")
DB_PATH = os.getenv("WRPAC_DB_PATH", "/var/lib/wrpac-acme/facade.sqlite3")
# Optional fallback if the request doesn't carry usable Host/X-Forwarded-*.
BASE_URL_FALLBACK = os.getenv("WRPAC_BASE_URL", "http://mw-vm-ca01.lab:9080").rstrip("/")

app = FastAPI(title="WE BUILD CS-06 ACME façade", version="0.1.0")


# ---------- Persistent state ----------

@dataclass
class Account:
    id: str
    jwk: jwk.JWK
    contact: List[str] = field(default_factory=list)
    status: str = "valid"
    # Organisational identity from the EBWOID the RA verified (CS-06 §5.4).
    # Matched against the order's wrp-id at challenge time (§7.2 #9).
    ebwoid_id: Optional[str] = None
    ebwoid_name: Optional[str] = None


@dataclass
class Challenge:
    id: str
    type: str  # "registrar-api-01"
    token: str
    status: str = "pending"
    authz_id: str = ""


@dataclass
class Authorization:
    id: str
    order_id: str
    identifier_type: str
    identifier_value: str
    status: str = "pending"
    challenge_ids: List[str] = field(default_factory=list)


@dataclass
class Order:
    id: str
    account_id: str
    identifiers: List[Dict[str, str]]
    authz_ids: List[str] = field(default_factory=list)
    status: str = "pending"
    cert_id: Optional[str] = None


# Serialization helpers ---------------------------------------------------

def _account_to_dict(a: Account) -> dict:
    return {
        "id": a.id,
        "jwk": json.loads(a.jwk.export(private_key=False)),
        "contact": list(a.contact),
        "status": a.status,
        "ebwoid_id": a.ebwoid_id,
        "ebwoid_name": a.ebwoid_name,
    }


def _account_from_dict(d: dict) -> Account:
    return Account(
        id=d["id"],
        jwk=jwk.JWK(**d["jwk"]),
        contact=list(d.get("contact", [])),
        status=d.get("status", "valid"),
        ebwoid_id=d.get("ebwoid_id"),
        ebwoid_name=d.get("ebwoid_name"),
    )


def _challenge_to_dict(c: Challenge) -> dict:
    return {"id": c.id, "type": c.type, "token": c.token,
            "status": c.status, "authz_id": c.authz_id}


def _challenge_from_dict(d: dict) -> Challenge:
    return Challenge(**d)


def _authz_to_dict(a: Authorization) -> dict:
    return {"id": a.id, "order_id": a.order_id,
            "identifier_type": a.identifier_type,
            "identifier_value": a.identifier_value,
            "status": a.status,
            "challenge_ids": list(a.challenge_ids)}


def _authz_from_dict(d: dict) -> Authorization:
    return Authorization(**d)


def _order_to_dict(o: Order) -> dict:
    return {"id": o.id, "account_id": o.account_id,
            "identifiers": list(o.identifiers),
            "authz_ids": list(o.authz_ids),
            "status": o.status, "cert_id": o.cert_id}


def _order_from_dict(d: dict) -> Order:
    return Order(**d)


def _cert_to_dict(pem: str) -> dict:
    return {"pem": pem}


def _cert_from_dict(d: dict) -> str:
    return d["pem"]


_accounts: Store[Account] = Store(DB_PATH, "accounts", _account_to_dict, _account_from_dict)
_orders: Store[Order] = Store(DB_PATH, "orders", _order_to_dict, _order_from_dict)
_authzs: Store[Authorization] = Store(DB_PATH, "authzs", _authz_to_dict, _authz_from_dict)
_challenges: Store[Challenge] = Store(DB_PATH, "challenges", _challenge_to_dict, _challenge_from_dict)
_certs: Store[str] = Store(DB_PATH, "certs", _cert_to_dict, _cert_from_dict)


# ---------- URL helpers ----------

def base_url(request: Optional[Request]) -> str:
    """Derive the public-facing base URL from the request.

    Honors X-Forwarded-Proto / Host when uvicorn is started with
    --proxy-headers; otherwise reads scheme+host directly. Falls back to
    BASE_URL_FALLBACK when no request is available (e.g. internal helpers
    that don't have a request handle yet)."""
    if request is None:
        return BASE_URL_FALLBACK
    return f"{request.url.scheme}://{request.url.netloc}".rstrip("/")


def u(request: Optional[Request], *path: str) -> str:
    return f"{base_url(request)}{ROOT}/{'/'.join(path)}"


# ---------- Middleware: stamp every response with Replay-Nonce ----------

@app.middleware("http")
async def stamp_nonce(request: Request, call_next):
    response = await call_next(request)
    # Every ACME response should carry a fresh nonce (RFC 8555 §6.5).
    response.headers["Replay-Nonce"] = secrets.token_urlsafe(24)
    return response


# ---------- Directory & nonce ----------

@app.get(ROOT + "/directory")
def directory(request: Request) -> JSONResponse:
    return JSONResponse({
        "newNonce": u(request, "new-nonce"),
        "newAccount": u(request, "new-account"),
        "newOrder": u(request, "new-order"),
        "revokeCert": u(request, "revoke-cert"),
        "meta": {
            "termsOfService": f"{base_url(request)}/tos",
            "externalAccountRequired": True,
            "supportedIdentifierTypes": ["wrp-id"],
            "supportedChallengeTypes": ["registrar-api-01"],
            "rprcCoIssuanceSupported": False,
            "multiInstanceIssuanceSupported": False,
        },
    })


@app.api_route(ROOT + "/new-nonce", methods=["GET", "HEAD"])
def new_nonce() -> Response:
    # The middleware adds the Replay-Nonce header for us.
    # RFC 8555 §7.2: HEAD returns 200, GET returns 204.
    return Response(status_code=204)


# ---------- JWS helpers ----------

async def _read_jws(request: Request) -> dict:
    raw = await request.body()
    try:
        return __import__("json").loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(400, "request body must be a flattened JWS")


def _verify_with_account(body: dict) -> tuple[Account, dict, bytes]:
    """Verify a JWS where `kid` references an existing account URL."""
    import base64
    import json as _json

    if "protected" not in body:
        raise HTTPException(400, "missing protected header")
    pad = "=" * (-len(body["protected"]) % 4)
    protected = _json.loads(base64.urlsafe_b64decode(body["protected"] + pad))
    kid = protected.get("kid")
    if not kid:
        raise HTTPException(400, "kid required for this endpoint")
    # kid is the account URL: .../acct/<id>
    account_id = kid.rstrip("/").rsplit("/", 1)[-1]
    account = _accounts.get(account_id)
    if account is None:
        raise HTTPException(401, "unknown account")
    parsed = parse_and_verify(body, account_jwk=account.jwk)
    return account, parsed.protected, parsed.payload


# ---------- newAccount ----------

def _eab_ebwoid(eab: dict) -> dict:
    """Extract the (simulated) EBWOID {id, name} claim from the EAB protected
    header. In production the RA resolves this from the EAB Key ID after
    verifying the EBWOID via OID4VP; in this MVP the claim travels in the EAB
    so the façade can enforce the EBWOID↔wrp-id match (CS-06 §5.4, §7.2 #9)."""
    import base64
    import json as _json
    try:
        prot = eab["protected"]
        pad = "=" * (-len(prot) % 4)
        header = _json.loads(base64.urlsafe_b64decode(prot + pad))
    except Exception:
        return {}
    ebwoid = header.get("ebwoid")
    return ebwoid if isinstance(ebwoid, dict) else {}


@app.post(ROOT + "/new-account")
async def new_account(request: Request) -> JSONResponse:
    body = await _read_jws(request)
    parsed = parse_and_verify(body, account_jwk=None)
    payload = parsed.payload_json or {}

    # CS-06 §5.4: EAB required. In production the RA issues these credentials
    # bound to the organisation's verified EBWOID; here the EAB carries the
    # (simulated) EBWOID identity {id, name} in its protected header so the
    # façade can enforce the EBWOID↔wrp-id match at challenge time (§7.2 #9).
    eab = payload.get("externalAccountBinding")
    if not eab or not all(k in eab for k in ("protected", "payload", "signature")):
        raise HTTPException(400, "externalAccountBinding required (CS-06 §5.4)")
    ebwoid = _eab_ebwoid(eab)
    if not ebwoid.get("id") or not ebwoid.get("name"):
        raise HTTPException(
            400,
            "externalAccountBinding must carry an EBWOID {id, name} claim (CS-06 §5.4)",
        )

    account_id = uuid.uuid4().hex[:16]
    _accounts[account_id] = Account(
        id=account_id,
        jwk=parsed.jwk_obj,
        contact=payload.get("contact", []),
        ebwoid_id=ebwoid["id"],
        ebwoid_name=ebwoid["name"],
    )
    resp = JSONResponse(
        {
            "status": "valid",
            "contact": _accounts[account_id].contact,
            "orders": u(request, "acct", account_id, "orders"),
        },
        status_code=201,
    )
    resp.headers["Location"] = u(request, "acct", account_id)
    return resp


# ---------- newOrder ----------

@app.post(ROOT + "/new-order")
async def new_order(request: Request) -> JSONResponse:
    body = await _read_jws(request)
    account, _, _payload = _verify_with_account(body)
    payload_json = __import__("json").loads(_payload.decode("utf-8")) if _payload else {}

    identifiers = payload_json.get("identifiers") or []
    if not identifiers or any(i.get("type") != "wrp-id" for i in identifiers):
        raise HTTPException(400, "identifiers must contain at least one wrp-id (CS-06 §5.2)")

    order_id = uuid.uuid4().hex[:16]
    authz_ids: List[str] = []
    for ident in identifiers:
        authz_id = uuid.uuid4().hex[:16]
        chall_id = uuid.uuid4().hex[:16]
        token = secrets.token_urlsafe(24)
        _challenges[chall_id] = Challenge(
            id=chall_id, type="registrar-api-01", token=token, authz_id=authz_id,
        )
        _authzs[authz_id] = Authorization(
            id=authz_id,
            order_id=order_id,
            identifier_type=ident["type"],
            identifier_value=ident["value"],
            challenge_ids=[chall_id],
        )
        authz_ids.append(authz_id)

    _orders[order_id] = Order(
        id=order_id,
        account_id=account.id,
        identifiers=identifiers,
        authz_ids=authz_ids,
    )
    resp = JSONResponse(_order_view(request, order_id), status_code=201)
    resp.headers["Location"] = u(request, "order", order_id)
    return resp


def _order_view(request: Request, order_id: str) -> dict:
    o = _orders[order_id]
    view = {
        "status": o.status,
        "identifiers": o.identifiers,
        "authorizations": [u(request, "authz", a) for a in o.authz_ids],
        "finalize": u(request, "order", order_id, "finalize"),
    }
    if o.cert_id:
        view["certificate"] = u(request, "cert", o.cert_id)
    return view


# ---------- Order / Authz / Challenge GET (POST-as-GET) ----------

@app.post(ROOT + "/order/{order_id}")
async def order(order_id: str, request: Request) -> JSONResponse:
    body = await _read_jws(request)
    _verify_with_account(body)
    if order_id not in _orders:
        raise HTTPException(404, "order not found")
    return JSONResponse(_order_view(request, order_id))


@app.post(ROOT + "/authz/{authz_id}")
async def authz(authz_id: str, request: Request) -> JSONResponse:
    body = await _read_jws(request)
    _verify_with_account(body)
    if authz_id not in _authzs:
        raise HTTPException(404, "authz not found")
    return JSONResponse(_authz_view(request, authz_id))


def _authz_view(request: Request, authz_id: str) -> dict:
    a = _authzs[authz_id]
    return {
        "status": a.status,
        "identifier": {"type": a.identifier_type, "value": a.identifier_value},
        "challenges": [_challenge_view(request, c) for c in a.challenge_ids],
    }


def _challenge_view(request: Request, chall_id: str) -> dict:
    c = _challenges[chall_id]
    return {
        "type": c.type,
        "url": u(request, "chall", c.id),
        "status": c.status,
        "token": c.token,
    }


# ---------- registrar-api-01 challenge validation ----------

@app.post(ROOT + "/chall/{chall_id}")
async def challenge(chall_id: str, request: Request) -> JSONResponse:
    body = await _read_jws(request)
    account, _, payload = _verify_with_account(body)
    if chall_id not in _challenges:
        raise HTTPException(404, "challenge not found")
    c = _challenges[chall_id]
    a = _authzs[c.authz_id]

    # Empty payload "{}" signals readiness (RFC 8555 §7.5.1).
    if payload and payload != b"{}":
        raise HTTPException(400, "challenge POST payload must be empty object")

    # Compute expected key-authorization
    expected = key_authorization(c.token, account.jwk)

    # Fetch the RP List entry for this WRP
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"{RP_LIST_URL}/rp-list/{a.identifier_value}")
    if r.status_code != 200:
        c.status = "invalid"
        a.status = "invalid"
        _challenges.save(c.id); _authzs.save(a.id)
        raise HTTPException(403, f"WRP not in RP List: {a.identifier_value}")
    entry = r.json()
    if entry.get("status") != "active":
        c.status = "invalid"
        a.status = "invalid"
        _challenges.save(c.id); _authzs.save(a.id)
        raise HTTPException(403, "WRP not active")

    # CS-06 §7.2 #9: the EBWOID bound to the account MUST correspond to the WRP
    # being ordered — EBWOID.id == wrp-id and EBWOID.name == the RP List entry's
    # WRP legal name. This is the direct, testable identity binding that replaces
    # the looser POA-based check.
    if (account.ebwoid_id != a.identifier_value
            or account.ebwoid_name != entry.get("legal_name")):
        c.status = "invalid"
        a.status = "invalid"
        _challenges.save(c.id); _authzs.save(a.id)
        raise HTTPException(
            403,
            "EBWOID does not correspond to the WRP: "
            f"ebwoid.id={account.ebwoid_id!r} wrp-id={a.identifier_value!r}, "
            f"ebwoid.name={account.ebwoid_name!r} legal_name={entry.get('legal_name')!r}",
        )

    # acme-challenge may be a bare string (single-instance shorthand) or a
    # structured object per CS-06 §7.8. We only support single-instance.
    chal = entry.get("acme_challenge")
    if isinstance(chal, dict):
        chal = chal.get("default")
    if chal != expected:
        c.status = "invalid"
        a.status = "invalid"
        _challenges.save(c.id); _authzs.save(a.id)
        raise HTTPException(
            403,
            "RP List acme-challenge does not match expected key-authorization",
        )

    c.status = "valid"
    a.status = "valid"
    _challenges.save(c.id); _authzs.save(a.id)

    # Move order toward `ready` if all authz are valid
    o = _orders[a.order_id]
    if all(_authzs[az].status == "valid" for az in o.authz_ids):
        o.status = "ready"
        _orders.save(o.id)

    return JSONResponse(_challenge_view(request, chall_id))


# ---------- finalize ----------

@app.post(ROOT + "/order/{order_id}/finalize")
async def finalize(order_id: str, request: Request) -> JSONResponse:
    body = await _read_jws(request)
    account, _, payload = _verify_with_account(body)
    if order_id not in _orders:
        raise HTTPException(404, "order not found")
    o = _orders[order_id]
    if o.account_id != account.id:
        raise HTTPException(403, "order belongs to another account")
    if o.status != "ready":
        raise HTTPException(403, f"order not ready (status={o.status})")

    payload_json = __import__("json").loads(payload.decode("utf-8")) if payload else {}
    csr_b64u = payload_json.get("csr")
    if not csr_b64u:
        raise HTTPException(400, "csr field required")

    import base64
    pad = "=" * (-len(csr_b64u) % 4)
    csr_der = base64.urlsafe_b64decode(csr_b64u + pad)
    csr = x509.load_der_x509_csr(csr_der)

    # Cross-check CSR Subject matches the RP List entry for the order's WRP
    wrp_id = o.identifiers[0]["value"]
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"{RP_LIST_URL}/rp-list/{wrp_id}")
    if r.status_code != 200:
        raise HTTPException(403, "WRP not in RP List at finalize time")
    entry = r.json()

    subject_attrs = {a.oid.dotted_string: a.value for a in csr.subject}
    issues = []
    if subject_attrs.get("2.5.4.97") != entry["organization_identifier"]:
        issues.append(
            f"organizationIdentifier mismatch: csr={subject_attrs.get('2.5.4.97')!r} "
            f"rp-list={entry['organization_identifier']!r}"
        )
    if subject_attrs.get("2.5.4.10") != entry["legal_name"]:
        issues.append(
            f"O mismatch: csr={subject_attrs.get('2.5.4.10')!r} "
            f"rp-list={entry['legal_name']!r}"
        )
    if subject_attrs.get("2.5.4.6") != entry["country"]:
        issues.append(
            f"C mismatch: csr={subject_attrs.get('2.5.4.6')!r} "
            f"rp-list={entry['country']!r}"
        )
    if issues:
        raise HTTPException(
            400,
            "CSR Subject does not match RP List entry: " + "; ".join(issues),
        )

    o.status = "processing"
    _orders.save(o.id)

    # Forward to Dogtag
    csr_pem = csr.public_bytes(Encoding.PEM)
    try:
        cert_pem = await submit_csr(csr_pem)
    except Exception as exc:
        o.status = "invalid"
        _orders.save(o.id)
        raise HTTPException(500, f"CA issuance failed: {exc}")

    cert_id = uuid.uuid4().hex[:16]
    _certs[cert_id] = cert_pem
    o.cert_id = cert_id
    o.status = "valid"
    _orders.save(o.id)
    return JSONResponse(_order_view(request, order_id))


# ---------- cert download ----------

@app.post(ROOT + "/cert/{cert_id}")
async def cert(cert_id: str, request: Request) -> Response:
    body = await _read_jws(request)
    _verify_with_account(body)
    if cert_id not in _certs:
        raise HTTPException(404, "cert not found")
    return PlainTextResponse(
        _certs[cert_id],
        media_type="application/pem-certificate-chain",
    )


@app.post(ROOT + "/revoke-cert")
async def revoke_cert(request: Request) -> Response:
    raise HTTPException(501, "revocation not implemented in Phase 3 MVP")


@app.get("/tos")
def tos() -> PlainTextResponse:
    return PlainTextResponse("WE BUILD interoperability testing only.")
