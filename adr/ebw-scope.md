# Architectural Scoping of the European Business Wallet in the WE BUILD Consortium 

**Authors:**

- Miika Antila & TAX FI project team, Finnish Tax Administration, Finland

## Context

The European Business Wallet (EBW) is described at EU level with a broad functional scope. At the same time, enterprises typically operate established system landscapes where operational business data and business processes are managed in ERP, financial, CRM, and domain‑specific systems, while identity, mandates, and trust are handled as cross‑cutting infrastructure concerns. 

Within the WE BUILD consortium, the EBW is referenced across architectures, diagrams, and use cases. However, the assumed architectural role of the EBW within the WE BUILD consortium architecture has not yet been explicitly scoped, creating a risk of differing interpretations when defining interfaces, responsibilities, and integration scope across consortium participants. 

This ADR documents an explicit architectural scoping assumption for the WE BUILD consortium, in order to support a shared understanding of how the EBW is treated within this architecture. It does not aim to define or constrain the EBW beyond the scope of the WE BUILD consortium. 

## Decision

Within the scope of the WE BUILD consortium architecture, the European Business Wallet is assumed to function primarily as **a set of standardised identity, trust, and authorisation services**, used by enterprise systems to participate in trust-based interactions within the broader trust infrastructure, rather than as an operational business system or as an ERP‑level data exchange platform. This may include limited issuer capabilities for mandates, delegations, or other trust-related attestations within an organisation’s own trust domain, where such issuance is anchored in the broader trust infrastructure. Within this architecture, the EBW serves as an entry and anchoring point into a broader trust infrastructure, rather than constituting the trust layer itself. 

Accordingly, within the WE BUILD consortium, the EBW is assumed to support: 
- Organisational identity representation 
- Mandates, delegations, and representation rights 
- Trust anchors and verifiable attestations issuance and verification 
- Presentation of legally signed or sealed artefacts as evidentiary objects
- Trust-based interactions requiring legal assurance, such as proof of delivery or receipt (e.g. via QERDS) 

Within the WE BUILD consortium architectural scope, the EBW is not assumed to: 
- Act as a system of record for operational business data 
- Orchestrate or execute business processes 
- Act as a general-purpose system integration or data exchange channel (e.g. ERP‑to‑ERP or CRM‑to‑CRM)

Transactional business data and operational workflows are assumed to remain within existing enterprise systems and their established integrations. 

This decision represents an architectural scoping assumption specific to the WE BUILD consortium. It does not constitute a policy‑level interpretation of the EBW, nor does it restrict how the EBW may be used or implemented outside the WE BUILD consortium context. 

## Rationale

This architectural scoping is motivated by the following considerations: 
- **Alignment with enterprise realities:** Core business data and processes are already managed within mature enterprise systems that serve as authoritative sources of truth. 
- **Clear architectural layering:** Separating trust and identity infrastructure from transactional and process execution layers improves clarity, composability, and long‑term maintainability. 
- **Avoidance of parallel sources of truth:** Treating the EBW as a business system risks duplicating responsibilities already fulfilled elsewhere. 
- **Reduced integration complexity:** Limiting EBW integration to trust‑related concerns lowers coupling and interoperability risk. 

The purpose of this scoping is to clarify the architectural assumptions under which components are designed and evaluated, not to constrain the evolution of the EBW beyond this scope. 

## Consequences

**Positive**
- Clear architectural boundaries for EBW usage within the WE BUILD consortium 
- Consistent interpretation across WE BUILD consortium implementations 
- Simpler, trust‑focused EBW integrations across the consortium 

**Trade‑offs**
- WE BUILD consortium use cases envisioning a single end‑to‑end business interaction channel may partially fall outside this architectural scope 
- Such scenarios may require complementary components or architectural layers not addressed by this decision 
 
**Open Questions**
- Is this EBW scoping aligned with the WE BUILD consortium use cases and requirements? 
- Should this assumption be adopted as a stable architectural baseline for the consortium? 
- Are explicit deviations required for specific WE BUILD consortium use cases? 

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
