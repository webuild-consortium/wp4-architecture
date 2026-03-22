# Distinguish documents, data, and attestations as wallet content types

**Authors:**

- Rune Kjørlaug, OpenPeppol, Belgium

## Context

The European Business Wallet (EBW) proposal [COM(2025) 838 final](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0838) explicitly recognises three distinct content types that a Business Wallet may store and exchange: **data**, **documents**, and **attestations**. These are not interchangeable. The EBW proposal describes the wallet as a secure digital platform for storing and exchanging business documents (Recital 24), while Recital 14 lists "the digital management of representation rights and mandates, and a secure channel for exchanging official documents and attestations" as distinct capabilities.

Critically, Recital 27 of the EBW proposal specifies a **reference attestation** pattern, describing functionality that allows EBW owners to transmit a reference to a document, where appropriate with a cryptographic element such as a hash key to a sealed attestation issued by a Business Wallet, thereby attesting to the integrity and authenticity of the original submission. This is precisely the pointer-and-retrieve model: an attestation that certifies the existence and integrity of a document, without embedding the document's data content.

Despite this clear regulatory distinction, a recurring pattern has been observed across WE BUILD use cases: the conflation of "content carried in the wallet" with "wallet attestation". This leads use case designers to reach for the attestation model for artefacts — notably complex business documents — that the EBW proposal itself envisages being exchanged as documents via QERDS, or retrieved via authenticated reference.

Two use cases illustrate the problem concretely.

