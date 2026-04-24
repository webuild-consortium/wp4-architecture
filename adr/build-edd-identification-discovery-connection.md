# Structure the European Digital Directory as identification, discovery, and connection

**Authors:**

- Rune Kjørlaug, OpenPeppol, Belgium

## Context

The EBW proposal [COM(2025) 838 final](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0838) establishes the **European Digital Directory (EDD)** in Article 10 as the trusted source for locating and contacting EBW owners. The regulation implicitly combines three logically distinct operations into a single "directory" concept: **identification** (resolving an actor to a stable legal identifier), **discovery** (finding which networks and processes they are reachable through), and **connection** (retrieving the technical endpoint for message delivery). Without explicit separation, the EDD risks becoming a duplicated capability registry re-implementing what existing EU eDelivery infrastructure already provides.

A further complication is that the EUID, the primary legal identifier for registered companies under Directive (EU) 2017/1132, is itself ISO 6523-compliant by regulatory mandate: Commission Implementing Regulation (EU) 2021/1042 specifies in its Annex that *"the structure of the EUID shall be compliant with ISO 6523."* This means the EDD, Peppol, and EN 16931 already share a coherent identifier framework, and the EDD should build on that rather than introduce a parallel layer. However, EUID and BRIS do not cover sole traders, self-employed persons, or public institutions, leaving a registration gap for actor types that appear frequently in SC1 and SC5 use cases.

Three approaches to the discovery and connection layers were considered. A **proprietary EDD API** specified by Commission implementing act alone would create parallel, incompatible discovery infrastructure alongside existing eDelivery networks. **Decentralised identifier resolution** (W3C DIDs, distributed ledger approaches) is conceptually interesting but incompatible with AS4/ISO 6523 networks within the WE BUILD timeframe. **eDelivery BDXL 2.0 combined with ecosystem SMP 2.0** reuses proven, EU-mandated infrastructure: BDXL 2.0 resolves an ISO 6523 identifier to a capability registry URL using a Service-to-network and Process-to-process mapping; the ecosystem's own SMP (e.g. Peppol Discovery building block) handles endpoint detail. This keeps the EDD lean and supports federated operation.

This ADR covers infrastructure-mediated document exchange (QERDS, AS4/Peppol, eFTI). Discovery for direct wallet-to-wallet flows using OpenID4VC/VP raises different architectural and privacy considerations and is recorded as an open issue in the [supporting analysis](./build-edd-identification-discovery-connection-analysis.md).

*For detailed analysis including sequence diagrams, the BDXL 2.0 profile design, identification gaps, and risks, see the [supporting analysis](./build-edd-identification-discovery-connection-analysis.md).*

## Decision

The EDD SHALL be defined as a **federated legal identity resolver and discovery entry point** only. Capability registration, endpoint storage, and routing are delegated to ecosystem-specific registries.

The EDD SHALL:
- resolve economic actors to ISO 6523-compliant identifiers (EUID for registered companies; national ICD scheme values for actors not covered by EUID)
- return references to ecosystem discovery locators at network and process level (BDXL 2.0, WE BUILD profile)
- support registration of sole traders and public sector bodies using ISO 6523 ICD catalog entries

The EDD SHALL NOT:
- store AS4/SMP-style capability registry data (document type capabilities, AS4 endpoint addresses, transport certificates) — these belong in ecosystem-specific registries
- perform routing or protocol negotiation
- replace ecosystem capability registries (Peppol SMP, QERDS provider registries, eFTI gateway registries)
- replace authoritative legal business registries

The EDD machine API SHALL be deterministic and identifier-based. Human search capabilities (by name or attributes) SHALL NOT be normative for machine routing.

The recommended three-step stack for WE BUILD:

```mermaid
flowchart LR
    A[Sending System] --> B
    B["Step 1 · EDD\nIdentification\nEUID / ISO 6523"] --> C
    C["Step 2 · BDXL 2.0\nDiscovery\nNetwork + Process"] --> D
    D["Step 3 · Ecosystem SMP\nConnection\nEndpoint + Certificate"] --> E
    E[Access Point / QERDS / eFTI]
```

## Consequences

Structuring the EDD as three separated steps makes it easier to:
- reuse proven, EU-mandated eDelivery infrastructure (BDXL 2.0, SMP 2.0) rather than specifying a new directory protocol
- support federated operation. Each ecosystem manages its own capability registry without a central point of failure
- maintain a single coherent identifier model. EUID is ISO 6523-compliant (Reg. (EU) 2021/1042), aligning with Peppol and EN 16931
- keep the EDD lean and future-proof. Ccapability updates require no change to the EDD identity and discovery layers

It makes it more difficult to:
- proceed to end-to-end testing without a BDXL 2.0 WE BUILD profile (Service → network, Process → process mapping)
- onboard sole traders and public sector bodies, who are not covered by EUID/BRIS. Interim registration paths must be defined before affected use cases can proceed

The main risks introduced by this decision are: the pilot directory diverging from the eventual EDD implementing act standard; the identification gap blocking use case testing; and scope creep into existing Peppol infrastructure if the BDXL/SMP boundary is not maintained. These are addressed by WP4 Trust Registry Infrastructure developing the BDXL 2.0 WE BUILD profile as a first deliverable, defining interim registration paths for sole traders and public sector bodies, and engaging the Commission's EDD implementing act process proactively with documented design decisions.

## Advice

Once merged, this is our consortium's decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- [2026-02-11, Rune Kjørlaug, OpenPeppol, Belgium](https://github.com/webuild-consortium/wp4-architecture/pull/61#pullrequestreview-3785222841): Contributed the original three-step model (identification, discovery, connection) and the BDXL 2.0 proposal, noting EUID coverage gaps for sole traders and public sector bodies. This ADR is the result of that comment.
- [2026-03-13, Erlend Klakegg Bergheim, OpenPeppol, Belgium]: Corrections on ebCore Party Id (not used in Peppol; Peppol uses its own variant), DIDComm viability, SMP 2.0 profiling approach (Service → network, Process → process), recommendation to limit step 2 to process level only, EN 16931 regulatory basis for ISO 6523 coverage, and caution against routing non-Peppol ecosystems through existing Peppol SML/SMP infrastructure.
- [2026-03-27, Florin Cora, Bosch, Germany](https://github.com/webuild-consortium/wp4-architecture/pull/145): Raised that the SHALL NOT on endpoints was too broad, as the EDD may need to locate wallet metadata endpoints for OpenID4VC/VP flows. Also raised that centralised discovery intermediaries for peer-to-peer wallet flows create a metadata observation risk. These comments correctly identified a scope gap: this ADR covers infrastructure-mediated document exchange only; OpenID4VC/VP wallet discovery is recorded as an open issue requiring separate specification with privacy-by-design as a first-order requirement. Florin's broader suggestion that business documents should be transported as wallet attestations to address this privacy concern was not accepted: B2B capability metadata is categorically different from personal credential presentation and does not warrant the same architectural response.