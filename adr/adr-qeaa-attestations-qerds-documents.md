# ADR: (Q)EAA for verifiable claims (attestations), (Q)ERDS for data transfer (business documents)

| | |
|---|---|
| **Status** | Proposed |
| **Date** | 2026-06-11 |
| **Context** | WE BUILD WP4 — Architecture |
| **Related** | EDD three-layer model ADR; SC5 eInvoicing scenario specifications |

## Context

Neither eIDAS (as amended by Regulation (EU) 2024/1183) nor the proposed EU Business Wallet regulation (COM(2025) 838) provides a definition of an attestation beyond it being a structured piece of data that is signed or sealed by its issuer. In the EUDI Wallet context this under-specification is workable: the holder is a natural person, scoped by the device in use, and the wallet is in practice the system of record for the credentials it holds.

In the business wallet ecosystem this assumption does not hold. The wallet of an Economic Operator (EO) is connected to a broader suite of business systems — ERP, invoicing, procurement, archiving — that already act as systems of record for business transactions. If "anything signed and structured" can be carried as an attestation, the attestation mechanism becomes a de facto data transfer channel, duplicating and competing with established document exchange infrastructures rather than complementing them.

The stated aim of WE BUILD is that the EUBW should **complement, not replace, existing systems**. This requires a clear architectural boundary between what is conveyed as an attestation and what is exchanged as a business document.

## Decision

Within WE BUILD we adopt the following definitions and assign each concept to a distinct mechanism:

**Attestations ((Q)EAA)** are verifiable claims about an Economic Operator whose validity is lifecycle-managed at the source. While the claim content itself is integrity-protected and tamper-evident, its validity is mutable: the issuer can suspend or revoke it at any time, and relying parties are expected to check current status, not just signature validity.

**Business documents** are self-contained, structured or unstructured data artifacts that represent a business fact or transaction at a specific point in time. Once issued by its source, a business document is immutable — its content is finalized, and any subsequent change is expressed as a new document (e.g., a correction, amendment, or credit note), never as a modification of the original.

From these definitions follows the central rule of this ADR:

> **Business documents are not to be transferred as attestations.** Attestations are conveyed and presented via the (Q)EAA mechanisms of the wallet ecosystem; business documents are exchanged via electronic registered delivery services ((Q)ERDS) or other established document exchange infrastructures.

## Rationale

The two concepts differ in their fundamental temporal and lifecycle semantics:

| | Business document | Attestation |
|---|---|---|
| Asserts | What happened (historical fact) | What currently holds (status, capability, authorization) |
| Content | Immutable after issuance | Integrity-protected, fixed at issuance |
| Validity | Final — corrections via new, linked documents | Mutable — managed at source (suspension, revocation, expiry) |
| Verification | Integrity and authenticity of the artifact | Integrity **plus** current status at source |
| Natural mechanism | (Q)ERDS / document exchange networks | (Q)EAA |

A document asserts a historical fact and is therefore immutable; an attestation asserts an ongoing state and is therefore lifecycle-managed. Conflating the two creates concrete problems:

1. **Revocation semantics break down.** An invoice carried as an attestation would inherit revocation semantics that have no business meaning — an issued invoice cannot be "revoked," only credited or corrected through a new document.
2. **Systems of record are duplicated.** Treating documents as wallet-held attestations positions the wallet as a parallel store of transactional data, in conflict with existing ERP and archiving obligations (including statutory bookkeeping requirements).
3. **Established exchange infrastructure is bypassed.** Document exchange networks provide delivery evidence, addressing, and validation capabilities that the attestation presentation flow does not replicate. Routing documents through attestation channels discards these capabilities without replacement.
4. **Status-checking load is misdirected.** Relying parties would be expected to perform status checks against issuers for artifacts whose validity, by definition, never changes.

Conversely, the combination of the two mechanisms is where the value lies: attestations (e.g., ApprovedSupplier, AuthorizedServiceProvider) establish *who the parties are and what they are entitled to do*, while the document exchange conveys *what was transacted*. Attestations may be referenced from or embedded in business documents to bind transaction to entitlement, without changing the transfer mechanism of the document itself.

## Consequences

**Positive**

- Clear interoperability boundary: the EUBW integrates with, rather than substitutes for, existing document exchange infrastructure.
- Each artifact type gets verification semantics that match its nature — status checks for attestations, integrity/authenticity verification and delivery evidence for documents.
- Existing legal and operational frameworks (eInvoicing directives, ViDA, bookkeeping legislation, Peppol agreements) remain applicable to documents without reinterpretation.

**Negative / trade-offs**

- Two mechanisms must be operated and governed instead of one; scenarios involving both (e.g., attestation-bound invoicing) require explicit binding patterns.
- Edge cases exist where classification requires judgment (e.g., a certificate of conformity attached to a delivery). The decisive test is lifecycle semantics: if validity is managed at the source after issuance, it is an attestation; if the content is final at issuance, it is a document.

**Open points**

- Specification of the binding pattern between attestations and business documents (reference vs. embedding) is addressed in a separate ADR.
- The boundary between (Q)ERDS and non-qualified but established delivery networks is treated in the MLS/ERDS analysis and is out of scope here.
