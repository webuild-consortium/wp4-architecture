# Appendix A. Glossary

## Terms and Definitions

This appendix defines the key terms, regulatory frameworks, and technical specifications utilised throughout the WE BUILD ecosystem.

While this document avoids abbreviations as much as possible, commonly used abbreviations are included for reference.

| Term | Abbreviation | Definition |
| :--- | :--- | :--- |
| **Architectural Decision Record** | ADR | A document used to capture and justify significant technical choices. ADRs serve as the project’s "logbook" to ensure transparency regarding the rationale behind protocol and standard adoption. |
| **Architecture and Reference Framework** | ARF | The reference architecture for the European Digital Identity Wallet ecosystem published by the European Commission in cooperation with the Member States. It defines roles, trust models, protocols and interoperability requirements for the ecosystem. |
| **Attestation Rulebook**| - | A document describing the governance, requirements and semantic interpretation of a specific attestation type, including how credential data maps to vocabulary terms and schemas. |
| **Authorised representative** | - | A person acting on behalf of the owner on the basis of an authorisation granted by the owner. |
| **Blueprint** | — | The high-level architecture and integration document (D4.1) describing the WE BUILD ecosystem, architectural patterns, interaction flows and governance model. 
| **Business Wallet Instance Attestation** | BWIA | A signed JWT-based data object issued by a Wallet Provider that attests the integrity, security properties, and compliance of a specific Business Wallet Unit (BWU) deployment, acting in the role of the TS3 Wallet Instance Attestation (WIA). |
| **Business Wallet Unit Attestation** | BWUA | The complete cryptographic attestation mechanism for a European Business Wallet (EBW) instance. Formally composed of the Business Wallet Instance Attestation (BWIA) and the Server Key Attestation (SKA). |
| **EAA Provider** | — | An entity that relies on authentic sources of information to issue attestations to a wallet. |
| **EBW Instance** | — | A unique deployment or installation of a European Business Wallet (EBW) solution, controlled by an Owner (legal person or economic operator). |
| **EBW Provider** | — | A Wallet Provider specifically authorized to issue and manage European Business Wallets (EBW). |
| **EBW Owner Identification Data** | EBWOID | A mandatory, stable, and minimal set of core identity attributes (primarily legal name and EUID or national register code) used to uniquely bootstrap and identify a legal person or economic operator within the EBW ecosystem. Unlike personal identification data, it represents the organization itself, not any individual representative. |
| **EBWOID Provider** | — | An entity responsible for verifying the identity of a legal person or economic operator and issuing EBW Owner Identification Data (EBWOID). |
| **Economic operator** | — | Any natural or legal person or public entity which offers products or services on the market; the primary user of the European Business Wallet. |
| **Electronic Attestation of Attributes** | EAA / QEAA / PuB-EAA | Digital credentials that prove specific attributes (e.g., professional qualifications, representation rights) with either qualified (QEAA) or public sector body-issued (PuB-EAA) or non-qualified (EAA) legal status. |
| **Electronic Identification, Authentication and Trust Services** | eIDAS / eIDAS 2.0 | The legal framework for electronic identification and trust services for electronic transactions in the European Single Market. |
| **European Business Wallet** | EBW | A wallet designed for economic operators or public sector bodies to manage business data such as mandates, electronic invoices, and administrative and professional documents and notifications. |
| **European Digital Identity Wallet** | EUDI Wallet | A mobile or cloud-based solution for natural persons to manage and share identity data. |
| **EUDIW Instance** | — | A specific deployment of an EUDI Wallet solution for a natural person. |
| <del>**Holder**</del> | — | See *Wallet User* instead. |
|  **Interoperability**| - | The ability of independently developed systems and components to exchange information and correctly interpret the exchanged data. |
| **Interoperability Testbed** | ITB | The automated testing environment used in WE BUILD to verify that implementations conform to the agreed specifications and remain interoperable. |
| <del>**Issuer**</del> | — | See *EAA Provider* instead. |
| **Large Scale Pilot** | LSP | A project funded by the European Commission to test the practical implementation of the EUDI Wallet framework across various cross-border use cases. |
| **Legal Person** | — | An entity (such as a corporation or public body) recognized by law as having rights and duties, distinguished from a natural person. |
| <del>**Legal Person Identification Data**</del> | LPID | See **EBW Owner Identification Data** instead. |
| **Level of Assurance** | LoA | A classification of the degree of confidence in the electronic identification of a natural person, a legal person, or a natural person representing a legal person. Recognised levels are: Low, Substantial, High. |
| **List of Trusted Lists** | LoTL | A list that references national or ecosystem Trusted Lists, allowing participants to discover and validate trusted entities. |
| **Natural Person** | — | An individual human being acting in their own capacity. |
| **Owner** | — | The legal person or economic operator that has legal control over and responsibility for an EBW Instance. |
| **Personal Identification Data** | PID | A mandatory set of core identity attributes issued by a Member State authority to uniquely identify a natural person at Level of Assurance (LoA) High. Used in the EBW ecosystem to onboard authorized representatives and bind their natural-person identity to organizational actions. |
| **PID Provider** | — | An entity responsible for verifying the identity of a natural person and issuing Personal Identification Data (PID). |
| **Qualified Electronic Registered Delivery Service** | QERDS | A secure communication channel that provides legal evidence of the handling of transmitted data. |
| **QERDS Delivery Agent** | — | A core functional component of the QERDS infrastructure that produces, consumes, and delivers encrypted transport packages while enforcing strict access control and registering formal evidence of submission or notification. |
| **QERDS Delivery Log** | — | A QERDS database or ledger component designed to ensure the secure long-term retention of registered transaction and delivery evidence, allowing stakeholders to audit delivery events and resolve disputes. |
| **QERDS Delivery Relay** | — | A secure transport routing service that handles the physical and cryptographic transmission of encrypted packages between different QERDS providers operating in a federated four-corner network model. |
| **Qualified Trust Service Provider** | QTSP | A regulated entity providing electronic trust services (e.g., signatures, seals, or delivery services) with full legal effect under eIDAS. |
| **Relying Party** | RP | An entity that requests and receives attestations from a wallet to verify specific attributes or identities. |
| **Selective Disclosure JSON Web Token** | SD-JWT | A format allowing holders to share only specific parts of a credential while keeping other data private. |
| **Server Key Attestation** | SKA | A cryptographic attestation that proves that the private keys used for credential binding are securely protected inside a cloud-hosted or organization-controlled hardware security module (HSM), acting as a server-side counterpart to the TS3 Key Attestation (KA)-|
| **Trust Framework** | — | The set of governance rules, standards, and trust infrastructure used to establish and verify trust relationships between ecosystem participants. |
| **Trusted List** | TL | A machine-readable list of trusted service providers or entities used to validate trust relationships within the ecosystem. |
| **European Unique Identifier** | EUID | The official unique identifier assigned to a wallet owner; or a similar identifier created under the Regulation. |
| <del>**Verifier**</del> | — | See *Relying Party* instead. |
| **Wallet Application** | — | The user-facing software component of a Wallet Solution providing the interface for managing credentials. |
| **Wallet Core Component(s)** | — | The technical module(s) of a Wallet Solution handling cryptographic operations and protocol implementations. |
| **Wallet Instance** | — | A specific operational instance of a wallet solution running on a device or cloud environment. |
| **Wallet Instance Attestation** | WIA | A short-lived, signed information object issued by a Wallet Provider that contains information about the Wallet Instance. It is device-bound and presented to PID or Attestation Providers to authenticate the instance, but it does not require a WSCD/WSCA for key management and does not contain revocation information. |
| **Wallet Owner** | - | The economic operator or public sector body that owns or has a right of use of the wallet and is accountable for its actions. |
| **Wallet Provider** | — | An organization that provides a Wallet Solution and manages its lifecycle. |
| **Wallet Secure Cryptographic Device / Application** | WSCD / WSCA | The hardware or software environment used to manage cryptographic keys securely within the wallet. |
| **Wallet Solution** | — | A specific implementation of a wallet consisting of a Wallet Application and Wallet Core Component(s). |
| **Wallet Type** | — | A classification of wallet implementations by where the wallet runs and where its keys are protected. Appendix E describes the three types used in this document: on-device, remote / server-side, and hybrid. |
| **Wallet Unit** | WU | The deployed wallet controlled by a Wallet User, which presents the Wallet Unit Attestation that describes it. Credentials are bound to keys the Wallet Unit controls in its WSCD / WSCA. CS-04 uses Wallet Unit (WU) for the natural person's wallet; the business counterpart is the Business Wallet Unit (BWU) in CS-05. |
| **Wallet Unit Attestation** | WUA | A signed information object issued by a Wallet Provider that describes the capabilities and security properties of a Wallet Unit (especially the WSCD/WSCA). It is device-bound and allows PID or Attestation Providers to verify compliance, bind credentials to the unit, and check for revocation. |
| **Wallet User** | — | The natural or legal person that controls and operates a wallet instance. |
| **WE BUILD** | — | The consortium and project focused on pioneering the European Business Wallet and EUDI Wallet use cases. |
| **WE BUILD Conformance Specifications** | WBCS | Detailed technical rules that operationalize architectural intent. Approval of a WBCS signifies a commitment from partners to implement those interfaces. |
