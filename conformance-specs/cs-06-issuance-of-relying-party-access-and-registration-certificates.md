# WE BUILD - Conformance Specification: Issuance of Relying Party Access and Registration Certificates

Version 0.8 / Draft
Date: 23 April 2026

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language](#3-normative-language)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
  - [5.1 ACME Profile for WRPAC Issuance](#51-acme-profile-for-wrpac-issuance)
  - [5.2 ACME Resource Model](#52-acme-resource-model)
  - [5.3 WRPAC Identifier Type](#53-wrpac-identifier-type)
  - [5.4 Challenge Type: registrar-api-01](#54-challenge-type-registrar-api-01)
  - [5.5 EBW-based Account Binding](#55-ebw-based-account-binding)
  - [5.6 Mapping to WE BUILD Blueprint Issuance Process](#56-mapping-to-we-build-blueprint-issuance-process)
- [6. High-level Flows](#8-high-level-flows)
  - [6.1 Directory Discovery](#81-directory-discovery)
  - [6.2 Account Creation with EBW Authentication](#82-account-creation-with-ebw-authentication)
  - [6.3 Order Creation](#83-order-creation)
  - [6.4 Authorization and Challenge Validation](#84-authorization-and-challenge-validation)
  - [6.5 Order Finalization](#85-order-finalization)
  - [6.6 Certificate Download](#86-certificate-download)
  - [6.7 Certificate Revocation](#87-certificate-revocation)
- [7. Normative Requirements](#9-normative-requirements)
  - [7.1 Common Requirements](#91-common-requirements)
  - [7.2 ACME Server (CA / RA)](#92-acme-server-ca--ra)
  - [7.3 ACME Client (WRP / EBW)](#93-acme-client-wrp--ebw)
  - [7.4 Certificate Profile](#94-certificate-profile)
  - [7.5 Certificate Transparency](#95-certificate-transparency)
  - [7.6 Revocation](#96-revocation)
  - [7.7 Trusted List Integration](#97-trusted-list-integration)
  - [7.8 WE BUILD RP Lists](#98-we-build-rp-lists)
- [8. Interface Definitions](#10-interface-definitions)
  - [8.1 ACME Directory](#101-acme-directory)
  - [8.2 Account Management with EBW/POA](#102-account-management-with-ebwpoa)
  - [8.3 Order Lifecycle](#103-order-lifecycle)
  - [8.4 Authorization and Challenge](#104-authorization-and-challenge)
  - [8.5 Finalize and Certificate](#105-finalize-and-certificate)
  - [8.6 Revocation](#106-revocation)
- [9. Conformance](#11-conformance)
- [References](#references)

---

# 1. Introduction

This document defines the **WE BUILD Consortium Conformance Specification (CS)** for the issuance of Wallet-Relying Party Access Certificates (WRPACs) and, where applicable, Wallet-Relying Party Registration Certificates (WRPRCs) within the European Digital Identity Wallet ecosystem, using a protocol based on the Automatic Certificate Management Environment (ACME) as defined in RFC 8555 [1].

It profiles:

* Commission Implementing Regulation (EU) 2025/848 [2], in particular Article 7 and Annex IV
* ETSI TS 119 411-8 v1.1.1 [3] — Access Certificate Policy for EUDI Wallet Relying Parties
* ETSI TS 119 475 v1.2.1 [4] — Relying party attributes supporting EUDI Wallet user's authorisation decisions, in particular Annex D1 (Issuance process)
* WE BUILD WP4 Architecture Blueprint [5] — RPAC/RPRC documentation and issuance process
* IETF RFC 8555 [1] — Automatic Certificate Management Environment (ACME)

This specification positions the ACME protocol as the **technical implementation** of the issuance process defined in the WE BUILD Blueprint [5]. Section 7 provides an explicit mapping between the Blueprint's 11-step issuance flow and the ACME protocol operations.

This specification focuses **only on direct issuance** of WRPACs to registered Wallet-Relying Parties. The ACME flow is extended with EBW-based authentication and POA verification to align with the Blueprint's requirements for user authentication via European Business Wallets. This document is used to build the WE BUILD Interoperability Test Bed Plus (ITB+) [6].

> [!IMPORTANT]
> CS-RPAC_01: This specification is intended for **interoperability testing only**, not for production deployment. Its purpose is to validate the technical feasibility of ACME-based WRPAC issuance and to establish interoperability between independent implementations. Production deployments will require additional security hardening, policy alignment, and conformity assessment beyond the scope of this document.

# 2. Scope

This specification defines:

* An ACME protocol profile (based on RFC 8555) for the automated issuance of X.509-based Wallet-Relying Party Access Certificates, aligned with the WE BUILD Blueprint issuance process
* A custom ACME identifier type (`wrp-id`) for WRP identifiers
* A custom ACME challenge type (`registrar-api-01`) for verifying WRP authorization against WE BUILD RP Lists
* An EBW-based account binding mechanism for user authentication via European Business Wallets
* Requirements for:
    * ACME Servers (TSP Certificate Authorities and Registration Authorities)
    * ACME Clients (Wallet-Relying Parties using their EBW)
* Protocol flows for:
    * Direct WRPAC issuance to an authorized WRP (with optional co-issuance of WRPRC)
    * Certificate revocation

This specification does **not** cover:

* Intermediary or multi-party issuance
* Standalone WRPRC issuance (covered in a separate CS)
* Production deployment requirements (conformity assessment, CAB audits, national policy extensions)
* Proximity use cases for certificate presentation

# 3. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are to be interpreted as commonly used in technical specifications.

# 4. Roles and Components

This specification uses the following roles, mapped to both the ACME protocol and the WE BUILD Blueprint:

| ACME Role | Blueprint Role | Description |
|---|---|---|
| **ACME Client** | **User + EBW** | The RP representative using an European Business Wallet to authenticate and request certificates. The ACME Client software runs on or is invoked by the EBW. |
| **ACME Server** | **RA + CA** | The combined Registration Authority and Certificate Authority. The RA function handles identity verification, POA validation, and RP list checks. The CA function handles certificate generation and signing. These MAY be separate systems behind a single ACME endpoint. |
| — | **WP Leader** | Maintains the Lists of authorised RPs for the WE BUILD pilot. Functionally equivalent to the Registrar in the eIDAS ecosystem. |
| **Wallet Unit** | — | The EUDI/Business Wallet that verifies WRPACs during RP authentication. Not involved in issuance. |

Detailed role descriptions:

* **User (RP Representative):** A natural person authorized to act on behalf of the Wallet-Relying Party. Authenticates via an EBW and presents a Power of Attorney (POA) attestation as an EAA.
* **European Business Wallet (EBW):** The wallet application used by the RP representative to authenticate to the RA and to retrieve issued certificates. In the ACME flow, the EBW acts as the ACME Client or provides the authentication layer for the ACME Client.
* **Registration Authority (RA):** The TSP component that verifies the user's identity and POA, requests additional attributes for the RPRC, and checks the RP's presence in the authorised RP lists. Implemented as part of the ACME Server.
* **Certificate Authority (CA):** The TSP component that generates and signs WRPAC and WRPRC certificates. Implemented as the ACME Server's certificate issuance backend.
* **Lists of RP:** In the WE BUILD pilot, WP Leaders maintain lists of authorized Relying Parties. These lists serve as the functional equivalent of the national register of wallet-relying parties. The ACME Server checks these lists during authorization.

# 5. Protocol Overview

The WE BUILD WRPAC issuance protocol adapts the ACME framework (RFC 8555) to the EUDI Wallet trust model, implementing the issuance process defined in the WE BUILD Blueprint [5] and limited to Annex D1 of ETSI TS 119 475 [4] for MVP.

The key adaptations are:

* **Identifier type `wrp-id`**: replaces the `dns` identifier. The value is the WRP's unique identifier as it appears in the WE BUILD RP Lists.
* **Challenge type `registrar-api-01`**: replaces `http-01` / `dns-01`. The ACME Server verifies the WRP's presence in the WE BUILD RP Lists and confirms a token link between the ACME account and the RP entry.
* **EBW-based External Account Binding (EAB)**: REQUIRED for account creation. The RP representative authenticates via their EBW and presents a POA (EAA). The EAB binds the ACME account to the verified EBW identity and POA.
* **RA-integrated ACME Server**: the ACME Server combines RA and CA functions. The RA function validates identity, POA, and RP list membership. The CA function generates certificates.
* **Co-issuance of RPAC + RPRC**: the ACME order MAY result in both a WRPAC and a WRPRC being issued together, as specified in the Blueprint.
* **Certificate profile**: the issued certificate is an X.509 v3 WRPAC conforming to CIR 2025/848 Annex IV and ETSI TS 119 475 Annex D1.
* **Certificate Transparency**: the ACME Server logs all issued certificates per RFC 9162 [7].

All ACME messages are JSON payloads signed via JWS (RFC 7515 [6]), transported over HTTPS.

> [!NOTE]
> CS-RPAC_02: The choice of ACME provides a proven, standardised, and automatable protocol for certificate lifecycle management. It implements the Blueprint's 11-step process (Section 7) while enabling interoperability testing with off-the-shelf ACME tooling. The RA and CA functions defined in the Blueprint are encapsulated within the ACME Server.

# 5. ACME Profile for WRPAC Issuance

## 5.1 ACME Resource Model

This profile follows the standard ACME resource model:

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
  account     order ---+--> finalize
                |      |
                V      +--> certificate
          authorization      +--> registrationCertificate
                |
                V
           challenge
```

All standard ACME resource types and state transitions per RFC 8555 apply, with the extensions defined in Sections 5.2, 5.3, and 5.4. The `registrationCertificate` URL is a WE BUILD extension for WRPRC co-issuance.

## 5.2 WRPAC Identifier Type

**Type**: `wrp-id`

**Value**: the WRP's unique identifier as it appears in the WE BUILD RP Lists. For interoperability testing, the identifier format is defined by the WP Leader. In the production eIDAS ecosystem, this would use CIR 2025/848 Annex I identifiers (EUID, LEI, etc.).

**Example:**

```json
{
  "type": "wrp-id",
  "value": "NLKVK.12345678"
}
```

## 5.3 Challenge Type: registrar-api-01

**Type**: `registrar-api-01`

**Mechanism:**

1. The ACME Server generates a random `token` and returns it as part of the challenge object.
2. The ACME Client constructs a `key-authorization`: `token || '.' || base64url(Thumbprint(accountKey))`.
3. The ACME Client places the `key-authorization` as the `acme-challenge` attribute in its RP List entry.
4. The ACME Client signals readiness by POSTing to the challenge URL.
5. The ACME Server checks the RP List:
    * WRP is present and authorized
    * `acme-challenge` attribute matches the expected `key-authorization`
    * Identity data is consistent with the account and POA
6. Authorization transitions to `valid` on success.

**Challenge object:**

```json
{
  "type": "registrar-api-01",
  "url": "https://acme.example/chall/abc123",
  "status": "pending",
  "token": "DGyRejbN4F7wAJ3gPMR8Kw0VxBWgKEn2T4u-bQ_6Oc"
}
```

> [!NOTE]
> CS-RPAC_03: In the WE BUILD pilot, the RP Lists maintained by WP Leaders replace the national register. The `registrar-api-01` challenge verifies presence in these lists (Blueprint step 5). In production, this would query the Registrar's API per EC TS5 [9].

## 5.4 EBW-based Account Binding

This profile extends ACME External Account Binding (RFC 8555 §7.3.4) with EBW authentication. This implements Blueprint steps 1-3.

**Mechanism:**

1. The RP representative authenticates to the RA using their EBW, presenting PID/EBWOID and a POA attestation (EAA).
2. The RA validates the POA and verifies the representative's authority.
3. The RA issues EAB credentials (Key ID + HMAC Key) bound to the verified identity and POA.
4. The ACME Client uses these EAB credentials during `newAccount`.

**EAB in newAccount:**

```json
{
  "termsOfServiceAgreed": true,
  "contact": ["mailto:representative@rp.example"],
  "externalAccountBinding": {
    "protected": "<JWS header with EAB Key ID>",
    "payload": "<account public key>",
    "signature": "<HMAC signature>"
  }
}
```

> [!NOTE]
> CS-RPAC_04: For initial interoperability testing, EBW authentication MAY be simulated. EAB credentials are pre-provisioned by the RA/TSP after out-of-band identity verification. Future iterations will implement the full EBW-based OID4VP authentication flow for EAB provisioning.

# 6. High-level Flows

## 6.1 Directory Discovery

1. The ACME Client fetches the directory document via HTTPS GET.
2. The directory includes metadata: `externalAccountRequired: true`, `supportedIdentifierTypes: ["wrp-id"]`, `supportedChallengeTypes: ["registrar-api-01"]`.

## 6.2 Account Creation with EBW Authentication

**Pre-ACME phase (Blueprint steps 1-3):**

1. The RP representative connects to the TSP's RA portal/service.
2. The RA initiates an OID4VP request to the user's EBW, requesting PID/EBWOID and POA (EAA).
3. The EBW presents the requested credentials.
4. The RA validates the POA and verifies the representative's authority.
5. Optionally (Blueprint step 4): the RA requests additional attributes for RPRC production.
6. The RA issues EAB credentials to the user.

**ACME phase:**

7. The ACME Client generates an account key pair.
8. The ACME Client sends `newAccount` with the EAB binding.
9. The ACME Server validates the EAB and creates the account.

## 6.3 Order Creation

1. The ACME Client sends `newOrder` with one `wrp-id` identifier.
2. The ACME Server creates the order in `pending` state and returns authorization URL(s) and `finalize` URL.

## 6.4 Authorization and Challenge Validation

*Blueprint step 5: RP list check.*

1. The ACME Client fetches the authorization.
2. The ACME Client completes the `registrar-api-01` challenge: compute `key-authorization`, place in RP List, signal readiness.
3. The ACME Server checks the RP List and validates.
4. Authorization transitions to `valid`.

## 6.5 Order Finalization

*Blueprint steps 6-9: order, issue, transmit, notify.*

1. The ACME Client generates a certificate key pair and CSR.
2. The ACME Client sends the CSR to the `finalize` URL.
3. The ACME Server (RA) validates; the ACME Server (CA) generates WRPAC (and optionally WRPRC).
4. The CA submits to CT logs and obtains SCTs.
5. The order transitions to `valid` with a `certificate` URL (and optionally `registrationCertificate` URL).
6. The ACME Server MAY send out-of-band notification to the RP representative.

## 6.6 Certificate Download

*Blueprint steps 10-11: authenticate + retrieve.*

1. The ACME Client sends POST-as-GET to the `certificate` URL (authenticated via account key bound to EBW).
2. The ACME Server returns the PEM certificate chain.
3. If WRPRC was co-issued, it is available at the `registrationCertificate` URL.

## 6.7 Certificate Revocation

1. Client-initiated: `revokeCert` request.
2. Server-initiated: upon RP removal from the RP List.

# 7. Normative Requirements

## 7.1 Common Requirements

Both ACME Client and ACME Server **MUST**:

1. Implement the ACME protocol per RFC 8555 [1] with the extensions in Section 6.
2. Use HTTPS for all communication.
3. Use JWS (RFC 7515 [6]) for all request payloads.
4. Implement nonce-based replay protection.

## 7.2 ACME Server (CA / RA)

The ACME Server **MUST**:

1. Publish an ACME directory at a well-known URL.
2. Require EAB for all accounts (RFC 8555 §7.3.4).
3. Support `wrp-id` identifiers and `registrar-api-01` challenges.
4. Verify WRP presence in the WE BUILD RP Lists during challenge validation (Blueprint step 5).
5. Reject authorization if the WRP is not in the list or identity data is inconsistent.
6. Issue WRPACs exclusively to authorized WRPs.
7. Support the order state machine per RFC 8555 §7.1.6.
8. Support `revokeCert`.
9. Implement the RA function: POA validation (Blueprint steps 1-3) and RP List check (step 5).

The ACME Server **SHOULD**:

1. Support co-issuance of WRPRC alongside WRPAC in a single order.
2. Send out-of-band notification when certificates are ready (Blueprint step 9).
3. Support `keyChange`.

## 7.3 ACME Client (WRP / EBW)

The ACME Client **MUST**:

1. Perform directory discovery.
2. Support EAB using credentials obtained through EBW authentication.
3. Support `wrp-id` identifiers and `registrar-api-01` challenges.
4. Generate key pairs and construct valid CSRs per Section 9.4.
5. Validate the returned certificate chain.
6. Support `revokeCert`.

The ACME Client **SHOULD**:

1. Integrate with the EBW for authentication during EAB provisioning.
2. Clean up `acme-challenge` from the RP List after successful issuance.

## 7.4 Certificate Profile

Issued WRPACs **MUST**:

1. Be X.509 v3 certificates conforming to RFC 5280 [10].
2. Contain the WRP's legal name in the Subject field (CIR 2025/848 Annex I §1).
3. Contain a user-friendly name where applicable (Annex I §2).
4. Contain at least one unique WRP identifier (Annex I §3).
5. Include a certificate policy OID (Annex IV §3).
6. Include certification path information (URI).
7. Include a SAN extension (DNS name or URI).
8. Include registration information per Annex I points 1, 2, and 8.
9. Comply with RFC 5755 [11] for attribute expression.
10. Conform to ETSI TS 119 475 Annex D1 [4].
11. Use RSA (min. 3072 bits), ECDSA (P-256 or P-384), SHA-256 or stronger.

> [!NOTE]
> CS-RPAC_06: For interoperability testing, implementations SHOULD support both RSA and ECDSA. NCP per ETSI EN 319 411-1 [12] is the baseline.

## 7.5 Certificate Transparency

The ACME Server **MUST** log all WRPACs in CT logs per RFC 9162 [7] and embed SCTs.

> [!NOTE]
> CS-RPAC_07: For interoperability testing, test CT logs MAY be used.

## 7.6 Revocation

The ACME Server **MUST** support client-initiated (`revokeCert`) and server-initiated revocation (RP List removal), and publish status via OCSP and/or CRL.

> [!NOTE]
> CS-RPAC_08: For interoperability testing, RP List removal MAY be simulated.

## 7.7 Trusted List Integration

1. The test environment MUST include a simulated Trusted List with the CA's trust anchor(s).
2. Wallet Units MUST verify WRPACs against this Trusted List.

## 7.8 WE BUILD RP Lists

Per the Blueprint assumptions [5]:

1. Without actual Registrars, the present RAs of involved TSPs play the Registrar role.
2. WP Leaders establish and maintain lists of authorized RPs.
3. The ACME Server MUST check these lists as a precondition for issuance.
4. The RP List MUST support an `acme-challenge` metadata attribute.

Each RP List entry MUST contain at minimum:

* WRP unique identifier
* WRP legal name
* Authorization status (active / revoked)
* Metadata fields (including `acme-challenge`)

# 8. Interface Definitions

## 8.1 ACME Directory

* **Method**: `GET`
* **URL**: `{base}/.well-known/acme-eudi-wrpac/directory`

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
    "supportedChallengeTypes": ["registrar-api-01"],
    "rprcCoIssuanceSupported": true
  }
}
```

> [!NOTE]
> CS-RPAC_09: `rprcCoIssuanceSupported` is a WE BUILD extension indicating the server can co-issue RPAC and RPRC.

## 8.2 Account Management with EBW/POA

* **Method**: `POST` (JWS-signed)

**Pre-condition**: EBW authentication + POA validation completed; EAB credentials received.

```json
{
  "termsOfServiceAgreed": true,
  "contact": ["mailto:representative@rp.example"],
  "externalAccountBinding": {
    "protected": "<JWS header with EAB Key ID>",
    "payload": "<account public key>",
    "signature": "<HMAC signature>"
  }
}
```

## 8.3 Order Lifecycle

**Create order:**

```json
{
  "identifiers": [
    { "type": "wrp-id", "value": "NLKVK.12345678" }
  ]
}
```

**Order states**: `pending` → `ready` → `processing` → `valid` (or `invalid`)

## 8.4 Authorization and Challenge

**Authorization response:**

```json
{
  "status": "pending",
  "identifier": { "type": "wrp-id", "value": "NLKVK.12345678" },
  "challenges": [
    {
      "type": "registrar-api-01",
      "url": "https://acme.example/chall/chall789",
      "status": "pending",
      "token": "DGyRejbN4F7wAJ3gPMR8Kw0VxBWgKEn2T4u-bQ_6Oc"
    }
  ]
}
```

## 8.5 Finalize and Certificate

**Finalize:**

```json
{ "csr": "<base64url DER-encoded PKCS#10 CSR>" }
```

**Order with co-issued RPRC (WE BUILD extension):**

```json
{
  "status": "valid",
  "certificate": "https://acme.example/cert/cert012",
  "registrationCertificate": "https://acme.example/rprc/rprc012",
  "finalize": "https://acme.example/order/ord456/finalize",
  "authorizations": ["https://acme.example/authz/xyz789"]
}
```

**Certificate download**: `application/pem-certificate-chain` (end-entity first).

## 8.6 Revocation

```json
{ "certificate": "<base64url DER-encoded certificate>", "reason": 0 }
```

# 9. Conformance

An implementation **conforms as an ACME Server (TSP: RA + CA)** if it:

1. Implements ACME per RFC 8555 with the extensions in Section 6.
2. Publishes an ACME directory per Section 10.1.
3. Requires EAB with EBW/POA verification (Section 6.4).
4. Supports `wrp-id` identifiers and `registrar-api-01` challenges.
5. Verifies WRP presence in WE BUILD RP Lists (Section 9.8).
6. Issues certificates per Section 9.4.
7. Logs to CT logs (Section 9.5).
8. Supports revocation (Section 9.6).
9. Implements RA function: POA validation + RP List checks (Section 9.2).
10. Implements interfaces per Section 10.
11. Follows the Blueprint mapping per Section 7.

An implementation **conforms as an ACME Client (WRP / EBW)** if it:

1. Implements ACME per RFC 8555 with the extensions in Section 6.
2. Supports EBW-based EAB provisioning (Section 6.4).
3. Creates accounts with EAB, orders with `wrp-id`, and completes `registrar-api-01` challenges.
4. Submits valid CSRs and validates certificate chains.
5. Supports revocation.

An implementation **conforms as a test environment** if it:

1. Provides WE BUILD RP Lists with `acme-challenge` metadata support.
2. Provides a simulated Trusted List.
3. Provides a CT log (or test equivalent).
4. Supports EAB provisioning (or simulation).
5. Supports automated full-lifecycle testing.

Profiles for specific WE BUILD credential types MUST NOT relax these requirements.

Conformance of the Blueprint's 11-step issuance process [5] to the ACME protocol.

| Blueprint Step | Description | ACME Operation | Section |
|---|---|---|---|
| **1** | User authenticates to RA using EBW | EBW authentication → EAB provisioning | 6.4, 8.2 |
| **2** | RA requests credentials | OID4VP request from RA to EBW | 6.4 |
| **3** | User supplies EAA (POA) | EBW presents POA to RA | 6.4 |
| **4** | RA requests additional RPRC attributes | Collected during EAB provisioning or as order metadata | 8.3 |
| **5** | RA checks RP in authorized RP lists | `registrar-api-01` challenge validation | 6.3, 8.4 |
| **6** | RA orders issuance of both certificates | ACME `finalize` (CSR submission) | 8.5 |
| **7** | CA issues RPAC and RPRC | ACME Server generates certificates, order → `valid` | 8.5 |
| **8** | CA transmits certificates to RA | Internal (ACME Server encapsulates RA+CA) | — |
| **9** | RA notifies user (e.g. by email) | Order polling: status → `valid`. Optional out-of-band notification. | 8.5 |
| **10** | User authenticates via EBW | Certificate download authenticated via JWS-signed POST-as-GET (account key bound to EBW via EAB) | 8.6 |
| **11** | User retrieves RPAC and RPRC | ACME certificate download from `certificate` URL | 8.6 |

**Key design decisions:**

* **Steps 1-3** (EBW auth + POA) are a **pre-ACME phase** producing EAB credentials. This cleanly separates human authentication from the machine protocol.
* **Step 4** (RPRC attributes) is collected either during EAB provisioning or as ACME order metadata.
* **Step 5** (RP list check) maps directly to the `registrar-api-01` challenge.
* **Steps 6-8** (order, issue, transmit) map to ACME `finalize` → `processing` → `valid`.
* **Steps 9-11** (notify, auth, retrieve) map to order polling and certificate download, with optional email notification.

> [!NOTE]
> CS-RPAC_05: The Blueprint specifies RA and CA as separate actors. In this ACME profile they are encapsulated in a single endpoint. Implementations MAY separate them internally. This is consistent with real-world ACME CAs where the RA front-end and CA signing backend are separate systems behind one protocol interface.

# References

[1] IETF (2019) RFC 8555 — ACME. https://www.rfc-editor.org/rfc/rfc8555

[2] European Commission (2025) CIR (EU) 2025/848 on the registration of wallet-relying parties. https://eur-lex.europa.eu/eli/reg_impl/2025/848/oj

[3] ETSI (2025) ETSI TS 119 411-8 v1.1.1 — Access Certificate Policy for EUDI Wallet Relying Parties.

[4] ETSI (2025/2026) ETSI TS 119 475 v1.1.1 / v1.2.1 — Relying party attributes supporting EUDI Wallet user's authorisation decisions. In particular Annex D1.

[5] WE BUILD (2026) WP4 Architecture Blueprint — RPAC/RPRC Documentation. https://webuild-consortium.github.io/wp4-architecture/blueprint/blueprint.html

[6] WE BUILD (2025) ITB+ Reference Specification. https://github.com/webuild-consortium/wp4-interop-test-bed/

[7] IETF (2021) RFC 9162 — Certificate Transparency Version 2.0. https://www.rfc-editor.org/rfc/rfc9162

[6] IETF (2015) RFC 7515 — JWS. https://www.rfc-editor.org/rfc/rfc7515

[9] European Commission (2025/2026) EC TS5 — Common formats and API for RP registration information.

[10] IETF (2008) RFC 5280 — X.509 PKI Certificate and CRL Profile. https://www.rfc-editor.org/rfc/rfc5280

[11] IETF (2010) RFC 5755 — Attribute Certificate Profile. https://www.rfc-editor.org/rfc/rfc5755

[12] ETSI (2023) ETSI EN 319 411-1 v1.4.1 — TSP Policy; Part 1: General requirements.

[13] IETF (2003) RFC 3647 — Certificate Policy Framework. https://www.rfc-editor.org/rfc/rfc3647

[14] Regulation (EU) No 910/2014, amended by (EU) 2024/1183.

[15] EUDI Wallet ARF v2.6. https://eu-digital-identity-wallet.github.io/eudi-doc-architecture-and-reference-framework/