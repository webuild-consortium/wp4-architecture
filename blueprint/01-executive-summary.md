# Executive Summary & Project Context
## Background
[WE BUILD](https://webuildconsortium.eu/) is a [Large Scale Pilot (LSP)](https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/pages/694487808/What+are+the+Large+Scale+Pilot+Projects) funded by the European Commission. It is a European project with a very practical mission: to use the European Digital Identity (EUDI) Wallet and European Business Wallet (EBW) to make life easier, faster, and cheaper for businesses and citizens across the EU. Our goal is to strengthen European competitiveness by removing the "red tape" that usually slows down cross-border transactions, like opening a bank account or registering a company branch in another country.

WE BUILD is strictly use-case driven. We have 13 specific use cases divided into three main areas:
- Business (WP2): Handling things like company registration and verified mandates.
- Supply Chain (WP2): Streamlining logistics, transport, and eInvoicing.
- Payments & Banking (WP3): Making secure, fraud-resistant payments and simplifying bank onboarding.

## WE BUILD’s Role in the EUDI and Business Wallet Journey
WE BUILD operates within, but is not identical to, the final legally mandated EUDI and Business Wallet ecosystem. While the final ecosystem represents the mandatory end-state for all EU Member States, WE BUILD is the practical proving ground where these rules are tested and refined through use cases.

### A Bridge to the Business Wallet 
While the final EUDI ecosystem mandates a wallet for every citizen at Level of Assurance (LoA) High, WE BUILD is specifically pioneering the European Business Wallet. Unlike the citizen-centric wallet, the BW is designed for economic operators to manage mandates, exchange professional documents like electronic invoices, and receive legally valid notifications. Some Business Wallet operations like onboarding and data portability target Level of Assurance (LoA) Substantial.

### Bridging ARF Gaps through Specifications and Testing
The final ecosystem is strictly governed by the official [Architecture Reference Framework (ARF)](https://eudi.dev/latest/architecture-and-reference-framework-main/). However, because the ARF is still evolving, it does not yet cover every detail needed for complex scenarios. Also, in WE BUILD pre-production tests and pilots, the full production certification and qualification schemes cannot always be applied.

To address this, WE BUILD uses [WE BUILD Conformance Specifications (WBCS)](https://github.com/webuild-consortium/wp4-architecture/tree/main/conformance-specs) and [Architectural Decision Records (ADRs)](https://github.com/webuild-consortium/wp4-architecture/tree/main/adr) to create consortium-specific rules that dictate the implementation for our pilots.

In the final ecosystem, wallets and services must undergo formal certification by national bodies. WE BUILD operates in a pilot setting but builds functional, interoperable software that is as close to production-ready as possible.

| WE BUILD will not… | …but we will… |
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
WP4 does not build technology for its own sake. Our technical groups - Architecture, Semantics, Wallet Providers, PID & EBWOID Provider, Qualified Trust Service Provider (QTSP), Trust Registry Infrastructure, and Test Infrastructure exist solely to provide the engine that powers the use cases. 

WP2 and WP3 use cases are expected to implement the technology provided by WP4, rather than develop parallel solutions. 

### How WP4 Works: From Strategy to Testing and Piloting
To ensure interoperability across participants, we use three levels of documentation:

1. This **Blueprint (D4.1)**: The "big picture." It describes high-level patterns and how the different parts of the system fit together.
2. [**Architectural Decision Records (ADRs)**](https://github.com/webuild-consortium/wp4-architecture/tree/main/adr) document and justify major architectural decisions. When we make a major choice (like which standard to use), we document it here to ensure everyone understands the rationale.
3. [**WE BUILD Conformance Specifications (WBCS)**](https://github.com/webuild-consortium/wp4-architecture/tree/main/conformance-specs) define the detailed technical requirements that implementations must follow. If you implement your service according to these specs, you will be able to pass our automated tests.

The Interoperability Testbed (ITB) is a first step toward understanding conformity assessment requirements. In a controlled consortium environment, regulatory and technical specifications are translated into executable interoperability scenarios to expose gaps. This builds the technical and organisational maturity required before entering formal certification processes.

## How to get started
The Blueprint is your starting point to understand the "WE BUILD way" of doing things.
- Technical teams should look for the WBCS to start building their interfaces.
- Architecture stakeholders should look for ADRs to understand the critical architecture decisions and compare these with other implementations.
- Every implementation must eventually pass through our [Interoperability Testbed (ITB)](https://github.com/webuild-consortium/wp4-interop-test-bed), to prove that your technical solution is ready for real-world piloting.

