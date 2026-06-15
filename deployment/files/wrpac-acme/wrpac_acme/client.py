"""End-to-end Python ACME client speaking CS-06 (wrp-id + registrar-api-01).

Simulates a WRP/EBW issuing itself a WRPAC.

Usage:
    python -m wrpac_acme.client \
        --directory http://mw-vm-ca01.lab:9080/acme-eudi-wrpac/directory \
        --rp-list http://mw-vm-ca01.lab:9000 \
        --wrp-id NLKVK.12345678 \
        --legal-name "ACME Test Organisation B.V." \
        --org-id VATNL-000000000B01 \
        --country NL \
        --friendly-name "ACME RP Smoke Test"
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import time
from typing import Any, Dict, Optional

import httpx
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from jwcrypto import jwk, jws


def b64u(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def sign(key: jwk.JWK, protected: Dict[str, Any], payload: bytes) -> Dict[str, str]:
    token = jws.JWS(payload)
    token.add_signature(key, alg=protected.get("alg", "RS256"),
                        protected=json.dumps(protected))
    return json.loads(token.serialize())


class ACMEClient:
    def __init__(self, directory_url: str, rp_list_url: str) -> None:
        self.directory_url = directory_url
        self.rp_list_url = rp_list_url.rstrip("/")
        self.http = httpx.Client(timeout=15.0, verify=False)
        self.directory: Dict[str, Any] = {}
        self.nonce: Optional[str] = None
        self.account_key = jwk.JWK.generate(kty="RSA", size=3072)
        self.account_url: Optional[str] = None

    # ----- low-level helpers -----

    def fetch_directory(self) -> None:
        r = self.http.get(self.directory_url)
        r.raise_for_status()
        self.directory = r.json()
        print("[client] directory:", json.dumps(self.directory, indent=2))

    def fetch_nonce(self) -> None:
        r = self.http.head(self.directory["newNonce"])
        r.raise_for_status()
        self.nonce = r.headers["Replay-Nonce"]

    def _absorb_nonce(self, r: httpx.Response) -> None:
        n = r.headers.get("Replay-Nonce")
        if n:
            self.nonce = n

    def _post(self, url: str, *, payload: Optional[Dict[str, Any]] = None,
              use_jwk: bool = False, extra_protected: Optional[Dict[str, Any]] = None) -> httpx.Response:
        if self.nonce is None:
            self.fetch_nonce()
        protected: Dict[str, Any] = {"alg": "RS256", "nonce": self.nonce, "url": url}
        if use_jwk:
            protected["jwk"] = json.loads(self.account_key.export_public())
        else:
            assert self.account_url is not None
            protected["kid"] = self.account_url
        if extra_protected:
            protected.update(extra_protected)

        payload_bytes = b"" if payload is None else json.dumps(payload).encode("utf-8")
        body = sign(self.account_key, protected, payload_bytes)
        r = self.http.post(url, json=body,
                           headers={"Content-Type": "application/jose+json"})
        self._absorb_nonce(r)
        return r

    # ----- ACME flow -----

    def new_account_with_eab(self, contact: list[str], wrp_id: str,
                             legal_name: str) -> None:
        # Stub EAB carrying the (simulated) EBWOID identity the RA "verified".
        # In production the RA issues EAB credentials bound to the EBWOID; here
        # the EBWOID {id, name} travels in the EAB protected header so the
        # façade can enforce the EBWOID↔wrp-id match (CS-06 §5.4, §7.2 #9).
        eab_protected = b64u(json.dumps({"alg": "HS256", "kid": f"eab-{wrp_id}",
                                          "url": self.directory["newAccount"],
                                          "ebwoid": {"id": wrp_id,
                                                     "name": legal_name}}).encode())
        eab_payload = b64u(self.account_key.export_public().encode())
        eab_signature = b64u(b"STUB-NOT-AN-HMAC")  # CS-06 §5.4 MVP path
        payload = {
            "termsOfServiceAgreed": True,
            "contact": contact,
            "externalAccountBinding": {
                "protected": eab_protected,
                "payload": eab_payload,
                "signature": eab_signature,
            },
        }
        r = self._post(self.directory["newAccount"], payload=payload, use_jwk=True)
        if r.status_code not in (200, 201):
            raise RuntimeError(f"newAccount failed: {r.status_code} {r.text}")
        self.account_url = r.headers["Location"]
        print("[client] account:", self.account_url)

    def new_order(self, wrp_id: str) -> Dict[str, Any]:
        r = self._post(self.directory["newOrder"],
                       payload={"identifiers": [{"type": "wrp-id", "value": wrp_id}]})
        if r.status_code not in (200, 201):
            raise RuntimeError(f"newOrder failed: {r.status_code} {r.text}")
        order = r.json()
        order["_url"] = r.headers["Location"]
        print("[client] order:", json.dumps(order, indent=2))
        return order

    def get_authz(self, authz_url: str) -> Dict[str, Any]:
        r = self._post(authz_url, payload=None)  # POST-as-GET
        r.raise_for_status()
        return r.json()

    def post_challenge(self, chall_url: str) -> Dict[str, Any]:
        r = self._post(chall_url, payload={})
        if r.status_code not in (200, 202):
            raise RuntimeError(f"challenge POST failed: {r.status_code} {r.text}")
        return r.json()

    def finalize(self, finalize_url: str, csr_der: bytes) -> Dict[str, Any]:
        r = self._post(finalize_url, payload={"csr": b64u(csr_der)})
        if r.status_code not in (200, 201):
            raise RuntimeError(f"finalize failed: {r.status_code} {r.text}")
        return r.json()

    def get_order(self, order_url: str) -> Dict[str, Any]:
        r = self._post(order_url, payload=None)
        r.raise_for_status()
        return r.json()

    def download_cert(self, cert_url: str) -> str:
        r = self._post(cert_url, payload=None)
        r.raise_for_status()
        return r.text

    # ----- RP List helpers (out-of-band, not part of ACME) -----

    def put_acme_challenge(self, wrp_id: str, key_auth: str) -> None:
        r = self.http.put(f"{self.rp_list_url}/rp-list/{wrp_id}/acme-challenge",
                          json={"key_authorization": key_auth})
        r.raise_for_status()


def build_csr(legal_name: str, org_id: str, country: str,
              friendly_name: str) -> tuple[bytes, rsa.RSAPrivateKey]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(x509.ObjectIdentifier("2.5.4.97"), org_id),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, legal_name),
        x509.NameAttribute(NameOID.COMMON_NAME, friendly_name),
    ])
    csr = x509.CertificateSigningRequestBuilder() \
        .subject_name(subject) \
        .add_extension(x509.SubjectAlternativeName([x509.DNSName("rp.test.lab")]),
                       critical=False) \
        .sign(key, hashes.SHA256())
    return csr.public_bytes(serialization.Encoding.DER), key


def jwk_thumbprint(key: jwk.JWK) -> str:
    return key.thumbprint()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", required=True)
    ap.add_argument("--rp-list", required=True)
    ap.add_argument("--wrp-id", required=True)
    ap.add_argument("--legal-name", required=True)
    ap.add_argument("--org-id", required=True)
    ap.add_argument("--country", default="NL")
    ap.add_argument("--friendly-name", required=True)
    ap.add_argument("--out-cert", default="/tmp/wrpac-issued.pem")
    args = ap.parse_args()

    c = ACMEClient(args.directory, args.rp_list)
    c.fetch_directory()
    c.fetch_nonce()
    c.new_account_with_eab([f"mailto:smoke@{args.wrp_id}"], args.wrp_id,
                           args.legal_name)
    order = c.new_order(args.wrp_id)

    # Walk authorizations
    for authz_url in order["authorizations"]:
        authz = c.get_authz(authz_url)
        print("[client] authz:", json.dumps(authz, indent=2))
        chall = next(ch for ch in authz["challenges"] if ch["type"] == "registrar-api-01")
        key_auth = f"{chall['token']}.{jwk_thumbprint(c.account_key)}"
        print(f"[client] placing key-auth in RP List for {args.wrp_id}")
        c.put_acme_challenge(args.wrp_id, key_auth)
        print("[client] signalling readiness on challenge URL")
        c.post_challenge(chall["url"])
        # Poll authz until valid (façade transitions synchronously, so one poll suffices)
        for _ in range(10):
            authz = c.get_authz(authz_url)
            if authz["status"] == "valid":
                break
            if authz["status"] == "invalid":
                print("[client] authz invalid:", authz, file=sys.stderr)
                return 1
            time.sleep(1)

    csr_der, _key = build_csr(args.legal_name, args.org_id, args.country, args.friendly_name)
    order2 = c.finalize(order["finalize"], csr_der)
    print("[client] order after finalize:", json.dumps(order2, indent=2))

    if "certificate" not in order2:
        # Poll until certificate URL appears
        for _ in range(10):
            order2 = c.get_order(order["_url"])
            if order2.get("certificate"):
                break
            time.sleep(1)
        else:
            print("[client] no certificate URL appeared", file=sys.stderr)
            return 1

    pem = c.download_cert(order2["certificate"])
    with open(args.out_cert, "w") as f:
        f.write(pem)
    print(f"[client] issued WRPAC written to {args.out_cert}")
    print("---- PEM ----")
    print(pem)
    return 0


if __name__ == "__main__":
    sys.exit(main())
