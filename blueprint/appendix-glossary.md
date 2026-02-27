# Appendix A – Glossary

## Terms and Definitions

This appendix defines the key terms, regulatory frameworks, and technical specifications utilised throughout the WE BUILD ecosystem.

While this document avoids abbreviations as much as possible, commonly used abbreviations are included for reference.

| Term | Abbreviation | Definition |
| :--- | :--- | :--- |
| **Architectural Decision Record** | ADR | A document used to capture and justify significant technical choices. ADRs serve as the project’s "logbook" to ensure transparency regarding the rationale behind protocol and standard adoption. |
| **Architecture and Reference Framework** | ARF | The official document provided by the European Commission (EDICG) that specifies the functionalities and design principles of the EUDI ecosystem. |
| **Blueprint** | — | The primary strategic document describing the high-level architectural patterns and the "big picture" of how the WE BUILD system components integrate. |
| **Business Wallet Unit Attestation** | BWUA | A specific type of Wallet Unit Attestation issued for a European Business Wallet (EBW) instance. |
| **EAA Provider** | — | An entity that relies on authentic sources of information to issue attestations to a wallet. |
| **EBW Instance** | — | A unique deployment or installation of a European Business Wallet (EBW) solution, controlled by an Owner (legal person or economic operator). |
| **EBW Provider** | — | A Wallet Provider specifically authorized to issue and manage European Business Wallets (EBW). |
| **EBWOID Provider** | — | An entity responsible for verifying the identity of a legal person or economic operator and issuing EBW Owner Identification Data (EBWOID). |
| **EBW Owner Identification Data** | EBWOID | A digital set of attributes that uniquely identifies a legal entity (the business equivalent of a PID). |
| **Economic operator** | — | Any natural or legal person or public entity which offers products or services on the market; the primary user of the European Business Wallet. |
| **Electronic Attribute Attestation** | EAA / QEAA / PuB-EAA | Digital credentials that prove specific attributes (e.g., professional qualifications, representation rights) with either qualified (QEAA) or public sector body-issued (PuB-EAA) or non-qualified (EAA) legal status. |
| **Electronic Identification, Authentication and Trust Services** | eIDAS / eIDAS 2.0 | The legal framework for electronic identification and trust services for electronic transactions in the European Single Market. |
| **European Business Wallet** | EBW | A wallet designed for economic operators or public sector bodies to manage business data such as mandates, electronic invoices, and administrative and professional documents and notifications. |
| **European Digital Identity Wallet** | EUDI Wallet | A mobile or cloud-based solution for natural persons to manage and share identity data. |
| **EUDIW Instance** | — | A specific deployment of an EUDI Wallet solution for a natural person. |
| <del>**Holder**</del> | — | See *Wallet User* instead. |
| **Interoperability Testbed** | ITB | The primary gatekeeper and automated testing infrastructure used to prove that a technical solution is ready for real-world piloting. |
| <del>**Issuer**</del> | — | See *EAA Provider* instead. |
| **Large Scale Pilot** | LSP | A project funded by the European Commission to test the practical implementation of the EUDI Wallet framework across various cross-border use cases. |
| **Legal Person** | — | An entity (such as a corporation or public body) recognized by law as having rights and duties, distinguished from a natural person. |
| <del>**Legal Person Identification Data**</del> | LPID | See **EBW Owner Identification Data** instead. |
| **Level of Assurance** | LoA | A classification of the degree of confidence in the electronic identification of a natural person, a legal person, or a natural person representing a legal person. Recognised levels are: Low, Substantial, High. |
| **Natural Person** | — | An individual human being acting in their own capacity. |
| **Owner** | — | The legal person or economic operator that has legal control over and responsibility for an EBW Instance. |
| **Personal Identification Data** | PID | A mandatory set of attributes issued to a natural person to uniquely identify them at Level of Assurance (LoA) High. |
| **PID Provider** | — | An entity responsible for verifying the identity of a natural person and issuing Personal Identification Data (PID). |
| **Qualified Electronic Registered Delivery Service** | QERDS | A secure communication channel that provides legal evidence of the handling of transmitted data. |
| **Qualified Trust Service Provider** | QTSP | A regulated entity providing electronic trust services (e.g., signatures, seals, or delivery services) with full legal effect under eIDAS. |
| **Relying Party** | RP | An entity that requests and receives attestations from a wallet to verify specific attributes or identities. |
| **Selective Disclosure JSON Web Token** | SD-JWT | A format allowing holders to share only specific parts of a credential while keeping other data private. |
| **Trust Framework** | — | The system of rules, standards, and trust lists (based on ETSI TS 119604/119612) that ensure all actors in the ecosystem are valid and compliant. |
| <del>**Verifier**</del> | — | See *Relying Party* instead. |
| **Wallet Application** | — | The user-facing software component of a Wallet Solution providing the interface for managing credentials. |
| **Wallet Core Component(s)** | — | The technical module(s) of a Wallet Solution handling cryptographic operations and protocol implementations. |
| **Wallet Instance** | — | A unique deployment or installation of a Wallet Solution on a device or cloud environment. |
| **Wallet Instance Attestation** | WIA | A short-lived, signed information object issued by a Wallet Provider that contains information about the Wallet Instance. It is device-bound and presented to PID or Attestation Providers to authenticate the instance, but it does not require a WSCD/WSCA for key management and does not contain revocation information. |
| **Wallet Provider** | — | An organization that provides a Wallet Solution and manages its lifecycle. |
| **Wallet Secure Cryptographic Device / Application** | WSCD / WSCA | The hardware or software environment used to manage cryptographic keys securely within the wallet. |
| **Wallet Solution** | — | A specific implementation of a wallet consisting of a Wallet Application and Wallet Core Component(s). |
| **Wallet Unit Attestation** | WUA | A signed information object issued by a Wallet Provider that describes the capabilities and security properties of a Wallet Unit (especially the WSCD/WSCA). It is device-bound and allows PID or Attestation Providers to verify compliance, bind credentials to the unit, and check for revocation. |
| **Wallet User** | — | The natural or legal person that controls the wallet. |
| **WE BUILD** | — | The consortium and project focused on pioneering the European Business Wallet and EUDI Wallet use cases. |
| **WE BUILD Conformance Specifications** | WBCS | Detailed technical rules that operationalize architectural intent. Approval of a WBCS signifies a commitment from partners to implement those interfaces. |
