# WE BUILD - Conformance Specification: Issuance of Relying Party Access and Registration Certificates

Version 1.0
Date: 25 Août 2026
Original Author: Jilles Van Oossanen
Modified Proposal by : François CHASSERY

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language and Terminology](#3-normative-language-and-terminology)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
  - [5.1 ACME Resource Model](#51-acme-resource-model)
  - [5.2 WRPAC Identifier Type](#52-wrpac-identifier-type)
  - [5.3 EBW-based Account Binding](#53-ebw-based-account-binding)
- [6. High-level Flows](#6-high-level-flows)
  - [6.1 Automated Issuance Process](#61-automated-issuance-process)
  - [6.2 Direct Isssuance Process](#62-direct-issuance-process)
 - [7. Normative Requirements](#7-normative-requirements)
  - [7.1 Common Requirements](#71-common-requirements)
  - [7.2 ACME Server (CA / RA)](#72-acme-server-ca--ra)
  - [7.3 ACME Client (WRP / EBW)](#73-acme-client-wrp--ebw)
  - [7.4 Certificate Profile](#74-certificate-profile)
  - [7.5 Certificate Transparency](#75-certificate-transparency)
  - [7.6 Revocation](#76-revocation)
  - [7.7 Trusted List Integration](#77-trusted-list-integration)
  - [7.8 WE BUILD RP Lists](#78-we-build-rp-lists)
  - [7.9 IANA Considerations](#79-iana-considerations)
- [8. Interface Definitions](#8-interface-definitions)
  - [8.1 ACME Directory](#81-acme-directory)
  - [8.2 Account Management with EBW/EBWOID](#82-account-management-with-ebwebwoid)
  - [8.3 Order Lifecycle](#83-order-lifecycle)
  - [8.4 Finalize and Certificate](#85-finalize-and-certificate)
  - [8.5 Revocation](#86-revocation)
- [9. Conformance](#9-conformance)
- [References](#references)

---

# 1. Introduction

This document defines the **WE BUILD Consortium Conformance Specification (CS)** for the issuance of Wallet-Relying Party Access Certificates (WRPACs) and, where applicable, Wallet-Relying Party Registration Certificates (WRPRCs) within the European Digital Identity Wallet ecosystem, and proposes either an automated issuance process using a protocol based on the Automatic Certificate Management Environment (ACME) as defined in RFC 8555 [1], or a direct issuance process relying on Web interfaces, electronic identifications means and digital signature.

It profiles:

* Commission Implementing Regulation (EU) 2025/848 [2], in particular Article 7, Annex I, Annex IV, and Annex V (the latter for optional WRPRC co-issuance)
* ETSI TS 119 411-8 v1.1.1 (2025-10) [3] — Access Certificate Policy for EUDI Wallet Relying Parties
* ETSI TS 119 475 v1.2.1 (2026-03) [4] — Relying party attributes supporting EUDI Wallet user's authorisation decisions, in particular Annex D, Use Case 1 (Integrated model)
* WE BUILD WP4 Architecture Blueprint [5] — RPAC/RPRC documentation and issuance process
* IETF RFC 8555 [1] — Automatic Certificate Management Environment (ACME)

This specification uses the ACME protocol as a **technical implementation** for automation of the integrated issuance model described in ETSI TS 119 475 v1.2.1 Annex D, Use Case 1 [4], as adopted by the WE BUILD Blueprint [5]. Section 9 provides an explicit mapping between the WE BUILD Blueprint issuance workflow and the ACME protocol operations.

An alternative issuance process is described to allow WRP to obtain WRPC without using EBW nor ACME client.

This specification focuses **only on direct issuance** of WRPACs to registered Wallet-Relying Parties. The ACME flow is preceded with EBW-based authentication and EBWOID verification to align with the Blueprint's requirements for user authentication via European Business Wallets. This document is used to build the WE BUILD Interoperability Test Bed Plus (ITB+) [6].

> [!IMPORTANT]
> CS-RPAC_01: This specification is intended for **interoperability testing only**, not for production deployment. Its purpose is to validate the technical feasibility of ACME-based WRPAC issuance and to establish interoperability between independent implementations. Production deployments will require additional security hardening, policy alignment, and conformity assessment beyond the scope of this document.

> [!NOTE]
> CS-RPAC_02: CIR (EU) 2025/848 [2] was adopted on 6 May 2025 and **applies from 24 December 2026**. Requirements in this specification that derive from CIR (EU) 2025/848 are therefore drafted in anticipation of that date of application.

# 2. Scope

This specification defines:

* An ACME protocol profile (based on RFC 8555) for the automated issuance of X.509-based Wallet-Relying Party Access Certificates, aligned with the WE BUILD Blueprint issuance process
* Support for multi-instance issuance, enabling a single WRP to obtain separate WRPACs for multiple Relying Party Instances per the EUDI Wallet ARF v2.8 [15]
* Requirements for:
    * ACME Servers operated by TSP acting as Certificate Authorities and Registration Authorities)
    * ACME Clients (Wallet-Relying Parties)
* Protocol flows for:
    * Optional WRPRC issuance after registration of an authorized WRP
    * Direct WRPAC issuance to an authorized WRP
    * Multi-instance issuance (one WRPAC per Relying Party Instance)
    * Certificate revocation

This specification does **not** cover:

* Intermediary or multi-party issuance
* Standalone WRPRC issuance 
* Production deployment requirements (conformity assessment, CAB audits, national policy extensions)
* Proximity use cases for certificate presentation

# 3. Normative Language and Terminology

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are to be interpreted as commonly used in technical specifications.

The following terminology applies throughout this specification:

* **WRPAC** — Wallet-Relying Party Access Certificate. This specification uses the term **WRPAC** (matching ETSI TS 119 475 v1.2.1 [4] and CIR (EU) 2025/848 [2]). The abbreviation **RPAC** as used in some WE BUILD Blueprint [5] and ARF [15] discussion documents is synonymous.
* **WRPRC** — Wallet-Relying Party Registration Certificate. The abbreviation **RPRC** used elsewhere is synonymous.
* **EBW** — European Business Wallet.
* **EUDIW** — European Digital Identity Wallet.
* **RP** — Relying Party; in this specification usually **WRP** (Wallet-Relying Party).
* **RA / CA / TSP** — Registration Authority, Certificate Authority, Trust Service Provider.
* **CP** — Certification Policy for **RPAC**
* **EAA** — Electronic Attestation of Attributes.
* **EBWOID** — European Business Wallet Organisational Identification Data, as defined in the WE BUILD EBWOID Attestation Rulebook [20]. Carries the organisation's unique identifier (`id`) and official name (`name`).
* **Authorised representative** or **RP representative**: Individual acting on behalf of the RP
* **Legal Representative** or **LR**: a natural person authorized by law or record registration to act on behalf of a legal person.
* **Power of Attorney** or **POA**: written document digitally signed by the RL with an advanced or qualified signature to establish that RP representative is appointed to act on behalf of the RP.
* **RP’s BACKEND**: IS of RP
* **RP’s FRONTEND**: ACME client of RP
* **TRUST LIST**: Trusted registry of accredited Relying Parties

# 4. Roles and Components

This specification uses the following roles, mapped to both the ACME protocol and the WE BUILD Blueprint:

| ACME Role | Blueprint Role | Description |
|---|---|---|
| **User + EID** | The RP representative using an Electronic Identification Means of level substantial or higher as per eIDAS regulation. The EID needs to be completed by POA in this specification in the aim of user-authentication and proof of authority for account creation|
| **User + EBW** | The RP representative using an European Business Wallet. The EBW plays a role in this specification of a user-authentication authority for EBW-based External Account Binding per RFC 8555 §7.3.4 [1]. |
| **ACME Server** | **RA + CA** | The combined Registration Authority and Certificate Authority. For automated issuance process, the RA function handles identity verification, EBWOID validation, and RP list checks. The CA function handles certificate generation and signing. These MAY be separate systems behind a single ACME endpoint. |
|**ACME CLIENT** **RP’s FRONTEND**| — | host or invocation environment for the ACME Client software |
| — | **Mock Registrar (RA/TSP)** | In the WE BUILD pilot, participating TSPs acting as mock Registrars maintain the Lists of authorised RPs. This role is functionally equivalent to the Member State Registrar in the production eIDAS ecosystem. In production, this function is performed by the national Registrar of the Member State concerned per the eIDAS framework. |
| **Wallet Unit** | — | The EUDI/Business Wallet that verifies WRPACs during RP authentication. Not involved in issuance. |

Detailed role descriptions:

* **User (RP Representative or authorised representative):** A natural person operating on behalf of the Wallet-Relying Party via the organisation's EBW, or on interfaces of RPC Provider. 
When WRP is using an EBW, User  Authenticates via the EBW, which presents the organisation's EBWOID attestation (an EAA). Authorisation to obtain a certificate for the WRP results from control of the organisation's EBW; this profile does not require a separate Power of Attorney or representative attestation.
When the WRP does not use EBW, User Authenticates via its EID, and presents its POA. Authorisation to obtain a certificate for the WRP results from control of the POA together with the identity of the User. 
* **European Business Wallet (EBW):** The wallet application used to authenticate to the RA in the automated issuance process.
* **Registration Authority (RA):** The TSP component that verifies the organisation's identity, requests additional attributes for the RPRC, and checks the RP's presence in the authorised RP lists. 
* **Certificate Authority (CA):** The TSP component that generates and signs WRPAC and WRPRC certificates. Implemented as the ACME Server's certificate issuance backend in the automated issuance process.
* **Mock Registrar:** In the WE BUILD pilot, participating TSPs acting as mock Registrars establish and maintain the Lists of authorized Relying Parties. These lists serve as the functional equivalent of the national register of wallet-relying parties per the Blueprint [5] MVP governance model. The RA checks these lists during authorization. During ITB+ conformance testing, the WE BUILD RP List is served by the mock Registrar; in production, by the national Registrar of the Member State concerned.

# 5. Protocol Overview

The WE BUILD WRPAC automated issuance protocol uses the standard ACME framework (RFC 8555) where domain-control challenge will be disabled, in order to implement the integrated issuance model described in ETSI TS 119 475 v1.2.1 Annex D, Use Case 1 [4] as adopted by the WE BUILD Blueprint [5].

The key adaptations are:

* ** External Account Binding (EAB)**: The EAB binds the ACME account to the credentials supplied to RP’s EBW.
EBW is REQUIRED for EAB issuance: The EBW presents the organisation's EBWOID (EAA) and identifies the authorised representative.
Trust List verification SHALL occur before EAB issuance. 
* **RA **: The RA function validates the EBWOID, the organisation's identity, and RP list membership, and delivers RP’s ACME credentials. 
* **Multi-instance issuance**: a single WRP (`wrp-id`) MAY obtain multiple WRPACs, one per Relying Party Instance. Each instance is identified by an optional `instanceId` in the order (see §5.2).
* * **Certificate profile**: the issued certificate is an X.509 v3 WRPAC conforming to CIR 2025/848 Annex IV and ETSI TS 119 411-8 v1.1.1 [3], with attribute content as specified in ETSI TS 119 475 v1.2.1 clause 5 [4].
* **Certificate Transparency**: the ACME Server logs all issued certificates per RFC 9162 [7] (see §7.5 for deployment guidance).
* **ACME Challenge**: this challenge is not used and replaced by an internal control by CA that the DN of RPAC contains EBWOID without any change. 

All ACME messages are JSON payloads signed via JWS (RFC 7515 [8]), using JWK Thumbprints as specified in RFC 7638 [17], transported over HTTPS.

> [!NOTE]
> CS-RPAC_03: The choice of ACME provides a proven, standardised, and automatable protocol for automated certificate lifecycle management. It implements the integrated issuance workflow described in ETSI TS 119 475 v1.2.1 Annex D, Use Case 1 (see Section 9) while enabling interoperability testing with off-the-shelf ACME tooling. The RA functions defined in the Blueprint may be encapsulated within the ACME Server.
> CS-RPAC_04: The choice of keeping standard ACME protocol but adding wrp-identifier will avoid to use a specific EWB for RP, and leave opened the opportunity of a complete ID and mandate verification by RA in the future.
>CS-RPAC_05: In the context of automated issuance for WEBUILD, RA will presume that the Id of the RP’s representative is true without performing a true identity verification conform to NCP Policy.
>CS-RPAC_06: In the context of automated issuance for WEBUILD, RA will consider that the authorised representative has an implicit mandate for requesting an NCP certificate.

## 5.1 ACME Resource Model

This profile follows the standard ACME resource model defined in RFC 8555 §7.1 [1]:

```
directory
    |
    +--> newNonce
    |
    +-----+-----+-----+-----+--------+
    |     |     |     |     |        |
    V     V     V     V     V        V
newAccount  newOrder  revokeCert  keyChange
    |           |
    V           V
  account     order ---+--> finalize (URL)
                       +--> certificate (URL)              
              
```

This profile follows RFC 8555 with the extensions defined in §5.2, §5.3. except that it intentionally replaces domain control validation with organisation control validation performed during EAB provisioning. Authorization is performed during EAB provisioning and account creation.

## 5.2 WRPAC Identifier Type

**Type**: `wrp-id`

**Value**: the WRP's unique identifier as it appears in the WE BUILD RP Lists and in RP’s EBWOID. For interoperability testing, the identifier format is defined by the mock Registrar. In the production eIDAS ecosystem, this would use CIR 2025/848 Annex I identifiers (EUID per CIR (EU) 2021/1042, LEI per CIR (EU) 2022/1860, National Trade Register numbers, or VAT identification numbers).

**Example:**

```json
{
  "type": "wrp-id",
  "value": "NLKVK.12345678"
}
```

**Multi-instance issuance**: A single WRP identified by one `wrp-id` value MAY obtain multiple WRPACs, one per Relying Party Instance, in accordance with the Relying Party Instance model described in the EUDI Wallet ARF v2.8 [15]. Each order MAY include an optional `instanceId` string that uniquely identifies the specific Relying Party Instance within the WRP's deployment. When `instanceId` is provided:

* If multi issuance is advertised the ACME Server MUST verify that the `instanceId` is distinct from all other currently valid WRPACs issued to the same `wrp-id`.
* If multi issuance is advertised the issued WRPAC MUST include the `instanceId` as an Organisational Unit in the Subject's Distinguished Name.

## 5.3 EBW-based Account Binding

ACME External Account Binding (RFC 8555 §7.3.4 [1]) will rely on EBW authentication completed by a control of presence of the RP in the Trust List. This implements Blueprint steps 1-3.

**Mechanism:**

1. The EBW authenticates to the RA, presenting the organisation's EBWOID attestation (EAA).
2. The RA validates the EBWOID and verifies the organisation's identity.
3. The RA registers the authorised representative as a subscriber within the meaning of ETSI EN 319 411-1 §5.4.2. For WE BUILD interoperability testing, mandate validation is presumed based on control of the organisation's EBW and is not independently verified.
4. The RA issues EAB credentials (Key ID + HMAC Key) together with a registration URL and supply them to RP’s EBW.
5. The ACME Client uses these EAB credentials during `newAccount`.

**EAB in newAccount:**

Per RFC 8555 §7.3.4 [1], the `externalAccountBinding` value is a flattened JWS whose payload is the ACME account key in JWK form, and whose protected header carries `alg` (a MAC algorithm), `kid` (the CA-issued EAB Key Identifier), and `url`.

```json
{
  "termsOfServiceAgreed": true,
  "contact": ["mailto:representative@rp.example"],
  "externalAccountBinding": {
    "protected": "<JWS header with alg (MAC), kid (EAB Key ID), and url>",
    "payload": "<ACME account public key in JWK form>",
    "signature": "<HMAC signature>"
  }
}
```

> [!NOTE]
> CS-RPAC_07: **[MVP]** For initial interoperability testing, EBW authentication MAY be simulated. EAB credentials are pre-provisioned by the RA/TSP after out-of-band identity verification. **[MVP+]** Future iterations MUST implement the full EBW-based OID4VP authentication flow for EAB provisioning, including presentation of the organisation's EBWOID (EAA) via OID4VP. Implementations declaring MVP+ conformance MUST support the full OID4VP-based EBW authentication flow.

# 6. High-level Flows

## 6.1 Automated Issuance Process

### 6.1.1 Directory Discovery

1. The ACME Client fetches the directory document via HTTPS GET.
2. The directory includes metadata: `externalAccountRequired: true`

### 6.1.2 Account Creation with EBW Authentication

**Pre-ACME phase (Blueprint steps 1-3):**

1. The RP representative connects to the TSP's RA portal/service via the organisation's EBW.
2. **[MVP+]** The RA initiates an OID4VP request to the EBW, requesting the organisation's EBWOID (EAA). **[MVP]** This step MAY be performed out-of-band.
3. The EBW presents the EBWOID.
4. The RA validates the EBWOID and verifies the organisation's identity.
5. The RA validates the presence of RP in Trust Lists (*Blueprint step 5: RP list check.*)
6. Optionally (Blueprint step 4): **[MVP+]** the RA collects  entitlements or types of entitlements in Trust Lists for WRPRC production. **[MVP]** RA MAY collects this information from RP out of band.
7. Optionally CA issues RPRC.
8. The RA issues EAB credentials to the EBW together with the optional RPRC if produced.

**ACME phase:**

8. The ACME Client generates an account key pair. 
9. The ACME Client sends `newAccount` with the EAB binding.
10. The ACME Server validates the EAB and creates the account.

### 6.1.3 Order Creation

1. The ACME Client sends `newOrder` whose “identifier” value is ‘wrp-id’ and instanceID as an attribute

2. The ACME Server MUST validate wrp-id coherence with EAB. 

2. The ACME Server creates the order in `pending` state(“201” created response) and returns `finalize` URL.
3. For multi-instance issuance: the ACME Server MAY verify that the `instanceId` (if provided) is not already in use by a currently valid WRPAC for the same `wrp-id`.


### 6.1.4 Order Finalization

*Blueprint steps 6-9: order, issue, transmit, notify.*

1. **MVP+** The RP’s backend generates a certificate key pair and CSR and pass it to the ACME Client **MVP** The ACME Client generates a certificate key pair and CSR. Per §7.3 item 4, RP MUST generate a distinct key pair for each Relying Party Instance.
2. The ACME Client sends the CSR to the `finalize` URL.
3. The ACME Server (RA) validates.
4. The CA submits a pre-certificate to CT logs and obtains SCTs.
5. the ACME Server (CA) generates WRPAC
6. The order transitions to `valid` with a `certificate` URL.
7. The ACME Server MAY send out-of-band notification to the RP representative.

### 6.1.5 Certificate Download

*Blueprint steps 10-11: authenticate + retrieve.*

1. The ACME Client sends POST-as-GET to the `certificate` URL (authenticated via account key bound to EBW).
2. The ACME Server returns the PEM certificate chain.

### 6.1.6 Certificate Revocation

1. Client-initiated: `revokeCert` request.
2. Server-initiated: upon RP removal from the RP List, or upon revocation of a specific Relying Party Instance.
3. For multi-instance deployments: revocation of one instance's WRPAC MUST NOT affect WRPACs issued to other instances of the same WRP.

## 6.2 Direct Issuance Process

### 6.2.1 Account Creation with EID Authentication

**Registration phase (Blueprint steps 1-3):**

1.	The User connects to the TSP's RA portal/service.
2.	The User fills in RP identification information (i.e. Company Name, Organisation Identifier, address and points of contact).
3.	The User registers himself as the Authorised Representative
4.	The User uploads WRP evidences (proof of existence or registration, depending on the RP’s country regulation, and the POA)

### 6.2.2 Order Creation

1.	The User describes the certificate receiver.
2.	The User fills in a RPAC certificate application
3.	Optionally the User fills in a RPRC certificate application.
4.	The user set a complex password for certificate retrieval.

### 6.2.3 Order Validation

1.	The RA validates the RP Identifier and verifies the organisation's identity.
2.	The RA validates the presence of RP in Trust Lists (*Blueprint step 5: RP list check.*)
3.	Optionally (Blueprint step 4): **[MVP+]** the RA collects  entitlements or types of entitlements in Trust Lists for WRPRC production. **[MVP]** RA MAY collects this information from RP out of band.

### 6.2.4 Certificate Issuance

*Blueprint steps 10-11: authenticate + retrieve.*

1.	Optionally CA issues RPRC.
2.	The CA issues RPAC as a PKCS#12 enciphered by the password selected at step 5.
3.	The RA sends the RPAC together with the optional RPRC if produced by e-mail to the certificate receiver.
4.	The RA send to the certificate receiver its revocation credentials and procedure.

### 6.2.5 Certificate Revocation

1.	Certificate receiver may use its revocation credentials to revoke RPAC according to RPC issuer procedure.

> [!NOTE]
> CS-RPAC_08: RPRC can be seen as a structured export of registration data, for instance formatted as a signed JWT. It seems then opportune to issue these just at the end of registration steps that check the content of the Trust List.
> CS-RPAC_09: Renewal is out of scope of this specification; implementations are only required to support initial issuance and revocation.

# 7. Normative Requirements

## 7.1 Common Requirements

Both ACME Client and ACME Server **MUST**:

1. Implement the ACME protocol per RFC 8555 [1].
2. Use HTTPS for all communication.
3. Use JWS (RFC 7515 [8]) for all request payloads, with JWK Thumbprints computed per RFC 7638 [17] where required by ACME.
4. Implement nonce-based replay protection.

## 7.2 CA / RA
###7.2.1 RA
1.**MVP+** RA MUST authenticate RP and authorised representative through OID4VP protocol; **MVP** SHOULD authenticate RP and authorised representative through OID4VP protocol.
2. RA MUST verify WRP presence in the WE BUILD RP Lists before EAB credentials issuance (Blueprint step 5).

###7.2.2 ACME Server
The ACME Server **MUST**:

1. Publish an ACME directory at a well-known URL (see §7.9 for IANA considerations).
2. Require EAB for all accounts (RFC 8555 §7.3.4 [1]).
3. Reject authorization if the `wrp-id` does not match with the EBWOID bound to the EAB (see item 9).
4. Issue WRPACs exclusively to authorized WRPs.
5. Support the order state transitions defined in RFC 8555 §7.1.6 "Status Changes" [1].
6. Support `revokeCert`.
7. Accept instanceId when multi-instance support is advertised

The ACME Server **SHOULD**:

1. Send out-of-band notification when certificates are ready (Blueprint step 9).
2. Support `keyChange`.

## 7.3 ACME Client (WRP / EBW)

The ACME Client **MUST**:

1. Perform directory discovery.
2. Support EAB using credentials obtained from the RA after registration.
3. Supply a distinct key pair per Relying Party Instance and supply valid CSRs per §7.4. For single-instance issuance, a single key pair applies; for multi-instance issuance, a distinct certificate request including a distinct key pair MUST be post for each `instanceId`. This is the single normative key-separation rule applied by both the Client and the Server.
4. Validate the returned certificate chain.
5. Support `revokeCert`.

The ACME Client **SHOULD**:

2. Include an `instanceId` as one ‘identifier’ in orders for multi-instance deployments.

## 7.4 Certificate Profile

Issued WRPACs **MUST**:

1. Be X.509 v3 public-key certificates conforming to RFC 5280 [10].
2. Comply with ETSI TS 119 411-8 v1.1.1 [3] (Access Certificate Policy for EUDI Wallet Relying Parties), which in turn applies the NCP policy as specified in ETSI EN 319 411-1 v1.5.1 [12] and the WRPAC-specific policy identifiers `NCP-n-eudiwrp` (natural person) and `NCP-l-eudiwrp` (legal person).
3. Contain the WRP's legal name in the Subject field (CIR 2025/848 Annex I point 1 [2]).
4. Contain a user-friendly name where applicable (Annex I point 2).
5. Contain one unique WRP identifier (Annex I point 3), listed in the CP among EUID, LEI, National Trade Register number, or VAT identification number.
6. Include a certificate policy OID (Annex IV).
7. Include certification path information (URI).
8. Include a SAN extension containing contact information of RP as described in ETSI TS 119411-8 (6.6.1-07)
9. Include registration information per Annex I points 1, 2, and 8.
10. Express attribute content (e.g. `organizationIdentifier`, semantic identifiers) using the Subject DN and certificate-extension attributes defined in ETSI EN 319 412-1 [18] and ETSI TS 119 475 v1.2.1 clause 5 [4].
11. Conform to ETSI TS 119 475 v1.2.1 [4].
12. Use RSA (min. 3072 bits), ECDSA (P-256 or P-384), SHA-256 or stronger.
13. Have a validity period of **one year** from the date of issuance. Shorter validity periods are NOT used in WE BUILD interoperability testing.
14. Set Key Usage value at Digital Signature.
### 7.4.1 Subject Name Construction

SERIAL NUMBER (2.5.4.5)= 
Unique number calculated by CA to guarantee certificate unicity
CN =
“Friendly name”, either Company Name or Trade Name, easily understandable by end user
OU=
Optional intanceID
2.5.4.97 (organisation identifier)=
Wrp-id
O=
Organisation name
C=
Country

For instance:

1 CN=FICTIVE RELYING PARTY,
2 OU=Unit 01,
3 organizationIdentifier=NTRFR.123456789,
4 O=FICTIVE RELYING PARTY SAS,
5 C=FR


> [!NOTE]
> CS-RPAC_10: For interoperability testing, implementations SHOULD support both RSA and ECDSA. NCP as defined in ETSI EN 319 411-1 v1.5.1 [12] is the baseline policy level, with the WRPAC-specific extensions of TS 119 411-8 v1.1.1 [3] applied on top. The one-year validity period applies uniformly in the WE BUILD ITB+ test environment.

> [!NOTE]
> CS-RPAC_11: WRPACs are X.509 public-key certificates; they are not X.509 Attribute Certificates. Attribute content in WRPACs is expressed through public-key certificate extensions and ETSI-defined Subject DN attributes (ETSI EN 319 412 series [18], ETSI TS 119 475 v1.2.1 clause 5 [4]). The Attribute Certificate profile defined in RFC 5755 is therefore not applicable to WRPACs and is not used in this specification.

## 7.5 Certificate Transparency

The ACME Server **MUST** log all WRPACs in CT logs and embed SCTs.

> [!NOTE]
> CS-RPAC_12: RFC 9162 [7] ("Certificate Transparency Version 2.0", Experimental, December 2021) is the current IETF specification for CT and obsoletes RFC 6962. However, virtually all production CT log operators and browser CT policies currently implement RFC 6962. For interoperability testing in WE BUILD ITB+, implementations MAY use test CT logs and MAY rely on RFC 6962 where production tooling is not yet available for RFC 9162. Implementations MUST document which CT specification they implement.

## 7.6 Revocation

The ACME Server **MUST** support client-initiated (`revokeCert`) and server-initiated revocation (RP List removal or instance-specific revocation), and publish status via OCSP and/or CRL.

For multi-instance deployments, revocation of one instance's WRPAC MUST be scoped to that instance and MUST NOT affect WRPACs issued to other instances of the same WRP.

As per notification of removal of an RP from Trust List, RA SHALL without delay:
1.Delete EAB when RP has registered with the automated process
2.Order revocation of all RP’s RPAC.

> [!NOTE]
> CS-RPAC_13: For interoperability testing, RP List removal MAY be simulated.

## 7.7 Trusted List Integration

1. The test environment MUST include a simulated Trusted List containing the trust anchor certificate(s) of the CA(s) participating in the WE BUILD pilot. Individual WRPAC end-entity certificates are NOT listed in the Trusted List; trust is established through the CA trust anchor chain.
2. Wallet Units MUST verify WRPACs by building and validating the certificate chain up to a CA trust anchor present in the Trusted List.

## 7.8 WE BUILD RP Lists

In the WE BUILD pilot, participating TSPs acting as mock Registrars establish and maintain the Lists of authorized Relying Parties, in accordance with the Blueprint [5] MVP governance model. This is the functional equivalent of the national register of wallet-relying parties.

1. The RA MUST check these lists as a precondition for EAB credential issuance.

Each RP List entry MUST contain at minimum:

* WRP unique identifier
* WRP legal name
* Authorization status (active / revoked)

Each RP List entry SHOULD contain entitlements or types of entitlements.

## 7.9 IANA Considerations

This specification defines extensions to the ACME protocol that fall within IANA registries established by RFC 8555 and its successors, and introduces a custom URI suffix. For interoperability-testing purposes within WE BUILD ITB+, registration is not a prerequisite; for any future production use, the following registrations would be required.

**ACME Identifier Types registry** (established by RFC 8555): the identifier type `wrp-id` (§5.2) would need to be registered.

**Well-Known URI registry** (RFC 8615 [19]): the URI suffix `acme-eudi-wrpac` (§8.1) would need to be registered if the `/.well-known/` prefix is used. Alternatively, since RFC 8555 does not mandate the use of `/.well-known/` for the ACME directory, a conventional (non-`.well-known/`) path MAY be used, as shown in §8.1. Implementations intending to place the ACME directory under `/.well-known/acme-eudi-wrpac/` MUST complete the RFC 8615 registration process.

**ACME directory metadata extensions**: the metadata fields `rprcCoIssuanceSupported` and `multiInstanceIssuanceSupported` (§8.1) are WE BUILD-specific extensions. The IANA "ACME Directory Metadata Fields" registry (established by RFC 8555) would need to be updated for any production deployment.

# 8. Interface Definitions

## 8.1 ACME Directory

* **Method**: `GET`
* **URL**: `{base}/acme-eudi-wrpac/directory` (see §7.9 for URI considerations)

```json
{
  "newNonce":   "https://acme.example/new-nonce",
  "newAccount": "https://acme.example/new-acct",
  "newOrder":   "https://acme.example/new-order",
  "revokeCert": "https://acme.example/revoke-cert",
  "keyChange":  "https://acme.example/key-change",
  "meta": {
    "termsOfService": "https://acme.example/terms",
    "externalAccountRequired": true,
    "supportedIdentifierTypes": ["wrp-id"], 
    "rprcCoIssuanceSupported": true,
    "multiInstanceIssuanceSupported": true
  }
}
```

> [!NOTE]
> CS-RPAC_14: `rprcCoIssuanceSupported` and `multiInstanceIssuanceSupported` are WE BUILD extensions to the ACME directory metadata. The former indicates the server can co-issue WRPAC and WRPRC; the latter indicates support for per-instance issuance per the ARF v2.8 Relying Party Instance model [15]. Registration considerations for these extensions are described in §7.9.

## 8.2 Account Management with EBW/EBWOID

* **Method**: `POST` (JWS-signed)

**Pre-condition**: EBW authentication + EBWOID validation completed; EAB credentials received.

```json
{
  "termsOfServiceAgreed": true,
  "contact": ["mailto:representative@rp.example"],
  "externalAccountBinding": {
    "protected": "<JWS header with alg (MAC), kid (EAB Key ID), and url>",
    "payload": "<ACME account public key in JWK form>",
    "signature": "<HMAC signature>"
  }
}
```

## 8.3 Order Lifecycle

**Create order (single instance):**

```json
{
  "identifiers": [
    { "type": "wrp-id", "value": "NLKVK.12345678" }
  ]
}
```

**Create order (multi-instance, with instanceId):**

```json
{
  "identifiers": [
    { "type": "wrp-id", "value": "NLKVK.12345678" }
  ],
  "instanceId": "production-eu-west-1"
}
```

The `instanceId` value is an opaque string chosen by the ACME Client. It MUST be unique among all currently valid WRPACs issued to the same `wrp-id`. Recommended format: a short alphanumeric label identifying the deployment context (e.g., environment, region, or service name).

**Order states** (per RFC 8555 §7.1.6 "Status Changes" [1]): `pending` ? `valid`.

## 8.4 Finalize and Certificate

**Finalize:**

```json
{ "csr": "<base64url DER-encoded PKCS#10 CSR>" }
```

**Order RPAC (WE BUILD):**

```json
{
  "status": "valid",
  "identifiers": [
    { "type": "wrp-id", "value": "NLKVK.12345678" }
  ],
  "instanceId": "production-eu-west-1",
  "certificate": "https://acme.example/cert/cert012",
  "finalize": "https://acme.example/order/ord456/finalize",
  }
```

The `instanceId` field in the order response echoes the value from the order request.

**Certificate download**: `application/pem-certificate-chain` per RFC 8555 §7.4.2 [1] (end-entity first).

## 8.5 Revocation

```json
{ "certificate": "<base64url DER-encoded certificate>", "reason": 0 }
```

For multi-instance deployments, revocation targets the specific certificate identified by the DER-encoded value. Other WRPACs issued to the same `wrp-id` are unaffected.

> [!NOTE]
> CS-RPAC_15:This profile does not use ACME authorizations and challenges. Authorization is performed during EAB provisioning and account creation.

# 9. Conformance

An implementation **conforms as an ACME Server (TSP: RA + CA)** if it:

1. Implements ACME per RFC 8555 [1] with the extensions in §5.
2. Publishes an ACME directory per §8.1.
3. Requires EAB with EBW/EBWOID verification (§5.3).
4. Supports `wrp-id` identifiers.
5. Issues certificates per §7.4, including compliance with ETSI TS 119 411-8 v1.1.1 [3] and the attribute mapping in ETSI TS 119 475 v1.2.1 clause 5 [4].
6. Logs to CT logs (§7.5).
7. Supports revocation (§7.6).
8. Supports multi-instance issuance per §5.2, §7.2, and §8.3.
9. Implements interfaces per §8.

An implementation **conforms as an ACME Client (WRP / EBW)** if it:

1. Implements ACME per RFC 8555 [1] with the extensions in §5.
2. Supports EBW-based EAB provisioning (§5.3).
3. Creates accounts with EAB, orders with `wrp-id` (and optional `instanceId`).
4. Submits valid CSRs with distinct key pairs per instance, and validates certificate chains.
5. Supports revocation.

An implementation **conforms as a test environment** if it:

1. Provides WE BUILD RP Lists.
2. Provides a simulated Trusted List containing CA trust anchor certificate(s).
3. Provides a CT log (or test equivalent).
4. Supports EAB provisioning (or simulation per MVP scope).
5. Supports automated full-lifecycle testing, including multi-instance issuance scenarios.

An **MVP+ conformant** implementation additionally:

1. Implements the full OID4VP-based EBW authentication flow for EAB provisioning (§5.3, §6.2).
2. Accepts the organisation's EBWOID (EAA) as presented via the EBW during the pre-ACME authentication phase.

Profiles for specific WE BUILD credential types MUST NOT relax these requirements.

**Mapping of the WE BUILD Blueprint issuance workflow (derived from ETSI TS 119 475 v1.2.1 Annex D, Use Case 1: Integrated model [4]) to ACME protocol operations:**

| Blueprint Step | Description | ACME Operation | Section |
|---|---|---|---|
| **1** | User authenticates to RA using EBW | EBW authentication ? EAB provisioning | §5.3, §8.2 |
| **2** | RA requests credentials | OID4VP request from RA to EBW [MVP+] | §5.3 |
| **3** | User supplies EAA (EBWOID) | EBW presents EBWOID to RA | §5.3 |
| **4** | RA collects additional WRPRC attributes | Collected during EAB provisioning | §6.2 |
| **5** | RA checks RP in authorized RP lists | — | §6.2 |
| **6** | RA orders issuance of both certificates | ACME `finalize` (CSR submission) | §8.5 |
| **7** | CA issues WRPAC| ACME Server generates certificates, order ? `valid` | §8.5 |
| **7** | CA issues WRPRC| —| §6.2 |
| **8** | CA transmits certificates to RA | Internal (ACME Server encapsulates RA+CA) | — |
| **9** | RA notifies user (e.g. by email) | Order polling: status ? `valid`. Optional out-of-band notification. | §8.5 |
| **10** | User authenticates via EBW | Certificate download authenticated via JWS-signed POST-as-GET (account key bound to EBW via EAB) | §8.5 |
| **11** | User retrieves WRPAC and WRPRC | ACME certificate download from `certificate` URL | §8.5 |

> [!NOTE]
> CS-RPAC_16: The table above maps the eleven-step workflow used by the WE BUILD Blueprint [5] — which is derived from the integrated issuance model described in ETSI TS 119 475 v1.2.1 Annex D, Use Case 1 [4] — to the ACME protocol operations defined by this specification, including Registration Process and EAB credentials issuance. ETSI TS 119 475 Annex D is informative and presents four use cases (D.1 Integrated model, D.2 Registrar-initiated, D.3 RP-initiated, D.4 Provider-assisted); the eleven discrete steps enumerated above are a WE BUILD refinement of the D.1 flow and are not themselves a normative ETSI enumeration.

**Key design decisions:**

* **Steps 1-3** (EBW auth + EBWOID) are a **pre-ACME phase** producing EAB credentials. This cleanly separates organisational authentication from the machine protocol. Authorisation derives from control of the organisation's EBW and the EBWOID it presents; the EBWOID's `id`/`name` are matched against the order's `wrp-id` (§7.2 item 5). Full OID4VP-based EBW authentication is required for MVP+ conformance.
* **Step 4** (WRPRC attributes) is collected either during EAB provisioning.
* **Step 5** (RP list check) is performed by RA for EAB credentials issuance.
* **Steps 6-8** (order, issue, transmit) map to ACME `finalize` ? `pending` ? `valid`.
* **Steps 9-11** (notify, auth, retrieve) map to order polling and certificate download, with optional email notification.

> [!NOTE]
> CS-RPAC_17: The Blueprint specifies RA and CA as separate actors. In this ACME profile they MAY be encapsulated in a single endpoint. Implementations SHOULD separate them internally. This is consistent with real-world ACME CAs where the RA front-end and CA signing backend are separate systems behind one protocol interface.

# References

[1] IETF (2019) RFC 8555 — Automatic Certificate Management Environment (ACME). Standards Track, March 2019. https://www.rfc-editor.org/rfc/rfc8555

[2] European Commission (2025) Commission Implementing Regulation (EU) 2025/848 of 6 May 2025 laying down rules for the application of Regulation (EU) No 910/2014 of the European Parliament and of the Council as regards the registration of wallet-relying parties. OJ L, 2025/848, 7.5.2025. Applies from 24 December 2026. http://data.europa.eu/eli/reg_impl/2025/848/oj

[3] ETSI (2025) ETSI TS 119 411-8 v1.1.1 (2025-10) — Electronic Signatures and Trust Infrastructures (ESI); Policy and security requirements for Trust Service Providers issuing certificates; Part 8: Access Certificate Policy for EUDI Wallet Relying Parties.

[4] ETSI (2026) ETSI TS 119 475 v1.2.1 (2026-03) — Electronic Signatures and Trust Infrastructures (ESI); Relying party attributes supporting EUDI Wallet user's authorisation decisions. In particular Annex D, Use Case 1 (Integrated model).

[5] WE BUILD (2026) WP4 Architecture Blueprint — RPAC/RPRC Documentation. https://webuild-consortium.github.io/wp4-architecture/blueprint/blueprint.html

[6] WE BUILD (2025) ITB+ Reference Specification. https://github.com/webuild-consortium/wp4-interop-test-bed/

[7] IETF (2021) RFC 9162 — Certificate Transparency Version 2.0. Experimental, December 2021. Obsoletes RFC 6962. https://www.rfc-editor.org/rfc/rfc9162

[8] IETF (2015) RFC 7515 — JSON Web Signature (JWS). Standards Track, May 2015. https://www.rfc-editor.org/rfc/rfc7515

[9] European Commission (2025/2026) EC TS5 — Common formats and API for RP registration information. Draft, eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications repository.

[10] IETF (2008) RFC 5280 — Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile. Standards Track, May 2008. https://www.rfc-editor.org/rfc/rfc5280

[11] [Reserved]

[12] ETSI (2025) ETSI EN 319 411-1 v1.5.1 (2025-04) — Electronic Signatures and Trust Infrastructures (ESI); Policy and security requirements for Trust Service Providers issuing certificates; Part 1: General requirements.

[13] IETF (2003) RFC 3647 — Internet X.509 Public Key Infrastructure Certificate Policy and Certification Practices Framework. Informational, November 2003. https://www.rfc-editor.org/rfc/rfc3647

[14] Regulation (EU) No 910/2014, as amended by Regulation (EU) 2024/1183 of the European Parliament and of the Council of 11 April 2024 establishing the European Digital Identity Framework.

[15] EUDI Wallet Architecture and Reference Framework v2.8.0. https://eu-digital-identity-wallet.github.io/eudi-doc-architecture-and-reference-framework/

[16] European Commission (2025/2026) EC TS6 — Common set of RP registration information. Draft, eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications repository.

[17] IETF (2015) RFC 7638 — JSON Web Key (JWK) Thumbprint. Standards Track, September 2015. https://www.rfc-editor.org/rfc/rfc7638

[18] ETSI EN 319 412-1 — Electronic Signatures and Trust Infrastructures (ESI); Certificate Profiles; Part 1: Overview and common data structures.

[19] IETF (2019) RFC 8615 — Well-Known Uniform Resource Identifiers (URIs). Standards Track, May 2019. https://www.rfc-editor.org/rfc/rfc8615

[20] WE BUILD Attestation Rulebooks Catalog — EBWOID Attestation Rulebook (rb-ebwoid). https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-ebwoid
