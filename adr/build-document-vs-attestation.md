# Separate attestations, documents, and data in EBW

**Authors:**

- Rune Kjørlaug, OpenPeppol, Belgium

## Context

The EBW proposal [COM(2025) 838 final](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0838) distinguishes three wallet content types: **data**, **documents**, and **attestations** (Recitals 14, 24, 27). Recital 27 explicitly introduces a **reference attestation** (a pointer and cryptographic hash to a sealed document) as a first-class wallet capability, distinct from embedding a full document payload in a credential.

In practice, WE BUILD use cases (notably SC1 eCMR and SC5 Scenario 4) have modelled complex business documents as full-payload wallet attestations. This conflicts with the [eFTI Regulation (EU) 2020/1056](https://eur-lex.europa.eu/eli/reg/2020/1056/oj), which requires freight transport information to remain authoritative on certified platforms, and with the non-repudiation and audit-trail requirements that Peppol and QERDS are designed to provide.

Three options were considered. **Full-payload attestation** — embedding the complete document as a wallet credential. This was rejected: it bypasses eFTI certification requirements, is incompatible with document mutability and commercial sensitivity, and does not provide non-repudiation. **Selective disclosure** over document subsets using SD-JWT or mdoc was also rejected: it does not resolve mutability, versioning, or platform certification requirements, and adds disproportionate complexity. The **reference attestation with on-demand retrieval** model where the wallet holds a minimal attestation (document reference + hash + issuer) per Recital 27, while the full document remains authoritative on the certified platform and is retrieved on demand. This aligns with the EBW proposal, the eFTI Regulation, and established Peppol and (Q)ERDS trust models.

The root cause of the observed conflation is a specification gap: Recital 27 describes the reference attestation pattern but no conformance specification or credential schema yet exists for it, causing use case designers to default to full-payload alternatives.

*For detailed use-case analysis (SC1 eCMR, SC5 eInvoicing) and the layered model for roadside inspection scenarios, see the [supporting analysis](./build-document-vs-attestation-analysis.md).*

## Decision

WE BUILD adopts a strict separation between attestations, documents, and data:

**Attestations** SHALL convey identity attributes, status claims, and authorisation claims. They MAY also function as **reference attestations** per EBW Recital 27, carrying a document reference and cryptographic hash without embedding document payload.

**Documents** (e.g. eCMR, EN 16931 invoice) SHALL NOT be stored as full-payload wallet attestations. They SHALL be exchanged via QERDS, Peppol, or certified eFTI platforms, and retrieved on demand using a reference attestation.

**Data** MAY be stored in the wallet and shared with relying parties within the applicable data model and access control constraints.

Full-payload document attestations are **rejected** for complex business documents. Where a wallet interaction is required at a point of control, the reference attestation pattern SHALL be applied: the wallet presents the reference; the relying party retrieves the document via an authenticated channel.

## Consequences

Adopting this separation makes it easier to:
- comply with the EBW content-type model, the eFTI Regulation, and GDPR data minimisation
- handle document versioning and lifecycle correctly — the authoritative source remains current; the wallet holds only a reference
- provide non-repudiation and audit trail via (Q)ERDS
- reuse existing qualified infrastructure (Peppol, eFTI platforms) rather than reimplementing document exchange inside wallet credential flows

It makes it more difficult to:
- finalise use case specifications before the reference attestation format and retrieval flow are defined — this is a **blocker** and must not be resolved by falling back to full-payload alternatives
- integrate with use cases that have already invested in full-payload attestation designs (SC1 eCMR in particular requires rework)

The main risk introduced by this decision is the specification gap itself: in the absence of a reference attestation schema and flow, use case leads face pressure to use full-payload attestations because the tooling and templates for those already exist. This is addressed by treating the reference attestation specification as a priority deliverable for WP4 Architecture, and by WP3 Use Case Sync Leads reviewing all proposed attestation designs against this ADR before finalising rulebooks.

## Advice

Once merged, this is our consortium's decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

*(To be completed during review.)*