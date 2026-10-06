# Architectural Scoping of the European Business Wallet in the WE BUILD Consortium 

**Authors:**

- Miika Antila, Finnish Tax Administration, Finland

## Context

The European Business Wallet (EBW) is described at EU level with a broad functional scope. In reality, economic operators and public sector bodies alike sit within heterogeneous system landscapes of varying digital maturity, from spreadsheets to full ERP, on-premise or cloud-hosted, and in part supplied by the public sector (e.g. tax-reporting tools), in which operational business data and processes are already handled, while identity, mandates, and trust are cross-cutting infrastructure concerns.

Within the WE BUILD consortium, the EBW is referenced across architectures, diagrams, and use cases. However, the assumed architectural role of the EBW within the WE BUILD consortium architecture has not yet been explicitly scoped, creating a risk of differing interpretations when defining interfaces, responsibilities, and integration scope across consortium participants. 

This ADR documents an explicit architectural scoping assumption for the WE BUILD consortium, in order to support a shared understanding of how the EBW is treated within this architecture. It does not aim to define or constrain the EBW beyond the scope of the WE BUILD consortium. 

The EBW is intended to support interactions in which identity, trust, verifiability, or legally assured delivery is central. Business documents are exchanged via secure communication channel or other established document exchange infrastructures and remain authoritative at their source.

## Decision

Within the scope of the WE BUILD consortium architecture, the European Business Wallet is assumed to function primarily as **a set of standardised identity, trust, and authorisation services**. These capabilities may be consumed by various business applications, organisational processes, and digital services, independent of any specific system type. The wallet may also provide limited issuer capabilities for mandates, delegations, and other trust-related attestations within an organisation's trust domain. Within this architecture, the EBW serves as an entry and anchoring point into a broader trust infrastructure, rather than constituting the trust layer itself. 

Accordingly, within the WE BUILD consortium, the EBW is assumed to support: 
- Organisational identity representation 
- Operational authorisations and technical access management 
- Issuance of electronic attestations of attributes
- Presentation of electronic attestations of attributes
- Verification and validation of electronic attestations of attributes
- Presentation of legally signed or sealed documents and evidentiary objects
- Support for trust-based interactions requiring legal assurance, such as proof of delivery or receipt (e.g. via QERDS)

Transactional business data and operational workflows are assumed to remain primarily within business systems and their established integrations where applicable.

## Rationale

This architectural scoping is motivated by the following considerations: 
- **Alignment with enterprise realities:** Core business data and processes are already managed within mature enterprise systems that serve as authoritative sources of truth. 
- **Clear architectural layering:** Separating trust and identity infrastructure from transactional and process execution layers improves clarity, composability, and long‑term maintainability. 
- **Avoidance of parallel sources of truth:** Treating the EBW as a business system risks duplicating responsibilities already fulfilled elsewhere. 
- **Reduced integration complexity:** Focusing EBW integration on trust-related concerns keeps coupling low and reduces interoperability risk. 

The purpose of this scoping is to clarify the architectural assumptions under which components are designed and evaluated, not to constrain the evolution of the EBW beyond this scope. 

## Consequences

**Positive**
- Clear architectural boundaries for EBW usage within the WE BUILD consortium 
- Consistent interpretation across WE BUILD consortium implementations 
- Simpler, trust‑focused EBW integrations across the consortium 

**Trade-offs**
- Use cases envisioning the EBW as a single end-to-end business interaction channel need to be explicit about where document exchange and process execution sit, which may involve components outside this ADR
- Introducing trust services into existing integrations adds coordination cost between wallet providers and enterprise system owners

**Risk treatment**
- WP4 Architecture, with the WP3 Use Case Sync Leads, checks the WE BUILD use cases against this scoping and records any that do not fit, so gaps surface as issues rather than as divergent local interpretations
- The Blueprint Coordination Group confirms that Appendix D, the glossary, Chapter 1 and Chapter 4 read consistently with this ADR once merged
  
**Open points**
- A worked mapping of the WE BUILD use cases onto this scoping, to be contributed by the authors together with the WP3 Use Case Sync Leads
- Blueprint consistency check as set out under Risk treatment above

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
