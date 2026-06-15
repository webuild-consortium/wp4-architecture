"""Negative tests for the CS-06 façade.

Exercises CS-06 §7.2 MUST clauses by trying things the façade must reject.

Run:
    python -m wrpac_acme.negative_tests \
        --directory https://rpca.lab.cleverbase.io/acme-eudi-wrpac/directory \
        --rp-list   https://rpca.lab.cleverbase.io
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from typing import Tuple

import httpx
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from jwcrypto import jwk, jws


def b64u(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def sign(key: jwk.JWK, protected: dict, payload: bytes) -> dict:
    tok = jws.JWS(payload)
    tok.add_signature(key, alg=protected.get("alg", "RS256"),
                      protected=json.dumps(protected))
    return json.loads(tok.serialize())


def pass_(name: str) -> None:
    print(f"  PASS  {name}")


def fail(name: str, why: str) -> None:
    print(f"  FAIL  {name} — {why}")


class Runner:
    def __init__(self, directory_url: str, rp_list_url: str) -> None:
        self.directory_url = directory_url
        self.rp_list_url = rp_list_url.rstrip("/")
        self.http = httpx.Client(timeout=15.0)
        self.dir: dict = {}
        self.fails = 0
        self.passes = 0

    def record(self, ok: bool, name: str, why: str = "") -> None:
        if ok:
            self.passes += 1
            pass_(name)
        else:
            self.fails += 1
            fail(name, why)

    def setup(self) -> None:
        self.dir = self.http.get(self.directory_url).json()

    def fresh_nonce(self) -> str:
        return self.http.head(self.dir["newNonce"]).headers["Replay-Nonce"]

    def fresh_account(self, ebwoid_id: str = "NLKVK.12345678",
                      ebwoid_name: str = "ACME Test Organisation B.V.",
                      ) -> Tuple[jwk.JWK, str]:
        """Successfully create a new account and return (key, account_url).

        The EAB carries a (simulated) EBWOID {id, name}; the defaults match the
        seeded WRP so the account passes the §7.2 #9 EBWOID↔wrp-id check."""
        key = jwk.JWK.generate(kty="RSA", size=2048)
        nonce = self.fresh_nonce()
        eab_protected = b64u(json.dumps({"alg": "HS256", "kid": "eab-test",
                                          "url": self.dir["newAccount"],
                                          "ebwoid": {"id": ebwoid_id,
                                                     "name": ebwoid_name}}).encode())
        eab_payload = b64u(key.export_public().encode())
        eab_sig = b64u(b"STUB")
        payload = {
            "termsOfServiceAgreed": True,
            "contact": ["mailto:neg@test"],
            "externalAccountBinding": {
                "protected": eab_protected,
                "payload": eab_payload,
                "signature": eab_sig,
            },
        }
        protected = {"alg": "RS256", "nonce": nonce, "url": self.dir["newAccount"],
                     "jwk": json.loads(key.export_public())}
        r = self.http.post(self.dir["newAccount"],
                           json=sign(key, protected,
                                     json.dumps(payload).encode()),
                           headers={"Content-Type": "application/jose+json"})
        return key, r.headers["Location"]

    def post(self, url: str, key: jwk.JWK, kid: str,
             payload: dict | None) -> httpx.Response:
        nonce = self.fresh_nonce()
        protected = {"alg": "RS256", "nonce": nonce, "url": url, "kid": kid}
        body = sign(key, protected,
                    b"" if payload is None else json.dumps(payload).encode())
        return self.http.post(url, json=body,
                              headers={"Content-Type": "application/jose+json"})

    # ---- tests ----

    def t_newaccount_without_eab(self) -> None:
        name = "newAccount without externalAccountBinding rejected (§7.2 #2)"
        key = jwk.JWK.generate(kty="RSA", size=2048)
        nonce = self.fresh_nonce()
        protected = {"alg": "RS256", "nonce": nonce, "url": self.dir["newAccount"],
                     "jwk": json.loads(key.export_public())}
        payload = {"termsOfServiceAgreed": True, "contact": ["mailto:x@y"]}
        r = self.http.post(self.dir["newAccount"],
                           json=sign(key, protected,
                                     json.dumps(payload).encode()),
                           headers={"Content-Type": "application/jose+json"})
        self.record(r.status_code == 400, name,
                    f"expected 400, got {r.status_code}: {r.text[:200]}")

    def t_neworder_bad_identifier_type(self) -> None:
        name = "newOrder rejects non-wrp-id identifier (§7.2 #3)"
        key, acct = self.fresh_account()
        r = self.post(self.dir["newOrder"], key, acct,
                      {"identifiers": [{"type": "dns", "value": "example.com"}]})
        self.record(r.status_code == 400, name,
                    f"expected 400, got {r.status_code}: {r.text[:200]}")

    def t_challenge_unknown_wrp(self) -> None:
        name = "registrar-api-01 fails for wrp-id not in RP List (§7.2 #4,5)"
        key, acct = self.fresh_account()
        r = self.post(self.dir["newOrder"], key, acct,
                      {"identifiers": [{"type": "wrp-id",
                                         "value": "NLKVK.UNKNOWN-9999"}]})
        if r.status_code not in (200, 201):
            self.record(False, name, f"newOrder failed unexpectedly: {r.status_code}")
            return
        order = r.json()
        authz = self.post(order["authorizations"][0], key, acct, None).json()
        chall_url = next(c["url"] for c in authz["challenges"]
                         if c["type"] == "registrar-api-01")
        # Skip placing key-auth — server will fetch from RP List and 404
        r = self.post(chall_url, key, acct, {})
        self.record(r.status_code == 403, name,
                    f"expected 403, got {r.status_code}: {r.text[:200]}")

    def t_challenge_wrong_keyauth(self) -> None:
        name = "registrar-api-01 fails when RP List acme-challenge mismatches (§7.2 #4,5)"
        key, acct = self.fresh_account()
        r = self.post(self.dir["newOrder"], key, acct,
                      {"identifiers": [{"type": "wrp-id",
                                         "value": "NLKVK.12345678"}]})
        order = r.json()
        authz = self.post(order["authorizations"][0], key, acct, None).json()
        chall = next(c for c in authz["challenges"]
                     if c["type"] == "registrar-api-01")
        # Put a deliberately WRONG key-auth in the RP List
        wrong = chall["token"] + ".DELIBERATELY-WRONG-THUMBPRINT"
        self.http.put(f"{self.rp_list_url}/rp-list/NLKVK.12345678/acme-challenge",
                      json={"key_authorization": wrong})
        r = self.post(chall["url"], key, acct, {})
        self.record(r.status_code == 403, name,
                    f"expected 403, got {r.status_code}: {r.text[:200]}")

    def t_challenge_ebwoid_mismatch(self) -> None:
        name = "registrar-api-01 fails when EBWOID.id != ordered wrp-id (§7.2 #9)"
        # Account's EBWOID is for a DIFFERENT organisation than the WRP ordered.
        key, acct = self.fresh_account(ebwoid_id="NLKVK.99999999",
                                       ebwoid_name="Someone Else B.V.")
        r = self.post(self.dir["newOrder"], key, acct,
                      {"identifiers": [{"type": "wrp-id",
                                         "value": "NLKVK.12345678"}]})
        if r.status_code not in (200, 201):
            self.record(False, name, f"newOrder failed unexpectedly: {r.status_code}")
            return
        order = r.json()
        authz = self.post(order["authorizations"][0], key, acct, None).json()
        chall = next(c for c in authz["challenges"]
                     if c["type"] == "registrar-api-01")
        # Place the CORRECT key-auth, so the only failing check is the EBWOID match.
        key_auth = f"{chall['token']}.{key.thumbprint()}"
        self.http.put(f"{self.rp_list_url}/rp-list/NLKVK.12345678/acme-challenge",
                      json={"key_authorization": key_auth})
        r = self.post(chall["url"], key, acct, {})
        self.record(r.status_code == 403, name,
                    f"expected 403, got {r.status_code}: {r.text[:200]}")

    def t_finalize_subject_mismatch(self) -> None:
        name = "finalize rejects CSR whose Subject doesn't match RP List entry"
        key, acct = self.fresh_account()
        # newOrder
        r = self.post(self.dir["newOrder"], key, acct,
                      {"identifiers": [{"type": "wrp-id",
                                         "value": "NLKVK.12345678"}]})
        order = r.json()
        order_url = r.headers["Location"]
        # complete challenge with CORRECT key-auth
        authz = self.post(order["authorizations"][0], key, acct, None).json()
        chall = next(c for c in authz["challenges"]
                     if c["type"] == "registrar-api-01")
        key_auth = f"{chall['token']}.{key.thumbprint()}"
        self.http.put(f"{self.rp_list_url}/rp-list/NLKVK.12345678/acme-challenge",
                      json={"key_authorization": key_auth})
        self.post(chall["url"], key, acct, {})
        # Build CSR with WRONG O / organizationIdentifier
        cert_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
        wrong_subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "DE"),
            x509.NameAttribute(x509.ObjectIdentifier("2.5.4.97"),
                                "VAT-WRONG-IDENTIFIER"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Wrong Org GmbH"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Wrong friendly name"),
        ])
        csr = (x509.CertificateSigningRequestBuilder()
               .subject_name(wrong_subject)
               .sign(cert_key, hashes.SHA256()))
        csr_der = csr.public_bytes(serialization.Encoding.DER)
        r = self.post(order["finalize"], key, acct, {"csr": b64u(csr_der)})
        self.record(r.status_code == 400, name,
                    f"expected 400, got {r.status_code}: {r.text[:200]}")

    def t_revoke_unimplemented(self) -> None:
        name = "revokeCert returns 501 (stub — known gap)"
        key, acct = self.fresh_account()
        r = self.post(self.dir["revokeCert"], key, acct, {"certificate": "x"})
        self.record(r.status_code == 501, name,
                    f"expected 501, got {r.status_code}: {r.text[:200]}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", required=True)
    ap.add_argument("--rp-list", required=True)
    args = ap.parse_args()
    r = Runner(args.directory, args.rp_list)
    r.setup()
    print("CS-06 negative-test battery")
    print("=" * 60)
    for t in (
        r.t_newaccount_without_eab,
        r.t_neworder_bad_identifier_type,
        r.t_challenge_unknown_wrp,
        r.t_challenge_wrong_keyauth,
        r.t_challenge_ebwoid_mismatch,
        r.t_finalize_subject_mismatch,
        r.t_revoke_unimplemented,
    ):
        try:
            t()
        except Exception as exc:
            r.fails += 1
            fail(t.__name__, f"exception: {exc}")
    print("=" * 60)
    print(f"  {r.passes} passed, {r.fails} failed")
    return 0 if r.fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
