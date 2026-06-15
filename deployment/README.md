# WE BUILD RPAC CA — Ansible deployment

> **Scope.** This directory contains the **deployment artefacts** for a Dogtag PKI CA
> targeted at `mw-vm-ca01.lab` for WE BUILD interoperability testing of
> [CS-06](../conformance-specs/cs-06-issuance-of-relying-party-access-and-registration-certificates.md).
>
> It is **not** governance documentation. It is also **not yet** a CS-06-conformant
> deployment — see "Remaining gaps" below.

## Phases delivered

**Phase 1** — stock RFC 8555 ACME endpoint backed by Dogtag PKI on `mw-vm-ca01.lab`,
verified end-to-end with `acme.sh` (http-01 challenge, issues from the stock
`acmeServerCert` profile: RSA-only, 90-day).

**Phase 2** — custom `wrpacCert` profile that matches CS-06 §7.4 (1-year validity,
RSA-3072+/ECDSA P-256/P-384, SHA-256+, Subject DN constraint requiring
`organizationIdentifier=`, WRPAC policy OID, SAN). Verified by direct enrolment
of a CSR with a real WRPAC Subject DN (`O=` legal name + `organizationIdentifier=`
+ `C=` + `CN=` friendly name) using the `pki` CLI as a CA agent.

