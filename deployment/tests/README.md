# Tests

This directory holds the test suite for the CS-06 CA deployment. Each test is a
standalone ansible playbook that runs on the CA host (`mw-vm-ca01.lab`) and can
target either the local or the public ACME endpoints via a single variable.

## Test matrix

| Test | What it covers | Targetable URL |
|---|---|---|
| `test_01_directory.yml` | Both ACME directories + RP List service respond and advertise the expected URLs/metadata | local **or** public |
| `test_02_phase1_acme.yml` | Stock RFC 8555 ACME issuance via `acme.sh` http-01 (Dogtag's built-in responder) | **local only** — needs the validator to reach back to the client |
| `test_03_phase2_direct.yml` | Direct CA enrolment with `pki ca-cert-request-submit --profile wrpacCert` and a WRPAC-shaped CSR | **local only** |
| `test_04_phase3_happy.yml` | Full CS-06 §6 happy path: `wrp-id` order → `registrar-api-01` challenge → finalize → cert download | local **or** public |
| `test_05_phase3_negative.yml` | Negative-test battery for CS-06 §7.2 server MUST clauses (missing EAB, unknown wrp-id, wrong key-auth, Subject mismatch, etc.) | local **or** public |
| `test_06_cert_profile.yml` | Parses a freshly-issued WRPAC and asserts every CS-06 §7.4 attribute | local **or** public |
| `test_07_persistence.yml` | Registers an ACME account, restarts `pki-tomcatd`, re-issues with the same account — proves the `ds` backend persists state | **local only** (uses acme.sh + systemctl) |
| `test_08_facade_persistence.yml` | Snapshots façade SQLite row counts, restarts `wrpac-acme-facade` + `wrpac-rp-list`, asserts counts unchanged — proves the Phase 3 façade & RP List persist state | **local only** (uses sqlite3 + systemctl) |

## Run from `deployment/` (one level up)

```sh
. .venv/bin/activate

# Local (internal) URL — default
ansible-playbook tests/test_all.yml

# Public URL
ansible-playbook tests/test_all.yml \
    -e test_acme_directory=https://rpca.lab.cleverbase.io/acme-eudi-wrpac/directory \
    -e test_rp_list=https://rpca.lab.cleverbase.io \
    -e test_acme_stock_directory=https://rpca.lab.cleverbase.io/acme/directory

# Single test
ansible-playbook tests/test_05_phase3_negative.yml -e test_acme_directory=...
```

## Variables

| Var | Default | Used by |
|---|---|---|
| `test_acme_directory` | `http://{{ ca_fqdn }}:{{ wrpac_facade_port }}/acme-eudi-wrpac/directory` | tests 1, 4, 5, 6 |
| `test_rp_list` | `http://{{ ca_fqdn }}:{{ wrpac_rp_list_port }}` | tests 1, 4, 5, 6 |
| `test_acme_stock_directory` | `https://{{ ca_fqdn }}:8443/acme/directory` | test 1 |
| `test_out_dir` | `/root/test-out` | tests 4, 6 |
