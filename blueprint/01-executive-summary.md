# Executive Summary & Project Context
## Background
[WE BUILD](https://webuildconsortium.eu/) is a [Large Scale Pilot (LSP)](https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/pages/694487808/What+are+the+Large+Scale+Pilot+Projects) funded by the European Commission. The project tests how the European Digital Identity (EUDI) Wallet and the European Business Wallet (EBW) can support cross-border business processes across the EU.

The goal is practical: reduce administrative barriers that slow down companies when they operate across borders, such as opening a bank account, exchanging trusted business documents, or registering a branch in another country.

WE BUILD is organised around 13 concrete use cases that demonstrate how digital identity wallets can support real business processes. These use cases are grouped into three main areas:

- Business (WP2) – processes such as company registration, mandates and representation.
- Supply Chain (WP2) – logistics, transport documentation and electronic invoicing.
- Payments & Banking (WP3) – secure payments and simplified onboarding to financial services.

## WE BUILD’s Role in the EUDI and EBW Journey
WE BUILD operates within the emerging EUDI and Business Wallet ecosystem, but it is not the final production environment. Instead, the project acts as a large-scale pilot where technical solutions, governance models and interoperability rules can be tested through real use cases.

In the final EUDI ecosystem, every EU citizen will receive an EUDI Wallet at Level of Assurance (LoA) High.

WE BUILD focuses in particular on the European Business Wallet (EBW). The EBW is designed for economic operators to manage mandates, exchange trusted business documents such as electronic invoices, and receive legally valid notifications. Some Business Wallet functions, such as onboarding and data portability, will operate at Level of Assurance (LoA) Substantial.

### Bridging ARF Gaps through Specifications and Testing

The future EUDI ecosystem is defined through the [Architecture Reference Framework (ARF)](https://eudi.dev/latest/architecture-and-reference-framework-main/). However, the ARF is still evolving and does not yet cover every detail needed for complex implementation scenarios. In the WE BUILD pilot environment, the full certification and qualification schemes used in production cannot always be applied.

To address these gaps, WE BUILD defines project-specific implementation rules through: 
- [WE BUILD Conformance Specifications (WBCS)](https://github.com/webuild-consortium/wp4-architecture/tree/main/conformance-specs) – technical rules that implementations must follow.
- [Architectural Decision Records (ADRs)](https://github.com/webuild-consortium/wp4-architecture/tree/main/adr) documented architecture decisions that guide the project.

In the final ecosystem, wallets and services must undergo formal certification by national supervisory bodies. WE BUILD operates in a pilot setting, but the project still aims to build interoperable software that is as close as possible to production-ready systems.

| WE BUILD does not | WE BUILD does |
|---------------|----------------|
| certify EUDI wallets | provide WE BUILD wallets that pass the ITB |
| rely on eIDAS-eID | provide WE BUILD-eID, with fictitious but realistic identities |
| create eIDAS-qualified e-signatures | define WE BUILD-qualification of e-signatures, focusing on realistic technical interoperability |
| use real MS registries | involve real public sector bodies where possible, and otherwise simulate them, always with fictitious registries |
| use the EC List of Trusted Lists (LoTL) | provide a WE BUILD LoTL |
| use the MS Trusted lists (TL) | provide WE BUILD TLs, with feedback from real supervisory bodies if available |
| reach production-level legal liability | operate within the WE BUILD agreement and trust framework, not within eIDAS |
| deal with national policy-making | let the WP5 MS Forum indicate where alignment with national policy-making is advisable |
| deal with universal definitions | assess how far WE BUILD semantics can go within the available timeframe |
| issue EUDIW-RP access certificates | issue WE BUILD RP access certificates |
| issue eIDAS-QEAA | define WE BUILD-QEAA, focusing on realistic technical interoperability |

## Work Package 4 (WP4) - General Capabilities
WP4 provides the shared technical capabilities that enable the WE BUILD use cases. Our technical groups - Architecture, Semantics, Wallet Providers, PID & EBWOID Provider, Qualified Trust Service Provider (QTSP), Trust Registry Infrastructure, and Test Infrastructure exist solely to provide the engine that powers the use cases. 

WP2 and WP3 use cases are expected to use the capabilities provided by WP4 rather than developing parallel technical solutions.

To ensure interoperability across participants, WE BUILD uses three levels of documentation:

1. This **Blueprint (D4.1)** - the high-level architecture and system overview.
2. [**Architectural Decision Records (ADRs)**](https://github.com/webuild-consortium/wp4-architecture/tree/main/adr) - explain major architecture decisions and the reasoning behind them.
3. [**WE BUILD Conformance Specifications (WBCS)**](https://github.com/webuild-consortium/wp4-architecture/tree/main/conformance-specs) – define the detailed technical requirements that implementations must follow.

The Interoperability Testbed (ITB) is a first step toward understanding conformity assessment requirements. In a controlled consortium environment, regulatory and technical specifications are translated into executable interoperability scenarios.

## How to get started
The Blueprint is the starting point for understanding how WE BUILD works.

- Technical teams should begin with the WBCS to implement their interfaces.
- Architects should review the ADRs to understand the key architecture decisions.
- Every implementation must pass through the [Interoperability Testbed (ITB)](https://github.com/webuild-consortium/wp4-interop-test-bed) before participating in pilots.