**Phase 3** — minimal CS-06 ACME façade (Python/FastAPI) + mock Registrar (RP List
service) sitting in front of the Dogtag CA. Implements `wrp-id` identifier
(CS-06 §5.2), `registrar-api-01` challenge (§5.3) with the EBWOID↔wrp-id match
(§7.2 #9: `EBWOID.id == wrp-id`, `EBWOID.name == RP List legal name`), EBW-EAB
**stub** (§5.4 MVP path — EAB carries a simulated EBWOID `{id, name}` claim but
the HMAC is not verified), and synchronous finalize → CSR-Subject vs RP-List
cross-check → `pki ca-cert-request-submit --profile wrpacCert`. Verified
end-to-end by a Python ACME client (`acme.sh` can't speak `wrp-id`).

## Layout

```
deployment/
├── ansible.cfg                  base config (inventory, ssh)
├── inventory.yml                single host: mw-vm-ca01.lab as cbadmin
├── group_vars/all.yml           CA FQDN, passwords (test-only), DS suffix,
│                                WRPAC test identity, placeholder policy OIDs
├── site.yml                     imports the playbooks in order
├── files/
│   ├── wrpacCert.cfg.j2         Dogtag profile template (CS-06 §7.4)
│   └── wrpac-acme/              Phase 3 Python project (façade + RP List + client)
│       ├── pyproject.toml
│       └── wrpac_acme/
│           ├── rp_list.py       Mock Registrar / RP List service (port 9000)
│           ├── facade.py        ACME façade (port 9080)
│           ├── crypto.py        JWS / JWK / key-authorization helpers
│           ├── dogtag.py        Submits CSRs to Dogtag via `pki` CLI
│           └── client.py        End-to-end Python ACME client (CS-06 §6 flow)
└── playbooks/
    ├── 00-prereqs.yml           hostname, EPEL, firewalld, time sync, repos
    ├── 10-dogtag-ca.yml         389-DS instance + pkispawn -s CA
    ├── 20-dogtag-acme.yml       pki-acme package + acme-create/acme-deploy
    ├── 21-acme-persistence.yml  switch Dogtag ACME backend from in-memory to 389-DS
    ├── 30-wrpac-profile.yml     install + register wrpacCert profile
    ├── 31-wrpac-smoke-direct.yml direct CSR enrolment with WRPAC Subject DN
    ├── 40-wrpac-facade.yml      sync façade + RP List, systemd units, e2e smoke
    └── 99-smoke-test.yml        GET /acme/directory + acme.sh test issuance

tests/
├── README.md                   how to run; var reference
├── test_all.yml                master — runs all six in order
├── test_01_directory.yml       directories + RP List sanity                 [URL-flexible]
├── test_02_phase1_acme.yml     acme.sh stock ACME http-01 issuance          [local only]
├── test_03_phase2_direct.yml   pki CLI direct enrolment with wrpacCert      [local only]
├── test_04_phase3_happy.yml    Python ACME client CS-06 §6 happy path       [URL-flexible]
├── test_05_phase3_negative.yml CS-06 §7.2 MUST negative-test battery        [URL-flexible]
├── test_06_cert_profile.yml    Issue a fresh WRPAC + assert every §7.4 attribute [URL-flexible]
├── test_07_persistence.yml     Dogtag ACME state survives pki-tomcatd restart [local only]
└── test_08_facade_persistence.yml CS-06 façade + RP List survive service restart [local only]
```

## Running the test suite

```sh
# Against the local deployment (default)
ansible-playbook tests/test_all.yml

# Against the public deployment
ansible-playbook tests/test_all.yml \
    -e test_acme_directory=https://rpca.lab.cleverbase.io/acme-eudi-wrpac/directory \
    -e test_rp_list=https://rpca.lab.cleverbase.io \
    -e test_acme_stock_directory=https://rpca.lab.cleverbase.io/acme/directory
```

Tests 02 and 03 always run on the CA host (they need box-local state: acme.sh's
cache, the pki NSS DB). Tests 01, 04, 05, 06 run from the control machine, so
they can target either internal or public URLs.

## Run

From this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml

# Connectivity check
ansible -i inventory.yml -m ping all

# Full deploy
ansible-playbook site.yml

# Or step-by-step
ansible-playbook playbooks/00-prereqs.yml
ansible-playbook playbooks/10-dogtag-ca.yml
ansible-playbook playbooks/20-dogtag-acme.yml
ansible-playbook playbooks/99-smoke-test.yml
```

## Passwords

Test-only passwords live in [group_vars/all.yml](group_vars/all.yml) (`Secret.123`).
Before any non-throwaway use, replace them with an `ansible-vault` encrypted file.

## Remaining gaps before this is CS-06 conformant

### Implemented (Phase 1–3)

- `wrp-id` identifier type (§5.2) — façade-level
- `registrar-api-01` challenge (§5.3) — façade fetches RP List, verifies `acme-challenge` against expected key-authorization
- WRPAC certificate profile (§7.4) — Dogtag `wrpacCert`, 1-year, RSA-3072+/ECDSA P-256/P-384, policy OID, server-built Subject DN
- Mock Registrar / RP List (§7.8) — single-instance shorthand form
- EAB **structure** at newAccount (§5.4) — blob accepted, carries a simulated EBWOID `{id, name}`; HMAC not verified
- EBWOID↔wrp-id match (§7.2 #9) — challenge validation enforces `EBWOID.id == wrp-id` and `EBWOID.name == RP List legal name`

### Still missing

| Gap | Spec ref | Notes |
|---|---|---|
| HTTPS on the façade | §7.1 #2 | Façade currently binds plain HTTP on :9080. Put nginx in front, or have uvicorn terminate TLS with a Dogtag-issued cert. |
| Real EAB HMAC verification | §5.4 | Currently a stub. Needs an EAB-credentials store (Key ID → HMAC key) populated by the RA, and JWS HMAC verify on newAccount. The EBWOID `{id, name}` the EAB carries is likewise trusted as-presented, not cryptographically bound. |
| Nonce replay protection | §7.1 #4 | Façade issues fresh nonces but does not verify incoming ones. |
| `keyChange`, real `revokeCert` | §5.1, §7.6 | Stubs / unimplemented. |
| Multi-instance `instanceId` | §5.2, §8.3 | Single-instance only today. |
| `registrationCertificate` URL co-issuance | §5.1, §8.5 | The order object never carries this URL. |
| CT logging + SCTs | §7.5 | Neither Dogtag nor the façade log to CT today. |
| ~~Persistent state (Phase 3 façade)~~ | — | ✓ Done. Phase 3 façade state (accounts/orders/authz/challenges/certs) + mock RP List persist in SQLite under `/var/lib/wrpac-acme/`. See [`wrpac_acme/storage.py`](files/wrpac-acme/wrpac_acme/storage.py). Dogtag's own ACME state persists in 389-DS — see [21-acme-persistence.yml](playbooks/21-acme-persistence.yml). |
| Verified WRPAC policy OIDs | §7.4 #2 | Values in `group_vars/all.yml` are **placeholders** in the ETSI test arc. Replace with `NCP-l-eudiwrp` / `NCP-n-eudiwrp` from ETSI TS 119 411-8 v1.1.1. |
| Full OID4VP-based EBW authentication (MVP+) | §5.4, §6.2 | The RA + EBW flow that provisions EAB credentials is out of scope. |

`99-smoke-test.yml` (Phase 1 stock-ACME smoke test against Dogtag's built-in
responder) is still wired up alongside the Phase 3 façade. They live on
different ports (8443 vs 9080) and don't interfere.

## Tear-down

The CA can be removed with `pkidestroy -s CA -i pki-tomcat` and the 389-DS
instance with `dsctl pki remove --do-it`. A tear-down playbook is not provided —
re-image the VM if you want a clean slate.
