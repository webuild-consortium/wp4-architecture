# Baseline protocols, formats and versions

**Authors:**

- Sarah Amandusson, Digg, Sweden

**Obsoletes:** [Baseline protocols](base-protocols.md)

## Context

Use cases are building implementations and need to know which ARF version applies, and whether new versions of standards will be introduced in a way that breaks what they have built. The earlier ADR [Baseline protocols](base-protocols.md) chose OpenID4VCI 1.0 and OpenID4VP 1.0, but did not cover the ARF version, formats, proximity, business-wallet-to-business-wallet exchange, or how versions change.

This ADR also records the concrete formats foreseen by [Specify PID and eAA formats](document-formats.md), which remains in force.

## Decision

**1. The WBCS are what you implement.** Each WBCS pins the exact versions of the specifications it builds on. Implementations and ITB tests follow the WBCS, not the latest upstream version.

**2. ARF 3.0.0 is the reference framework** for interactions with EUDI Wallets. WE BUILD takes ARF 3.0 requirements into the WBCS when a use case needs them, not all at once. Known deviations are listed in each WBCS. The ARF does not cover business wallets; for those, the WE BUILD ADRs and the EBW definition apply.

**3. Protocols**

| Interaction | Protocol | WBCS |
|---|---|---|
| Issuance (remote) | OpenID4VCI 1.0 with HAIP 1.0 | CS-01 |
| Presentation (remote) | OpenID4VP 1.0 with HAIP 1.0 | CS-02 |
| Presentation via browser | W3C Digital Credentials API | CS-07 |
| Proximity | ISO/IEC 18013-5, for use cases that need it | CS-014 |
| EBW to EBW, including automated (machine-to-machine) | OpenID4VCI / OpenID4VP as above, with [automatic approval](EBW-EAA-exchange-automation.md) and [mutual identification](mutual_identification.md) | CS-01, CS-02 |
| Business documents and messages | (Q)ERDS, see [Deliver business wallet data using QERDS (ADR)](build-qerds.md) and [EAA for verifiable claims (attestations), (Q)ERDS for data transfer (business documents)](adr-qeaa-attestations-qerds-documents.md) | CS-15, CS-16 |

WE BUILD does not introduce a separate machine-to-machine protocol for attestations within the pilot.

**4. Formats**

| Wallet | Formats |
|---|---|
| EUDI Wallet | SD-JWT VC (remote); mdoc (proximity) |
| European Business Wallet | SD-JWT VC; mdoc where proximity is needed. W3C VCDM 2.0 (JSON-LD) is not a baseline format: it is used only between business wallets in use cases that need it, as specified in a pre-flight WBCS (currently CS-019 for data spaces). |

JSON-LD is never used towards EUDI Wallets.

**5. How versions change**

- **Clarifications and additions that do not break implementations** raise the minor version of a WBCS (1.x).
- **Breaking changes** require a new major version of the WBCS (2.0) and are made only when:
  1. a regulation or implementing act requires it;
  2. a use case cannot work without it; or
  3. a security issue requires it.
- A breaking change is announced at UC sync and in the ITB, with a transition period of at least [8 weeks] during which the previous version remains testable.
- A new upstream version (for example OpenID4VCI 1.1) is adopted only through a new WBCS version, under the same conditions.

The first merged version of a WBCS, including a pre-flight, is 1.0.

## Consequences

**Easier:** use cases know what to build against and that it will not change without reason and notice. ITB tests have a stable reference.

**More difficult:** WE BUILD will lag behind the latest upstream versions. Requirements from ARF 3.0 that no use case asks for are not implemented in the pilot. WBCS that refer to ARF 2.9 must refer to ARF 3.0 at their next revision, and list any deviations.

**Risks and mitigation:** gaps to ARF 3.0 and to new upstream versions are documented in each WBCS, so they can be closed when needed or after the pilot. Use cases that need something not supported raise it at UC sync or as an issue, and the WBCS is extended.

## Advice

Once merged, this is our consortium's decision. This does not mean all participants agree it is the best possible decision. In the decision making process, we have heard the following advice.

- 2026-10-01, Wallet Providers Group (via thodoris): support aligning the WBCS with ARF 3.0, limited to the requirements the use cases need for the pilot.
- [#292](https://github.com/webuild-consortium/wp4-architecture/issues/292), stavamichal and MartinHurych-Aricoma: freeze on ARF 3.0 rather than 2.9, as the more mature version.
