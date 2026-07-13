# Business Wallet Unit Attestation based on TS3

**Authors:**

- Lal Chandran, iGrant.io, Sweden
- Nikolaos Triantafyllou, University of Aegean, Greece

## Context

The EUDI Wallet (CS-04) defines its Wallet Unit Attestation through [Technical Specification 3 (TS3)](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/blob/main/docs/technical-specifications/ts3-wallet-unit-attestation.md), where the Wallet Unit Attestation is composed as WUA = WIA + KA, that is, a Wallet Instance Attestation bound to one or more Key Attestations. TS3 lets Issuers determine a Wallet Unit's security level, authenticate it, and verify it has not been revoked for the lifetime of an issued attestation.

The [Wallet Unit Attestation and lifecycle management](wallet-unit-lifecycle-management.md) decision made a Wallet Unit Attestation mandatory for the European Business Wallet but did not fix its shape. The Business Wallet (CS-05) differs from the EUDI Wallet on several dimensions: it is a server or cloud-hosted service rather than an app on a personal device, its keys live in a Cloud HSM, an organisation-controlled HSM or server-side, and it plays Holder, Issuer and Verifier in one wallet at high, possibly batched or asynchronous, throughput.

A comparison of CS-04 and CS-05 shows that several dimensions can be reused from the EUDI Wallet approach as-is, while a smaller set requires CS-05-specific work. The settled, reused dimensions are roles, form factor, key custody, attestation shape, organisational identity carriage, and roles played. The open dimensions, addressed in separate ADRs, are lifecycle source, discovery, session binding, and throughput.

This ADR records the decision for the attestation shape dimension: how the Business Wallet Unit Attestation is structured.

## Decision

For WE BUILD Consortium usecases, the European Business Wallet SHALL adopt the TS3 Wallet Unit Attestation approach as the basis for the Business Wallet Unit Attestation (BWUA).

As a working hypothesis, the BWUA is composed as **BWUA = BWIA + SKA**, mirroring the TS3 WUA = WIA + KA structure:

- **BWIA** (Business Wallet Instance Attestation) attests the Business Wallet Unit and its components against the relevant requirements, in the role of the TS3 WIA.
- **SKA** (Server Key Attestation) attests the keys used for credential binding where those keys are held in a Cloud HSM, organisation-controlled HSM or server-side environment, in the role of the TS3 KA adapted to a server form factor and key custody.

The following dimensions are reused from the EUDI Wallet (CS-04) / TS3 approach as-is, adapted only for the Business Wallet form factor where noted:

- **Roles** — Business Wallet Provider, Admin(s) and Users.
- **Form factor** — server or cloud-hosted service.
- **Key custody** — Cloud HSM, organisation-controlled HSM, server-side, or any.
- **Organisational identity** — EBWOID carried as a claim, issued by member state business registries or similar.
- **Roles played** — Holder, Issuer and Verifier in one wallet.

The lifecycle source, discovery, session binding and throughput dimensions are out of scope for this ADR and are decided separately.

## Consequences

Reusing TS3 gives the Business Wallet a known, interoperable attestation model rather than a bespoke one, so Issuers and Relying Parties can reason about Business Wallet security and revocation using the same structure as the EUDI Wallet. The BWIA + SKA decomposition preserves the TS3 separation between attesting the instance and attesting the keys, while accommodating server-side and HSM-based key custody that the EUDI Wallet's device-bound model does not assume.

Because BWUA = BWIA + SKA is recorded as a working hypothesis, the precise profile, including formats, the SKA's relationship to HSM key-attestation mechanisms, and conformance criteria, remains to be elaborated via a conformance specification. Where the Business Wallet's server form factor diverges from TS3 assumptions about a local WSCD, those divergences must be made explicit so that Issuers are not exposed to attestation semantics that do not hold for a cloud-hosted wallet.

## Advice

Once merged, this is our consortium's decision. This does not mean all participants agree it is the best possible decision.
