"""Mock Registrar / RP List service per CS-06 §7.8.

Stand-in for the national Registrar's API in the WE BUILD pilot.

Endpoints:
    GET    /rp-list/{wrp_id}                — return the RP entry
    PUT    /rp-list/{wrp_id}                — admin: create / update entry
    PUT    /rp-list/{wrp_id}/acme-challenge — WRP places its key-authorization
    DELETE /rp-list/{wrp_id}                — admin
    GET    /rp-list                         — list all WRPs

In production these would be queried per EC TS5 / TS6.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .storage import Store

app = FastAPI(title="WE BUILD Mock RP List", version="0.1.0")

DB_PATH = os.getenv("WRPAC_RP_LIST_DB_PATH", "/var/lib/wrpac-acme/rp_list.sqlite3")


class ACMEChallenge(BaseModel):
    """CS-06 §7.8 allows both a single key-authorization string and a
    multi-instance dict keyed by `instanceId`. We accept both."""

    default: Optional[str] = None
    instances: Dict[str, str] = Field(default_factory=dict)


class RPListEntry(BaseModel):
    wrp_id: str
    legal_name: str
    organization_identifier: str
    country: str = "NL"
    status: str = "active"
    acme_challenge: Union[str, ACMEChallenge, None] = None


def _entry_to_dict(e: RPListEntry) -> dict:
    return e.model_dump(mode="json")


def _entry_from_dict(d: dict) -> RPListEntry:
    return RPListEntry.model_validate(d)


_store: Store[RPListEntry] = Store(DB_PATH, "entries", _entry_to_dict, _entry_from_dict)


def _seed() -> None:
    """Pre-populate one test WRP so the smoke client has something to enrol.

    Only seeds if the WRP isn't already in the persistent store — re-running
    after a restart preserves the entry (including any acme-challenge values
    a client has placed)."""
    seed = os.getenv("WRPAC_SEED_WRP_ID", "NLKVK.12345678")
    if seed in _store:
        return
    _store[seed] = RPListEntry(
        wrp_id=seed,
        legal_name=os.getenv("WRPAC_SEED_LEGAL_NAME", "ACME Test Organisation B.V."),
        organization_identifier=os.getenv("WRPAC_SEED_ORG_ID", "VATNL-000000000B01"),
        country=os.getenv("WRPAC_SEED_COUNTRY", "NL"),
        status="active",
        acme_challenge=None,
    )


_seed()


@app.get("/rp-list")
def list_all() -> Dict[str, Any]:
    return {"items": [e.model_dump() for e in _store.values()]}


@app.get("/rp-list/{wrp_id}")
def get_entry(wrp_id: str) -> RPListEntry:
    entry = _store.get(wrp_id)
    if entry is None:
        raise HTTPException(404, "WRP not found")
    return entry


@app.put("/rp-list/{wrp_id}")
def put_entry(wrp_id: str, entry: RPListEntry) -> RPListEntry:
    if entry.wrp_id != wrp_id:
        raise HTTPException(400, "wrp_id in path/body mismatch")
    _store[wrp_id] = entry
    return entry


class ChallengePayload(BaseModel):
    key_authorization: str
    instance_id: Optional[str] = None


@app.put("/rp-list/{wrp_id}/acme-challenge")
def put_challenge(wrp_id: str, payload: ChallengePayload) -> Dict[str, Any]:
    entry = _store.get(wrp_id)
    if entry is None:
        raise HTTPException(404, "WRP not found")
    if entry.status != "active":
        raise HTTPException(403, "WRP not active")
    if payload.instance_id:
        # Multi-instance form
        if not isinstance(entry.acme_challenge, ACMEChallenge):
            entry.acme_challenge = ACMEChallenge()
        entry.acme_challenge.instances[payload.instance_id] = payload.key_authorization
    else:
        # Single-instance shorthand (CS-06 §7.8)
        entry.acme_challenge = payload.key_authorization
    _store[wrp_id] = entry
    return {"wrp_id": wrp_id, "acme_challenge": entry.acme_challenge}


@app.delete("/rp-list/{wrp_id}")
def delete_entry(wrp_id: str) -> Dict[str, str]:
    if wrp_id not in _store:
        raise HTTPException(404, "WRP not found")
    del _store[wrp_id]
    return {"deleted": wrp_id}
