# How the Wallet Interacts with Services

## Our Shared Design Principles
Modularity, standardization, versioning.

## High-Level Flows
- Credential issuance
- Presentation & verification
- Revocation and status checking

### General PID issuing process
Todo: EUDI: ARF
EBW: the issuing we do
This chapter describes the general **WE BUILD PID/EBWOID issuing process** in a sequence diagram.
Todo: Mention ETSI standardization: ETSI TS 119 472-3 for (Q)EAA and PID issuance. ETSI TS 119 476-3 will standardize WUA and WIA.

##  The Technical Languages We Use 
List of integration points that will be formalized in Conformance Specifications.

## Interaction Pattern: Attestation Issuance
To be authored by Group 6 (QTSP) and Group 7 (Wallets). Focuses on how use cases get data into the wallet (e.g., PID or QEAA) using protocols like OpenID4VCI (but no need to mention that part, stuff like that should be mainly in CS). 

The [WE BUILD Consortium Conformance Specification (CS)](https://github.com/webuild-consortium/wp4-architecture/blob/blueprint/updates-jan/conformance-specs/cs-01-credential-issuance.md) for high assurance credential issuance. The aim is to ensure that Wallet Units and Credential Issuers within the WE BUILD ecosystem interoperate consistently for the issuance of verifiable digital credentials with high security and privacy.

## Interaction Pattern: Attestation Presentation (Receiving) 
To be authored by Architecture and Wallets. This is the "Receiving" flow for Relying Parties, detailing how they request and receive verified attributes under the user's sole control using OpenID4VP. 

The [WE BUILD Conformance Specification for Credential Presentation](https://github.com/webuild-consortium/wp4-architecture/blob/blueprint/updates-jan/conformance-specs/cs-02-credential-presentation.md) describes how Wallet Units (WU) and Verifiers interoperate within the WE BUILD ecosystem. It covers presentation (request and response flows), interfaces between wallets and verifiers as well as security, privacy and interoperability requirements and same‑device and cross‑device invocation patterns

## Signature and Seal Integration 
To be authored by Group 6 (QTSP). Explains the technical flows for wallet-centric and QTSP-centric (remote) signing/sealing, allowing individuals to sign on behalf of a company with full legal effect

## Secure communication channel
In WE BUILD, the secure communication channel will be implemented through Qualified Electronic Registered Delivery Services (QERDS) operated by QTSPs. The core idea will be that whenever a message will need legal-grade delivery assurance (who sent what, to whom, and when it was received), it will be routed through QERDS so that delivery will be registered and can later be proven to a relying party. This “registered delivery” pattern will be positioned as an enabler for interactions between competent authorities, economic operators, and relying parties.

### From “registered delivery” to “digital identity wallets”
As a baseline a classic B2G/B2B situation will be used: an authority will notify an economic operator, the economic operator will respond, and the relying party will require evidence. With QERDS, both sides will use their QERDS providers to register sending and receiving, so that delivery will not be just transport, but will be a process that will produce trustworthy evidence.

WE BUILD will take the next step: wallets will become the user-facing endpoints (“wallet-centric delivery”). The sender wallet and recipient wallet will remain the places where users will read, will approve, and will manage messages, or where they will configure connections to backend systems to perform these actions. QERDS providers will form the delivery layer underneath, handling routing, inter-provider exchange, and evidence creation, while wallets will provide identity/authentication and user control.

### Technical flow (WE BUILD high-level)
WE BUILD will follow the QERDS architecture decomposition and the 4-corner delivery pattern:
1) Sender identification and authentication will be performed at the sender’s QTSP (wallet-driven).
2) Message submission will be performed from the sender wallet to the sender QERDS (QTSP A).
3) Discovery of the recipient’s QERDS endpoint and capabilities will be performed via common services (e.g., the European Digital Directory in accordance with the EUDI Wallet ARF).
4) Handshake and relay will be performed between QTSP A and QTSP B (QERDS-to-QERDS interoperability) and will be based on ETSI EN 319 522.
5) Recipient notification will be issued, followed by recipient authentication being performed at QTSP B.
6) Consignment and handover of the message and its metadata will be performed to the recipient wallet.
7) Evidence will be made accessible to sender and recipient wallets (submission/dispatch and receipt/consignment or non-delivery). Evidence will not necessarily be pushed; it will be stored and retrievable on demand, protected by qualified sealing and, where required, qualified timestamping.

#### Scaling to the EU Business Wallet: “reliable access points”
For the EU Business Wallet, the planned approach will position QERDS as a designated network of reliable access points: businesses and businesses with governments will interact across the EU by connecting their wallets to a chosen access point/QERDS provider, while interoperability will ensure end-to-end reachability without vendor lock-in. WE BUILD’s future implementation will pilot this “delivery layer” so that EBW-to-EBW and EBW-to-government messaging will reuse the same secure channel principles: mutual authentication, end-to-end integrity and confidentiality, interoperability across access points, and, when needed, timestamped evidence.