**SC1 — eCMR.** SC1 correctly scopes its ambition as integrating with existing eFTI platforms (not replacing them), and Scenario SC1.3/SC1.3bis explicitly describes eFTI-compliant cross-border transport by *connecting* eCMR datasets with Business Wallets. However, the eCMR attestation specification developed for SC1 — based on [UN/CEFACT eCMR D24A](https://unece.org/trade/documents/2024/12/standards/ecmr-d24a) — embeds the full eCMR payload as a wallet attestation. This contradicts both the SC1 boundary statement ("building or redesigning eFTI platforms is out of scope") and the [eFTI Regulation (EU) 2020/1056](https://eur-lex.europa.eu/eli/reg/2020/1056/oj) trust architecture, which requires freight transport information to remain authoritative on a certified eFTI platform, accessible via a unique identifying link on authenticated request.

The eCMR document is unsuitable as a full-payload attestation for several compounding reasons: it is a multi-party transport contract (consignor, carrier, consignee) with commercially sensitive data that must be shared only with authorised parties; it is mutable over its lifecycle (handovers, receipt confirmations, quantity corrections); and the eCMR D24A specification itself acknowledges that versioning in SD-JWT format is complex and not currently supported. The SC1 stock-taking document explicitly identifies "liability, audit trails, and non-repudiation in wallet-based cargo authorisation" as an open research objective — these are precisely the properties that QERDS and certified eFTI platforms provide, not wallet credential presentation.

**SC5 — eInvoicing.** SC5's core architecture is well-conceived: its MVP scenarios (1–3) use wallet attestations correctly to convey *relationship claims* — the Approved Supplier attestation (buyer issues, supplier holds, service provider verifies) and the Authorised Service Provider attestation (company issues, service provider holds, tax authority verifies). These are identity and authorisation claims, not business documents. This is the right use of attestations.

The risk in SC5 is Scenario 4: Direct eInvoicing using Business Wallets, in which the supplier issues the eInvoice as a verifiable attestation and sends it directly to the buyer's wallet. An EN 16931 / Peppol BIS Invoice is a structured legal and fiscal document, not an identity or status claim. Its exchange must be non-repudiable, auditable, and in many jurisdictions tax-compliant. Peppol and QERDS exist precisely for this. SC5 Scenario 5 (Peppol enhancements using qualified trust services including QERDS) correctly identifies the right direction for improving trust in Peppol flows and should be considered the preferred architecture for document-carrying scenarios.

The source of the confusion is understandable. The EBW proposal makes the wallet the central integration point for business interactions, and the credential tooling developed under eIDAS 2.0 (OpenID4VCI, SD-JWT, ISO 18013-5) is mature and well-documented. Implementing acts, conformance specifications, and rulebook templates all focus on attestations. There is as yet no equally mature, wallet-native flow specification for the Recital 27 reference attestation pattern — leaving a specification gap that causes use case designers to default to full-payload attestations. The interchangeable use of words like **data**, **documents**, **business documents** and **attesations** adds to this confusion.  

The following alternatives were considered:

- **Full-payload attestation in the wallet.** Encodes the complete document (e.g. eCMR, EN 16931 invoice) as a wallet credential. This is the approach proposed in the SC1 eCMR attestation specification. It is rejected for the reasons above: it bypasses eFTI certification requirements, is incompatible with the document's mutability and commercial sensitivity, and does not provide the non-repudiation properties that the use cases themselves identify as requirements.
- **Selective disclosure attestation covering document subsets.** Uses SD-JWT or mdoc selective disclosure to expose only relevant fields. This partially addresses data minimisation but does not resolve mutability, versioning, or regulatory certification. It also adds complexity disproportionate to a dataset the size of the eCMR or invoice models, and does not address the certification-chain requirement.
- **Reference attestation with on-demand document retrieval (recommended).** The wallet holds a minimal attestation — document reference, document hash, issuer, validity — per the Recital 27 pattern. The full document remains authoritative on a certified platform (eFTI or Peppol access point). Relying parties retrieve it on demand via QERDS or the eFTI unique-link mechanism. This is the model the EBW proposal itself describes, and aligns with the eFTI Regulation and Peppol network trust models.

## Decision

WE BUILD adopts the following separation of concerns between attestations, documents, and data in the Business Wallet:

**Attestations** convey identity attributes, status claims, and authorisation claims about a natural or legal person or their relationships (e.g. Approved Supplier, Authorised Service Provider, power of representation, mDL transport categories). They MAY also serve as **reference attestations** per EBW Recital 27 — carrying a document reference and cryptographic hash to prove the existence and integrity of an authoritative document, without embedding its payload.

**Documents** (e.g. PDFs) are enclosed bodies of structured, semi-structured and unstructured data intended for a natural person/human actor, and are exchanged via QERDS or equivalent relevant infrastructure (such as the Peppol network), and remain authoritative at their source platform. Where a wallet interaction is needed at a point of control, the wallet presents a reference attestation; the relying party retrieves the document via the relevant infrastructure.

**Business Documents** (e.g. eCMR, EN 16931 invoice) are structured datasets following a clearly defined and standardised machine readable format and are exchanged via QERDS or equivalent relevant infrastructure (such as the Peppol network), and remain authoritative at their source platform. Where a wallet interaction is needed at a point of control, the wallet presents a reference attestation; the relying party retrieves the document via the relevant infrastructure.

**Data** may be stored in the wallet and shared with relying parties as part of wallet-native flows, within the constraints of the applicable data model and access control rules.

For use cases requiring a human actor to present document-related information at a point of control (e.g. SC1.2 driver identification and cargo authorisation at port access, SC1.3bis public authority checkpoint):

1. **A minimal reference attestation** — in mDL or equivalent format — is held by the actor. It contains the minimum attributes to establish identity, role, and the existence of a registered document: document reference or eFTI unique link, document hash, issuing authority. It does not embed the document payload. It is designed for offline-capable proximity presentation.
2. **Authenticated document retrieval**, triggered by the relying party using the reference. The full document is retrieved from the certified eFTI platform via QERDS or the eFTI unique-link mechanism, with non-repudiation and audit trail.

For SC5 eInvoicing use cases:

- Scenarios 1–3 (Approved Supplier, Authorised Service Provider attestations) follow the attestation model and are architecturally sound as specified.
- Scenario 4 (direct wallet-to-wallet invoice exchange) SHALL apply the reference attestation pattern: the eInvoice is exchanged via QERDS as a document; the wallet holds a reference attestation that the relying party uses to retrieve and verify it. Direct embedding of an EN 16931 invoice as a wallet attestation payload is not recommended.
- Scenario 5 (Peppol enhancements with qualified trust services) is the preferred model for exploring how QERDS strengthens Peppol-connected flows, and should be progressed as MVP.

Responsibilities:

- WP3 Use Case Sync Leads review proposed attestation designs against this ADR before finalising attestation rulebooks. Where a full-payload attestation is proposed for a document type, the use case must justify how the document's mutability, commercial sensitivity, and chain-of-custody requirements are addressed.
- WP4 Architecture group maintains this ADR and provides the flow specification for the Recital 27 reference attestation pattern, in coordination with WP4 QTSP.
- WP4 QTSP group ensures that QERDS gateway and conformance specifications include the retrieval flows described in this ADR, specifically for eFTI-connected (SC1.3) and Peppol-connected (SC5 Scenario 4/5) use cases.

## Consequences

Adopting this separation makes it easier:

- To align with the EBW proposal's own content-type model: data, documents, and attestations are distinct, and Recital 27 explicitly describes the reference attestation as a first-class wallet capability.
- To maintain compliance with the eFTI Regulation (EU) 2020/1056: freight transport information remains authoritative on certified eFTI platforms; the wallet provides access and identity, not document transport.
- To comply with GDPR data minimisation: reference attestations present only the minimum attributes required for the interaction; full document data is accessed only by authorised parties on authenticated request.
- To handle document versioning correctly: the authoritative document at source is always current; reference attestations need only be reissued when document status changes materially (e.g. cancellation, replacement).
- To provide the non-repudiation and audit trail properties that SC1 identifies as open research objectives, by routing document exchange through QERDS.
- To build on existing qualified infrastructure (Peppol, eFTI platforms) via QERDS gateways rather than reimplementing document exchange inside wallet credential flows.

Open issues:

- **Reference attestation format and flow specification.** The EBW proposal describes the Recital 27 reference attestation pattern in general terms, but no implementing act or WE BUILD conformance specification yet defines the concrete format of a reference attestation (what attributes are required, how the eFTI unique link or Peppol document reference is encoded, how the hash is computed and bound). WP4 Architecture and WP4 QTSP groups should develop this specification as a priority, as it is a prerequisite for SC1.3 and SC5 Scenario 4.
- **Offline-capable reference attestation for roadside scenarios.** The reference attestation at Layer 1 must function without network connectivity at the point of presentation (e.g. driver presenting to roadside inspector). The hash and reference must be verifiable offline. The retrieval step requires connectivity, but this can be deferred until the authority actively requests the document. The threshold between offline-verifiable reference and online document retrieval needs to be specified for SC1.3bis.
- **SC5 Scenario 4 flow design.** Wallet-to-wallet direct invoice exchange is a legitimate use case for the EBW, but the invoice must transit via QERDS as a document, with the wallet acting as the endpoint. The UX flow for how a supplier triggers QERDS delivery via the wallet — and how the buyer's wallet receives notification and initiates retrieval — is not yet specified. This is also relevant to the PA4 dependency (business payments follow invoice delivery).

The following risks need to be addressed:

- **Specification vacuum drives full-payload defaults.** The reference attestation pattern is described in EBW Recital 27 but has no associated flow specification, credential schema, or conformance test. In the absence of guidance, use case leads will default to full-payload attestations because the tooling and templates exist. To address this risk, WP4 Architecture must publish a reference flow and minimal schema for the Recital 27 pattern before use cases enter specification finalisation. Use Case Sync Leads should treat absence of a reference attestation specification as a blocker, not a reason to use full-payload alternatives.
- **Conflation of "wallet-native" with "attestation-native".** Several wallet providers and implementers may assume that because something is exchanged via the wallet, it must be modelled as an attestation. The Recital 24 framing ("secure digital platform for storing and exchanging business documents") explicitly contradicts this. WP4 Architecture members engaging with SC1 and SC5 should use the EBW proposal's own content-type model — not just this ADR — to explain the distinction.
- **eFTI platform readiness.** SC1.3 depends on certified eFTI platforms being operational and accessible for authenticated retrieval. The eFTI Regulation applies in full from 9 July 2027, but platform certification is still in progress. For the WE BUILD pilot phase, use cases may need to operate against pre-production eFTI environments or mock platforms. This must be captured as a dependency in the SC1 specification phase rather than resolved by falling back to full-payload attestations.
- **Peppol gateway for SC5 Scenario 4/5.** QERDS-based delivery of Peppol-format invoices requires a gateway between the wallet's QERDS channel and the Peppol four-corner infrastructure. This gateway is not yet specified in WE BUILD. SC5 and WP4 QTSP should jointly define the gateway requirements as part of Scenario 5 specification, which is the natural vehicle for this work.

## Advice

Once merged, this is our consortium's decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

*(To be completed during review.)*
