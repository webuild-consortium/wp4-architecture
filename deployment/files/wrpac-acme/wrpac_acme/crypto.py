"""JWS / JWK helpers used by the ACME façade.

Just enough crypto to:
    - parse and verify a flattened JWS request body (RFC 8555 §6.2)
    - compute the JWK thumbprint per RFC 7638
    - derive the key-authorization per RFC 8555 §8.1

For Phase 3 simplicity we DO NOT verify nonces here — the façade just issues
fresh ones and never checks. Replay protection is out of scope for the
interop demo.
"""
from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Optional

from jwcrypto import jwk, jws


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64u_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


@dataclass
class ParsedJWS:
    protected: dict
    payload: bytes
    signature_valid: bool
    jwk_obj: jwk.JWK  # The verifying key
    payload_json: Optional[dict] = None


def parse_and_verify(
    body: dict,
    *,
    account_jwk: Optional[jwk.JWK] = None,
) -> ParsedJWS:
    """Parse a flattened JWS request body and verify the signature.

    If `account_jwk` is given, that's the key the JWS must verify against
    (post-newAccount requests use `kid`). Otherwise the JWS protected
    header MUST carry an embedded `jwk` (newAccount, revokeCert by cert key).
    """
    if not all(k in body for k in ("protected", "payload", "signature")):
        raise ValueError("not a flattened JWS")

    protected_raw = b64u_decode(body["protected"])
    protected = json.loads(protected_raw)

    if account_jwk is None:
        if "jwk" not in protected:
            raise ValueError("no jwk in protected header and no account key supplied")
        verify_key = jwk.JWK(**protected["jwk"])
    else:
        verify_key = account_jwk

    token = jws.JWS()
    token.deserialize(json.dumps(body))
    token.verify(verify_key)

    payload = token.payload  # bytes
    payload_json: Optional[dict] = None
    if payload:
        try:
            payload_json = json.loads(payload)
        except json.JSONDecodeError:
            payload_json = None

    return ParsedJWS(
        protected=protected,
        payload=payload,
        signature_valid=True,
        jwk_obj=verify_key,
        payload_json=payload_json,
    )


def jwk_thumbprint(key: jwk.JWK) -> str:
    """RFC 7638 JWK thumbprint, returned as base64url-no-pad."""
    return key.thumbprint()


def key_authorization(token: str, key: jwk.JWK) -> str:
    """RFC 8555 §8.1: token || '.' || base64url(Thumbprint(accountKey))."""
    return f"{token}.{jwk_thumbprint(key)}"
