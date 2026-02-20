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

==

The [WE BUILD Consortium Conformance Specification (CS)](https://github.com/webuild-consortium/wp4-architecture/blob/blueprint/updates-jan/conformance-specs/cs-01-credential-issuance.md) for high-assurance credential issuance defines the requirements that will be applied within the WE BUILD project to ensure that Wallet Units and Credential Issuers across the WE BUILD ecosystem interoperate reliably and consistently when issuing verifiable digital credentials, with strong security guarantees and privacy protections.


The WE BUILD ecosystem mainly supports two credential issuance models, which differ in which actor inititates the process: wallet-initiated issuance and issuer-initiated-issuance In both cases, if the credential cannot be issued immediately, a deferred issuance mechanism is applied. In such case, the wallet will automatically make periodic retries until the credential is successfully issued or until it receives an unrecoverable error.

### Wallet-initiated issuance

This issuance flow is initiated by the wallet user:

1. The user opens their wallet and selects the credential type to be issued (for example, a PID or a QEAA).
2. The wallet connects with the corresponding issuer and requests the credential.
3. The wallet user authenticates with the issuer, following the procedure specified by the issuer itself.
4. The issuer requests the user's consent from the user to issue the credential and send it to their wallet.
5. The issuer generates the credential and delivers it to the wallet.
6. The wallet verifies the authenticity of the credential and stores it. From this point, the wallet user becomes responsible for managing the issued credential.

```mermaid
sequenceDiagram
participant User
participant Wallet
participant Issuer

User->>Wallet:Selects the credential type
Wallet-->>Issuer: Requests the credential
Issuer->>User: Requests authentication
User->>Issuer: Authentication
Issuer->>User: Requests consent
User->>Issuer: Gives consent
Issuer-->>Issuer: Generates the credential
Issuer-->>Wallet: Sends the credential
Wallet-->>Wallet: Validates the credential
Wallet-->>Wallet: Stores the credential 
User->>Wallet: Accesses the credential
### Issuer-initiated issuance

This issuance flow is initiated by the issuer:

1. The user interacts with the issuer (for example, during a digital onboarding process).
2. The issuer prepares one or more credentials.
3. The issuer offers these credentials to the wallet user. This can be done in several ways, both same-device and cross-device:
- By displaying a QR code that the user shall scan with their wallet.
- By sending a link to the wallet.
4. The wallet displays the offer and requess confirmation from the user.
5. The wallet user authenticates with the issuer, following the procedure specified by the issuer itself.
6. The issuer requests the user's consent from the user to issue the credential and send it to their wallet.
7. The issuer generates the credential and delivers it to the wallet.
8. The wallet verifies the authenticity of the credential and stores it. From this point, the wallet user becomes responsible for managing the issued credential.

```mermaid
sequenceDiagram
participant User
participant Wallet
participant Issuer

User->>Issuer: Interacts digitally
Issuer-->>Issuer: Prepares the credential
Issuer->>User: Offers the credential diplaying a QR code
User->>Wallet: Scans the QR code
Wallet->>User: Requests confirmation
User->>Wallet: Accepts the offer
Wallet-->>Issuer: Requests the credential
Issuer->>User: Requests authentication
User->>Issuer: Authenticates
Issuer->>User: Requests consent
User->>Issuer: Gives consent
Issuer-->>Issuer: Generates the credential
Issuer-->>Wallet: Sends the credential
Wallet-->>Wallet: Validates the credential
Wallet-->>Wallet: Stores the credential
User->>Wallet: Accesses the credential

## Interaction Pattern: Attestation Presentation (Receiving) 
To be authored by Architecture and Wallets. This is the "Receiving" flow for Relying Parties, detailing how they request and receive verified attributes under the user's sole control using OpenID4VP. 

The [WE BUILD Conformance Specification for Credential Presentation](https://github.com/webuild-consortium/wp4-architecture/blob/blueprint/updates-jan/conformance-specs/cs-02-credential-presentation.md) describes how Wallet Units (WU) and Verifiers interoperate within the WE BUILD ecosystem. It covers presentation (request and response flows), interfaces between wallets and verifiers as well as security, privacy and interoperability requirements and same‑device and cross‑device invocation patterns

## Signature and Seal Integration 
To be authored by Group 6 (QTSP). Explains the technical flows for wallet-centric and QTSP-centric (remote) signing/sealing, allowing individuals to sign on behalf of a company with full legal effect

## Secure communication channel
To be authored by the QTSP group in consultation with the Architecture and Wallets groups. Explains the technical flows for usage of the qualified electronic registered delivery service (QERDS).
