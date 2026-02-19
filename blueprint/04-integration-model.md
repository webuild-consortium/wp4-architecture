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
In WE BUILD, signature and seal integration will combine wallet-centric signing with QTSP-centric (remote) signing/sealing. The architecture distinguishes where the private key and the signature/seal creation device will reside and how documents will be presented and processed within the signature creation application. This enables the wallet to orchestrate the user experience while qualified operations remain anchored in QTSP-governed environments for remote signing and sealing.

### Wallet-centric signing model
In the wallet-centric model, the EUDI Wallet is the central component of the qualified electronic signature process. Three distinct signing processes will be supported, depending on where the signature creation application runs and where signature creation takes place. In the remote cases, the private key and SCD/QSCD will be remote (QTSP-governed), while in local cases, they will be under the user’s control (e.g., on-device or locally accessible token).

#### 1) Remote signing with external SCA  
The user will initiate signing in the wallet, but the signature creation application is external. The document (or a derived signature request) will be transmitted to the external SCA, where the content is displayed for review. The external SCA captures the user’s approval and then triggers the signing operation. The document/signature request will be forwarded to a remote signature creation device, which creates the signature and returns the result to the calling flow.

#### 2) Remote signing with local SCA (wallet as SCA)  
The user will initiate signing in the wallet and the wallet acts as the signature creation application. The document is displayed in the wallet so review and explicit consent take place inside the wallet experience. After consent, the wallet will submit the document/signature request to a remote signature creation device for signature creation. The result will be returned to the wallet for delivery to the relying party as part of the business transaction.

#### 3) Local signing  
The wallet will initiate signing and the full signature creation application experience remains on-device. The document is displayed in the wallet and the user provides explicit consent there. Signature creation is performed locally using a signature creation device integrated into the user’s smartphone, without invoking a remote signature creation device.

### QTSP-centric signing and sealing model
In the QTSP-centric model, the trust service provider remains the central authority responsible for execution and governance of the signing or sealing process. The cryptographic key material used for signature or seal creation will be generated, stored, and operated within infrastructure controlled by or on behalf of the QTSP, typically within secure hardware environments. From the perspective of the user or calling application, signing and sealing are remote: external components interact with the trust service through defined service interfaces, while the cryptographic operation is performed within the QTSP-controlled environment.

Within this architecture, the EUDI Wallet may act as the client-side orchestration component, primarily for user authentication, collecting user intent, and triggering a signing operation. However, it does not operate the signature creation environment, does not manage signing credentials, and does not assume the regulatory obligations of a trust service provider.

From a regulatory perspective, established trust boundaries are preserved. The QTSP remains responsible for identity binding, credential issuance, and compliance with applicable ETSI standards. Signature or seal creation data remains under controlled conditions consistent with the required assurance level. Activation mechanisms enforce the conditions required for advanced or qualified signatures, including sole control where applicable.

### CSC interoperability profile for remote signing/sealing
For all remote signing and sealing flows, CSC interoperability will be implemented using CSC API 2.2.0.0, CSC data model (DM) 1.0.0, and CSC data-model-bindings 1.0.0. This interoperability profile will expose remote signing/sealing via a standardized interface, while the underlying trust model and QTSP responsibilities remain unchanged.

### Organisational signing: individuals signing on behalf of a company
To support individuals signing on behalf of a company with full legal effect, the planned approach will reuse the wallet-centric and QTSP-centric models above. The wallet remains the user-facing control point for review and approval, while the QTSP will execute the qualified signing/sealing operation within its controlled environment. The relying party workflow will verify, bind, and validate the transaction and the resulting qualified signature/seal according to its policy and evidence model. WE BUILD will pilot this organisational signing pattern while preserving the QTSP trust boundary and reusing the same CSC-based interoperability profile for remote QSCD usage.

## Secure communication channel
To be authored by the QTSP group in consultation with the Architecture and Wallets groups. Explains the technical flows for usage of the qualified electronic registered delivery service (QERDS).
