# Executive Summary & Project Context
## Background
[WE BUILD](https://webuildconsortium.eu/) is a European project with a very practical mission: to use the European Digital Identity (EUDI) Wallet and Business Wallet to make life easier, faster, and cheaper for businesses and citizens across the EU. Our goal is to strengthen European competitiveness by removing the "red tape" that usually slows down cross-border transactions, like opening a bank account or registering a company branch in another country.

WE BUILD is strictly use-case driven. We have 13 specific use cases divided into three main areas:
- Business (WP2): Handling things like company registration and verified mandates.
- Supply Chain (WP2): Streamlining logistics, transport, and eInvoicing.
- Payments & Banking (WP3): Making secure, fraud-resistant payments and simplifying bank onboarding.

## WE BUILD’s Role in the EUDI Journey
It is important to distinguish between the final, legally mandated EUDI Wallet ecosystem and the work we are doing in WE BUILD. While the final ecosystem represents the mandatory end-state for all EU Member States, WE BUILD is the practical proving ground where these rules are tested, refined, and sometimes even invented through 13 use cases.

Below are the key areas where our pilot differs from the final production ecosystem:

### A Bridge to the Business Wallet 
While the final EUDI ecosystem mandates a wallet for every citizen at Level of Assurance (LoA) High, WE BUILD is specifically pioneering the European Business Wallet. Unlike the citizen-centric wallet, the BW is designed for economic operators to manage mandates, exchange professional documents like electronic invoices, and receive legally valid notifications. Core Business Wallet operations like onboarding and data portability target LoA Substantial.

### Filling the "ARF Gaps" with WBCS
The final ecosystem is strictly governed by the official [Architecture Reference Framework (ARF)](https://eudi.dev/latest/architecture-and-reference-framework-main/). However, because the ARF is still evolving, it does not yet cover every detail needed for complex scenarios. WE BUILD uses [WE BUILD Conformance Specifications (WBCS)](https://github.com/webuild-consortium/wp4-architecture/tree/main/conformance-specs) and [Architectural Decision Records (ADRs)](https://github.com/webuild-consortium/wp4-architecture/tree/main/adr) to create consortium-specific rules that "dictate the implementation" for our pilots. These specifications serve as our rulebook to ensure interoperability across all partners until the final EU standards are matured.

### Proving Readiness through Testing
In the final ecosystem, wallets and services must undergo formal certification by national bodies to ensure full legal compliance. Because we are in a pilot phase, WE BUILD relies on the Interoperability Testbed (ITB) as our primary gatekeeper. 

### From Lab to Near-Production
WE BUILD is not a theoretical exercise; we are building software that is functional, interoperable, and as close to production-ready as possible. 

## Work Package 4 (WP4) - General Capabilities
WP4 does not build technology for its own sake. Our technical groups - Architecture, Semantics, Wallet Providers, PID & EBWOID Provider, Qualified Trust Service Provider (QTSP), Trust Registry Infrastructure, and Test Infrastructure exist solely to provide the engine that powers the 13 use cases. We aim to create shared solutions so that each use case doesn't have to reinvent the wheel, saving time and project budget.

<!-- TODO: Is this true? How about testing things that the EC wants us to test or that would benefit the EUDIW/BW implementations in EU? -->  

### How WP4 Works: From Strategy to Testing and Piloting
To keep everyone aligned and ensure that a wallet from one country works with a verifier from another, we use three levels of documentation:

1. This **Blueprint (D4.1)**: The "big picture." It describes high-level patterns and how the different parts of the system fit together.
2. [**Architectural Decision Records (ADRs)**](https://github.com/webuild-consortium/wp4-architecture/tree/main/adr): This is where we record and justify the "Why." When we make a major choice (like which standard to use), we document it here to ensure everyone understands the rationale.
3. [**WE BUILD Conformance Specifications (WBCS)**](https://github.com/webuild-consortium/wp4-architecture/tree/main/conformance-specs): This is the "How." These are the detailed technical rules that developers follow. If you implement your service according to these specs, you will be able to pass our automated tests.

## How to get started
The Blueprint is your starting point to understand the "WE BUILD way" of doing things.
- Technical teams should look for the WBCS to start building their interfaces.
- Every implementation must eventually pass through our [Interoperability Testbed (ITB)](https://github.com/webuild-consortium/wp4-interop-test-bed), to prove that your technical solution is ready for real-world piloting.

Use cases set the requirements, and WP4 builds the interoperable foundation to meet them.

<!-- How do we go about writing about "the EUDI-compliant architecture positioning within the eIDAS and ARF context? -->  


