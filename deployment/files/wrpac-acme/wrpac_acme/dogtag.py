"""Thin wrapper around the `pki` CLI to submit a CSR to Dogtag.

The façade reuses the NSS DB set up by Phase 2's direct-enrolment smoke test
(/root/wrpac-smoke/nssdb) which already contains the caadmin client cert and
the trusted CA signing cert.
"""
from __future__ import annotations

import asyncio
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass


@dataclass
class DogtagConfig:
    nss_dir: str = os.getenv("WRPAC_NSS_DIR", "/root/wrpac-smoke/nssdb")
    nss_password: str = os.getenv("WRPAC_NSS_PASSWORD", "Secret.123")
    admin_nickname: str = os.getenv("WRPAC_ADMIN_NICKNAME", "PKI Administrator for lab")
    ca_url: str = os.getenv("WRPAC_CA_URL", "https://mw-vm-ca01.lab:8443")
    profile_id: str = os.getenv("WRPAC_PROFILE_ID", "wrpacCert")


_CFG = DogtagConfig()


def _pki_base() -> list[str]:
    return [
        "pki",
        "-d", _CFG.nss_dir,
        "-c", _CFG.nss_password,
        "-n", _CFG.admin_nickname,
        "-U", _CFG.ca_url,
    ]


_CERT_ID_RE = re.compile(r"Certificate ID:\s*(\S+)")


def _sync_submit_csr(csr_pem: bytes) -> str:
    """Submit a PEM-encoded CSR via the pki CLI and return the issued cert (PEM)."""
    with tempfile.TemporaryDirectory() as tmp:
        csr_path = os.path.join(tmp, "req.csr")
        cert_path = os.path.join(tmp, "cert.pem")
        with open(csr_path, "wb") as f:
            f.write(csr_pem)

        submit = subprocess.run(
            _pki_base() + [
                "ca-cert-request-submit",
                "--profile", _CFG.profile_id,
                "--csr-file", csr_path,
            ],
            capture_output=True,
            text=True,
        )
        if submit.returncode != 0:
            raise RuntimeError(
                f"pki ca-cert-request-submit failed: rc={submit.returncode} "
                f"stderr={submit.stderr.strip()} stdout={submit.stdout.strip()}"
            )
        if "Request Status: complete" not in submit.stdout:
            raise RuntimeError(
                f"cert request not complete: {submit.stdout.strip()}"
            )
        m = _CERT_ID_RE.search(submit.stdout)
        if not m:
            raise RuntimeError(f"no Certificate ID in output: {submit.stdout.strip()}")
        cert_id = m.group(1)

        show = subprocess.run(
            _pki_base() + [
                "ca-cert-show", cert_id,
                "--output", cert_path,
            ],
            capture_output=True,
            text=True,
        )
        if show.returncode != 0:
            raise RuntimeError(
                f"pki ca-cert-show failed: rc={show.returncode} stderr={show.stderr.strip()}"
            )
        with open(cert_path, "rb") as f:
            return f.read().decode("ascii")


async def submit_csr(csr_pem: bytes) -> str:
    """Async wrapper — runs the blocking pki CLI in a thread."""
    return await asyncio.to_thread(_sync_submit_csr, csr_pem)
