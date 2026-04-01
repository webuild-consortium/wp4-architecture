# Supporting analysis: Separating attestations, documents, and data in EBW

*This document supports the  [Architecture Decision Record](./build-document-vs-attestation.md). It records the use-case analysis, layered model, open issues, and risks that informed the decision but are too detailed for the ADR itself.*

---

## Use-case analysis

### SC1 — eCMR

SC1 correctly scopes its ambition as integrating with existing eFTI platforms rather than replacing them. Scenario SC1.3/SC1.3bis explicitly describes eFTI-compliant cross-border transport by *connecting* eCMR datasets with Business Wallets. However, the eCMR attestation specification developed for SC1, based on [UN/CEFACT eCMR D24A](https://unece.org/trade/documents/2024/12/standards/ecmr-d24a), embeds the full eCMR payload as a wallet attestation. This contradicts both the SC1 boundary statement ("building or redesigning eFTI platforms is out of scope") and the [eFTI Regulation (EU) 2020/1056](https://eur-lex.europa.eu/eli/reg/2020/1056/oj) trust architecture, which requires freight transport information to remain authoritative on a certified eFTI platform, accessible via a unique identifying link on authenticated request.

The eCMR document is unsuitable as a full-payload attestation for several compounding reasons:

- It is a multi-party transport contract (consignor, carrier, consignee) with commercially sensitive data that must be shared only with authorised parties.
- It is mutable over its lifecycle: handovers, receipt confirmations, and quantity corrections all update the authoritative record.
- The eCMR D24A specification itself acknowledges that versioning in SD-JWT format is complex and not currently supported.
- The SC1 stock-taking document explicitly identifies "liability, audit trails, and non-repudiation in wallet-based cargo authorisation" as an open research objective. These are precisely the properties QERDS and certified eFTI platforms provide — not wallet credential presentation.

### SC5 — eInvoicing

SC5's MVP Scenarios 1–3 use wallet attestations correctly to convey *relationship claims*:

- **Approved Supplier attestation**: buyer issues, supplier holds, service provider verifies. This is an authorisation claim.
- **Authorised Service Provider attestation**: company issues, service provider holds, tax authority verifies. This is a delegation claim.

These are not business documents. Using attestations here is architecturally sound.

The risk is **Scenario 4**: Direct eInvoicing using Business Wallets, in which the supplier issues the eInvoice as a verifiable attestation and transmits it directly to the buyer's wallet. An EN 16931 / Peppol BIS Invoice is a structured legal and fiscal document, not an identity or status claim. Its exchange must be non-repudiable, auditable, and in many jurisdictions tax-compliant. Peppol and (Q)ERDS exist precisely for this.

**Scenario 5** (Peppol enhancements using qualified trust services including (Q)ERDS) correctly identifies the right direction for improving trust in Peppol-connected flows and should be treated as the preferred architecture for document-carrying scenarios and progressed as MVP.

---

## Layered model for points of control (SC1.2, SC1.3bis)

For scenarios requiring a human actor to present document-related information at a physical checkpoint (port gate, roadside inspection):

**Layer 1 — Minimal reference attestation (wallet-held, offline-capable)**

Carried in the wallet in mDL or equivalent format. Contains:
- Actor identity (driver / carrier)
- Transport authorisation attributes (vehicle category, cargo type)
- Document reference (eFTI unique link or equivalent)
- Document hash (cryptographic binding)
- Issuing authority
- Validity period

Does not embed document payload. Designed for proximity presentation (NFC, QR) and offline verification of the hash and reference.

**Layer 2 — Authenticated document retrieval (on demand, online)**

Triggered by the relying party (inspector, port authority) using the reference from Layer 1. The full eCMR is retrieved from the certified eFTI platform via (Q)ERDS or the eFTI unique-link mechanism, with non-repudiation and audit trail. Network connectivity is required for this step but may be deferred from the initial presentation interaction.

This two-layer model satisfies:
- The eFTI Regulation's requirement for information to remain authoritative on certified platforms
- GDPR data minimisation at the point of presentation
- Operational robustness at locations with limited connectivity

---

## Open issues

**Reference attestation format and flow specification**

The EBW proposal describes the Recital 27 pattern in general terms, but no implementing act or WE BUILD conformance specification yet defines the concrete format: what attributes are required, how the eFTI unique link or Peppol document reference is encoded, how the hash is computed and bound to the attestation. WP4 Architecture and WP4 QTSP should develop this specification as a priority — it is a prerequisite for SC1.3 and SC5 Scenario 4.

**Offline-capable reference attestation for roadside scenarios**

The Layer 1 reference attestation must function without network connectivity at the point of presentation (e.g. driver presenting to roadside inspector). The hash and document reference must be verifiable offline. The threshold between offline-verifiable reference and online document retrieval needs to be specified for SC1.3bis, including what the inspector's workflow is when connectivity is unavailable.

**SC5 Scenario 4 — wallet-triggered QERDS delivery flow**

Wallet-to-wallet direct invoice exchange is a legitimate EBW use case, but the invoice must transit via QERDS as a document, with the wallet acting as the QERDS endpoint. The UX flow for how a supplier triggers QERDS delivery from the wallet — and how the buyer's wallet receives notification and initiates retrieval — is not yet specified. This is also relevant to the PA4 dependency (business payments follow invoice delivery).

---

## Risks

**Specification vacuum drives full-payload defaults**

The reference attestation pattern is described in EBW Recital 27 but has no associated flow specification, credential schema, or conformance test. In the absence of guidance, use case leads will default to full-payload attestations because the tooling and templates already exist. WP4 Architecture must publish a reference flow and minimal schema before use cases enter specification finalisation. WP3 Use Case Sync Leads should treat absence of a reference attestation specification as a **blocker**, not a reason to use full-payload alternatives.

**Conflation of "wallet-native" with "attestation-native"**

Wallet providers and implementers may assume that because something is exchanged via the wallet, it must be modelled as an attestation. EBW Recital 24 ("secure digital platform for storing and exchanging business documents") explicitly contradicts this. WP4 Architecture members engaging with SC1 and SC5 should use the EBW proposal's own content-type model to explain the distinction directly, not only reference this ADR.

**eFTI platform readiness**

SC1.3 depends on certified eFTI platforms being operational and accessible for authenticated retrieval. The eFTI Regulation applies in full from 9 July 2027, but platform certification is still in progress. For the WE BUILD pilot phase, use cases may need to operate against pre-production eFTI environments or mock platforms. This must be captured as a dependency in the SC1 specification phase, not resolved by falling back to full-payload attestations.

**Peppol gateway for SC5 Scenarios 4 and 5**

QERDS-based delivery of Peppol-format invoices requires a gateway between the wallet's QERDS channel and the Peppol four-corner infrastructure. This gateway is not yet specified in WE BUILD. SC5 and WP4 QTSP should jointly define gateway requirements as part of Scenario 5 specification.

---

## Responsibilities

| Action | Owner |
|---|---|
| Define minimal reference attestation schema and retrieval flow (Recital 27) | WP4 Architecture + WP4 QTSP |
| Review SC1 eCMR attestation specification against this ADR; identify required changes | WP3 SC1 Use Case Sync Lead |
| Review SC5 Scenario 4 against this ADR; confirm QERDS delivery model | WP3 SC5 Use Case Sync Lead |
| Ensure QERDS gateway and conformance specs include eFTI and Peppol retrieval flows | WP4 QTSP |
| Define eFTI pre-production environment dependencies for SC1 pilot | WP3 SC1 Use Case Sync Lead + WP4 |
| Define SC5 Scenario 4 wallet UX flow for QERDS-triggered invoice delivery | WP3 SC5 + WP4 Architecture |