# WE BUILD - Conformance Specification: Issuance of Relying Party Access and Registration Certificates

Version 0.2 / First proposal
Date: 24 April 2026

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language and Terminology](#3-normative-language-and-terminology)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
  - [5.1 ACME Resource Model](#51-acme-resource-model)
  - [5.2 WRPAC Identifier Type](#52-wrpac-identifier-type)
  - [5.3 Challenge Type: registrar-api-01](#53-challenge-type-registrar-api-01)
  - [5.4 EBW-based Account Binding](#54-ebw-based-account-binding)
- [6. High-level Flows](#6-high-level-flows)
  - [6.1 Directory Discovery](#61-directory-discovery)
  - [6.2 Account Creation with EBW Authentication](#62-account-creation-with-ebw-authentication)
  - [6.3 Order Creation](#63-order-creation)
  - [6.4 Authorization and Challenge Validation](#64-authorization-and-challenge-validation)
  - [6.5 Order Finalization](#65-order-finalization)
  - [6.6 Certificate Download](#66-certificate-download)
  - [6.7 Certificate Revocation](#67-certificate-revocation)
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
  - [8.2 Account Management with EBW/POA](#82-account-management-with-ebwpoa)
  - [8.3 Order Lifecycle](#83-order-lifecycle)
  - [8.4 Authorization and Challenge](#84-authorization-and-challenge)
  - [8.5 Finalize and Certificate](#85-finalize-and-certificate)
  - [8.6 Revocation](#86-revocation)
- [9. Conformance](#9-conformance)
- [References](#references)

---

# 1. Introduction

This document defines the **WE BUILD Consortium Conformance Specification (CS)** for the issuance of Wallet-Relying Party Access Certificates (WRPACs) and, where applicable, Wallet-Relying Party Registration Certificates (WRPRCs) within the European Digital Identity Wallet ecosystem, using a protocol based on the Automatic Certificate Management Environment (ACME) as defined in RFC 8555 [1].

It profiles:

* Commission Implementing Regulation (EU) 2025/848 [2], in particular Article 7, Annex I, Annex IV, and Annex V (the latter for optional WRPRC co-issuance)
* ETSI TS 119 411-8 v1.1.1 (2025-10) [3] — Access Certificate Policy for EUDI Wallet Relying Parties
* ETSI TS 119 475 v1.2.1 (2026-03) [4] — Relying party attributes supporting EUDI Wallet user's authorisation decisions, in particular Annex D, Use Case 1 (Integrated model)
* WE BUILD WP4 Architecture Blueprint [5] — RPAC/RPRC documentation and issuance process
* IETF RFC 8555 [1] — Automatic Certificate Management Environment (ACME)

This specification positions the ACME protocol as a **technical implementation** of the integrated issuance model described in ETSI TS 119 475 v1.2.1 Annex D, Use Case 1 [4], as adopted by the WE BUILD Blueprint [5]. Section 9 provides an explicit mapping between the WE BUILD Blueprint issuance workflow and the ACME protocol operations.

This specification focuses **only on direct issuance** of WRPACs to registered Wallet-Relying Parties. The ACME flow is extended with EBW-based authentication and POA verification to align with the Blueprint's requirements for user authentication via European Business Wallets. This document is used to build the WE BUILD Interoperability Test Bed Plus (ITB+) [6].

> [!IMPORTANT]
> CS-RPAC_01: This specification is intended for **interoperability testing only**, not for production deployment. Its purpose is to validate the technical feasibility of ACME-based WRPAC issuance and to establish interoperability between independent implementations. Production deployments will require additional security hardening, policy alignment, and conformity assessment beyond the scope of this document.

> [!NOTE]
> CS-RPAC_02: CIR (EU) 2025/848 [2] was adopted on 6 May 2025 and **applies from 24 December 2026**. Requirements in this specification that derive from CIR (EU) 2025/848 are therefore drafted in anticipation of that date of application.

# 2. Scope

This specification defines:

* An ACME protocol profile (based on RFC 8555) for the automated issuance of X.509-based Wallet-Relying Party Access Certificates, aligned with the WE BUILD Blueprint issuance process
* A custom ACME identifier type (`wrp-id`) for WRP identifiers
* A custom ACME challenge type (`registrar-api-01`) for verifying WRP authorization against WE BUILD RP Lists
* An EBW-based account binding mechanism for user authentication via European Business Wallets
* Support for multi-instance issuance, enabling a single WRP to obtain separate WRPACs for multiple Relying Party Instances per the EUDI Wallet ARF v2.8 [15]
* Requirements for:
    * ACME Servers (TSP Certificate Authorities and Registration Authorities)
    * ACME Clients (Wallet-Relying Parties using their EBW)
* Protocol flows for:
    * Direct WRPAC issuance to an authorized WRP (with optional co-issuance of WRPRC)
    * Multi-instance issuance (one WRPAC per Relying Party Instance)
    * Certificate revocation

This specification does **not** cover:

* Intermediary or multi-party issuance
* Standalone WRPRC issuance (covered in a separate CS)
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
* **POA** — Power of Attorney.
* **EAA** — Electronic Attestation of Attributes.
* **PID** — Person Identification Data.
* **EBWOID** — European Business Wallet Organisational Identification Data.

# 4. Roles and Components

This specification uses the following roles, mapped to both the ACME protocol and the WE BUILD Blueprint:

| ACME Role | Blueprint Role | Description |
|---|---|---|
| **ACME Client** | **User + EBW** | The RP representative using an European Business Wallet. The EBW plays two roles in this specification: (i) host or invocation environment for the ACME Client software, and (ii) user-authentication authority for EBW-based External Account Binding per RFC 8555 §7.3.4 [1]. |
| **ACME Server** | **RA + CA** | The combined Registration Authority and Certificate Authority. The RA function handles identity verification, POA validation, and RP list checks. The CA function handles certificate generation and signing. These MAY be separate systems behind a single ACME endpoint. |
| — | **Mock Registrar (RA/TSP)** | In the WE BUILD pilot, participating TSPs acting as mock Registrars maintain the Lists of authorised RPs. This role is functionally equivalent to the Member State Registrar in the production eIDAS ecosystem. In production, this function is performed by the national Registrar of the Member State concerned per the eIDAS framework. |
| **Wallet Unit** | — | The EUDI/Business Wallet that verifies WRPACs during RP authentication. Not involved in issuance. |

Detailed role descriptions:

* **User (RP Representative):** A natural person authorized to act on behalf of the Wallet-Relying Party. Authenticates via an EBW and presents a Power of Attorney (POA) attestation as an EAA.
* **European Business Wallet (EBW):** The wallet application used by the RP representative to authenticate to the RA and to retrieve issued certificates. In the ACME flow, the EBW acts as the ACME Client or provides the authentication layer for the ACME Client.
* **Registration Authority (RA):** The TSP component that verifies the user's identity and POA, requests additional attributes for the RPRC, and checks the RP's presence in the authorised RP lists. Implemented as part of the ACME Server.
* **Certificate Authority (CA):** The TSP component that generates and signs WRPAC and WRPRC certificates. Implemented as the ACME Server's certificate issuance backend.
* **Mock Registrar:** In the WE BUILD pilot, participating TSPs acting as mock Registrars establish and maintain the Lists of authorized Relying Parties. These lists serve as the functional equivalent of the national register of wallet-relying parties per the Blueprint [5] MVP governance model. The ACME Server checks these lists during authorization. During ITB+ conformance testing, the WE BUILD RP List is served by the mock Registrar; in production, by the national Registrar of the Member State concerned.

# 5. Protocol Overview

The WE BUILD WRPAC issuance protocol adapts the ACME framework (RFC 8555) to the EUDI Wallet trust model, implementing the integrated issuance model described in ETSI TS 119 475 v1.2.1 Annex D, Use Case 1 [4] as adopted by the WE BUILD Blueprint [5].

The key adaptations are:

* **Identifier type `wrp-id`**: replaces the `dns` identifier. The value is the WRP's unique identifier as it appears in the WE BUILD RP Lists. For the `wrp-id` identifier type, the only defined challenge is `registrar-api-01`; the standard ACME challenges `http-01` and `dns-01` do not apply to `wrp-id`.
* **Challenge type `registrar-api-01`**: the ACME Server verifies the WRP's presence in the WE BUILD RP Lists and confirms a token link between the ACME account and the RP entry. The RP List entry supports multiple concurrent challenge tokens to enable multi-instance issuance (see §5.2).
* **EBW-based External Account Binding (EAB)**: REQUIRED for account creation. The RP representative authenticates via their EBW and presents a POA (EAA). The EAB binds the ACME account to the verified EBW identity and POA.
* **RA-integrated ACME Server**: the ACME Server combines RA and CA functions. The RA function validates identity, POA, and RP list membership. The CA function generates certificates.
* **Multi-instance issuance**: a single WRP (`wrp-id`) MAY obtain multiple WRPACs, one per Relying Party Instance. Each instance is identified by an optional `instanceId` in the order (see §5.2).
* **Co-issuance of WRPAC + WRPRC**: the ACME order MAY result in both a WRPAC and a WRPRC being issued together, as specified in the Blueprint and in CIR (EU) 2025/848 Annex V [2].
* **Certificate profile**: the issued certificate is an X.509 v3 WRPAC conforming to CIR 2025/848 Annex IV and ETSI TS 119 411-8 v1.1.1 [3], with attribute content as specified in ETSI TS 119 475 v1.2.1 clause 5 [4].
* **Certificate Transparency**: the ACME Server logs all issued certificates per RFC 9162 [7] (see §7.5 for deployment guidance).

All ACME messages are JSON payloads signed via JWS (RFC 7515 [8]), using JWK Thumbprints as specified in RFC 7638 [17], transported over HTTPS.

> [!NOTE]
> CS-RPAC_03: The choice of ACME provides a proven, standardised, and automatable protocol for certificate lifecycle management. It implements the integrated issuance workflow described in ETSI TS 119 475 v1.2.1 Annex D, Use Case 1 (see Section 9) while enabling interoperability testing with off-the-shelf ACME tooling. The RA and CA functions defined in the Blueprint are encapsulated within the ACME Server.

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
                       +--> registrationCertificate (URL)  [WE BUILD extension]
                |
                V
           authorization
                |
                V
           challenge
```

All standard ACME resource types and state transitions per RFC 8555 apply, with the extensions defined in §5.2, §5.3, and §5.4.

The `registrationCertificate` URL is a WE BUILD extension to the standard RFC 8555 order object. Consistent with the conventions used by RFC 8555 for the `finalize` and `certificate` URLs, `registrationCertificate` is a URL-valued top-level field of the order object and is dereferenced via an authenticated POST-as-GET request. Registration considerations are described in §7.9 (IANA Considerations).

## 5.2 WRPAC Identifier Type

**Type**: `wrp-id`

**Value**: the WRP's unique identifier as it appears in the WE BUILD RP Lists. For interoperability testing, the identifier format is defined by the mock Registrar. In the production eIDAS ecosystem, this would use CIR 2025/848 Annex I identifiers (EUID per CIR (EU) 2021/1042, LEI per CIR (EU) 2022/1860, EORI, national business register numbers, or VAT identification numbers).

**Example:**

```json
{
  "type": "wrp-id",
  "value": "NLKVK.12345678"
}
```

**Multi-instance issuance**: A single WRP identified by one `wrp-id` value MAY obtain multiple WRPACs, one per Relying Party Instance, in accordance with the Relying Party Instance model described in the EUDI Wallet ARF v2.8 [15]. Each order MAY include an optional `instanceId` string that uniquely identifies the specific Relying Party Instance within the WRP's deployment. When `instanceId` is provided:

* The ACME Server MUST verify that the `instanceId` is distinct from all other currently valid WRPACs issued to the same `wrp-id`.
* The issued WRPAC MAY include the `instanceId` in a non-critical Subject Alternative Name extension or in the Subject's Common Name at the CA's discretion.
* The RP List entry for the `wrp-id` MUST support multiple concurrent `acme-challenge` tokens, keyed by `instanceId` (see §7.8).

When `instanceId` is omitted, the ACME Server treats the order as targeting a single-instance deployment. If a valid WRPAC already exists for that `wrp-id` without an `instanceId`, the new order replaces the previous certificate; the ACME Server MUST initiate revocation of the superseded certificate upon successful issuance of the replacement (see §7.2 item 12).

## 5.3 Challenge Type: registrar-api-01

**Type**: `registrar-api-01`

**Mechanism:**

1. The ACME Server generates a random `token` and returns it as part of the challenge object.
2. The ACME Client constructs a `key-authorization` per RFC 8555 §8.1 [1]: `token || '.' || base64url(Thumbprint(accountKey))`, where `Thumbprint` is the JWK Thumbprint defined in RFC 7638 [17].
3. The ACME Client places the `key-authorization` as the `acme-challenge` attribute in its RP List entry. For multi-instance issuance, the value is placed under the key corresponding to the `instanceId` of the order (or `"default"` if no `instanceId` was specified).
4. The ACME Client signals readiness by POSTing to the challenge URL.
5. The ACME Server checks the RP List:
    * WRP is present and authorized
    * `acme-challenge` attribute (for the relevant `instanceId`) matches the expected `key-authorization`
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
> CS-RPAC_04: In the WE BUILD pilot, the RP Lists maintained by participating TSPs acting as mock Registrars replace the national register. The `registrar-api-01` challenge verifies presence in these lists (Blueprint step 5). In production, this would query the Registrar's API per EC TS5 [9] and EC TS6 [16].

## 5.4 EBW-based Account Binding

This profile extends ACME External Account Binding (RFC 8555 §7.3.4 [1]) with EBW authentication. This implements Blueprint steps 1-3.

**Mechanism:**

1. The RP representative authenticates to the RA using their EBW, presenting PID/EBWOID and a POA attestation (EAA).
2. The RA validates the POA and verifies the representative's authority.
3. The RA issues EAB credentials (Key ID + HMAC Key) bound to the verified identity and POA.
4. The ACME Client uses these EAB credentials during `newAccount`.

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
> CS-RPAC_05: **[MVP]** For initial interoperability testing, EBW authentication MAY be simulated. EAB credentials are pre-provisioned by the RA/TSP after out-of-band identity verification. **[MVP+]** Future iterations MUST implement the full EBW-based OID4VP authentication flow for EAB provisioning, including presentation of PID/EBWOID and POA (EAA) via OID4VP. Implementations declaring MVP+ conformance MUST support the full OID4VP-based EBW authentication flow.

# 6. High-level Flows

## 6.1 Directory Discovery

1. The ACME Client fetches the directory document via HTTPS GET.
2. The directory includes metadata: `externalAccountRequired: true`, `supportedIdentifierTypes: ["wrp-id"]`, `supportedChallengeTypes: ["registrar-api-01"]`.

## 6.2 Account Creation with EBW Authentication

**Pre-ACME phase (Blueprint steps 1-3):**

1. The RP representative connects to the TSP's RA portal/service.
2. **[MVP+]** The RA initiates an OID4VP request to the user's EBW, requesting PID/EBWOID and POA (EAA). **[MVP]** This step MAY be performed out-of-band.
3. The EBW presents the requested credentials.
4. The RA validates the POA and verifies the representative's authority.
5. Optionally (Blueprint step 4): the RA requests additional attributes for WRPRC production.
6. The RA issues EAB credentials to the user.

**ACME phase:**

7. The ACME Client generates an account key pair.
8. The ACME Client sends `newAccount` with the EAB binding.
9. The ACME Server validates the EAB and creates the account.

## 6.3 Order Creation

1. The ACME Client sends `newOrder` with one `wrp-id` identifier and an optional `instanceId`.
2. The ACME Server creates the order in `pending` state and returns authorization URL(s) and `finalize` URL.
3. For multi-instance issuance: the ACME Server MUST verify that the `instanceId` (if provided) is not already in use by a currently valid WRPAC for the same `wrp-id`.

## 6.4 Authorization and Challenge Validation

*Blueprint step 5: RP list check.*

1. The ACME Client fetches the authorization.
2. The ACME Client completes the `registrar-api-01` challenge: compute `key-authorization`, place in RP List (under the relevant `instanceId` key), signal readiness.
3. The ACME Server checks the RP List and validates.
4. Authorization transitions to `valid`.

## 6.5 Order Finalization

*Blueprint steps 6-9: order, issue, transmit, notify.*

1. The ACME Client generates a certificate key pair and CSR. Per §7.3 item 4, the ACME Client MUST generate a distinct key pair for each Relying Party Instance.
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
2. Server-initiated: upon RP removal from the RP List, or upon revocation of a specific Relying Party Instance.
3. For multi-instance deployments: revocation of one instance's WRPAC MUST NOT affect WRPACs issued to other instances of the same WRP.

# 7. Normative Requirements

## 7.1 Common Requirements

Both ACME Client and ACME Server **MUST**:

1. Implement the ACME protocol per RFC 8555 [1] with the extensions in §5.
2. Use HTTPS for all communication.
3. Use JWS (RFC 7515 [8]) for all request payloads, with JWK Thumbprints computed per RFC 7638 [17] where required by ACME.
4. Implement nonce-based replay protection.

## 7.2 ACME Server (CA / RA)

The ACME Server **MUST**:

1. Publish an ACME directory at a well-known URL (see §7.9 for IANA considerations).
2. Require EAB for all accounts (RFC 8555 §7.3.4 [1]).
3. Support `wrp-id` identifiers and `registrar-api-01` challenges.
4. Verify WRP presence in the WE BUILD RP Lists during challenge validation (Blueprint step 5).
5. Reject authorization if the WRP is not in the list or identity data is inconsistent.
6. Issue WRPACs exclusively to authorized WRPs.
7. Support the order state transitions defined in RFC 8555 §7.1.6 "Status Changes" [1].
8. Support `revokeCert`.
9. Implement the RA function: POA validation (Blueprint steps 1-3) and RP List check (step 5).
10. Support multi-instance issuance: accept an optional `instanceId` in orders, verify its uniqueness among active WRPACs for the same `wrp-id`, and issue separate WRPACs per instance (§5.2).
11. Enforce that each Relying Party Instance receives a distinct WRPAC bound to a distinct key pair (see §7.3 item 4).
12. Upon successful replacement of a single-instance WRPAC (new order without `instanceId` replacing an existing single-instance WRPAC), MUST initiate revocation of the superseded certificate (see §5.2).

The ACME Server **SHOULD**:

1. Support co-issuance of WRPRC alongside WRPAC in a single order (WRPRC profile per CIR (EU) 2025/848 Annex V [2]).
2. Send out-of-band notification when certificates are ready (Blueprint step 9).
3. Support `keyChange`.

## 7.3 ACME Client (WRP / EBW)

The ACME Client **MUST**:

1. Perform directory discovery.
2. Support EAB using credentials obtained through EBW authentication.
3. Support `wrp-id` identifiers and `registrar-api-01` challenges.
4. Generate a distinct key pair per Relying Party Instance and construct valid CSRs per §7.4. For single-instance issuance, a single key pair applies; for multi-instance issuance, a distinct key pair MUST be used for each `instanceId`. This is the single normative key-separation rule applied by both the Client and the Server (see §7.2 item 11).
5. Validate the returned certificate chain.
6. Support `revokeCert`.

The ACME Client **SHOULD**:

1. Integrate with the EBW for authentication during EAB provisioning (REQUIRED for MVP+ conformance).
2. Include an `instanceId` in orders for multi-instance deployments.
3. Clean up `acme-challenge` entries from the RP List after successful issuance or upon authorization failure.

## 7.4 Certificate Profile

Issued WRPACs **MUST**:

1. Be X.509 v3 public-key certificates conforming to RFC 5280 [10].
2. Comply with ETSI TS 119 411-8 v1.1.1 [3] (Access Certificate Policy for EUDI Wallet Relying Parties), which in turn applies the NCP policy as specified in ETSI EN 319 411-1 v1.5.1 [12] and the WRPAC-specific policy identifiers `NCP-n-eudiwrp` (natural person) and `NCP-l-eudiwrp` (legal person).
3. Contain the WRP's legal name in the Subject field (CIR 2025/848 Annex I point 1 [2]).
4. Contain a user-friendly name where applicable (Annex I point 2).
5. Contain at least one unique WRP identifier (Annex I point 3), selected from EUID, LEI, EORI, national business register number, or VAT identification number.
6. Include a certificate policy OID (Annex IV).
7. Include certification path information (URI).
8. Include a SAN extension (DNS name or URI).
9. Include registration information per Annex I points 1, 2, and 8.
10. Express attribute content (e.g. `organizationIdentifier`, semantic identifiers) using the Subject DN and certificate-extension attributes defined in ETSI EN 319 412-1 [18] and ETSI TS 119 475 v1.2.1 clause 5 [4].
11. Conform to ETSI TS 119 475 v1.2.1 [4].
12. Use RSA (min. 3072 bits), ECDSA (P-256 or P-384), SHA-256 or stronger.
13. Have a validity period of **one year** from the date of issuance. Shorter validity periods are NOT used in WE BUILD interoperability testing.

> [!NOTE]
> CS-RPAC_06: For interoperability testing, implementations SHOULD support both RSA and ECDSA. NCP as defined in ETSI EN 319 411-1 v1.5.1 [12] is the baseline policy level, with the WRPAC-specific extensions of TS 119 411-8 v1.1.1 [3] applied on top. The one-year validity period applies uniformly in the WE BUILD ITB+ test environment.

> [!NOTE]
> CS-RPAC_07: WRPACs are X.509 public-key certificates; they are not X.509 Attribute Certificates. Attribute content in WRPACs is expressed through public-key certificate extensions and ETSI-defined Subject DN attributes (ETSI EN 319 412 series [18], ETSI TS 119 475 v1.2.1 clause 5 [4]). The Attribute Certificate profile defined in RFC 5755 is therefore not applicable to WRPACs and is not used in this specification.

## 7.5 Certificate Transparency

The ACME Server **MUST** log all WRPACs in CT logs and embed SCTs.

> [!NOTE]
> CS-RPAC_08: RFC 9162 [7] ("Certificate Transparency Version 2.0", Experimental, December 2021) is the current IETF specification for CT and obsoletes RFC 6962. However, virtually all production CT log operators and browser CT policies currently implement RFC 6962. For interoperability testing in WE BUILD ITB+, implementations MAY use test CT logs and MAY rely on RFC 6962 where production tooling is not yet available for RFC 9162. Implementations MUST document which CT specification they implement.

## 7.6 Revocation

The ACME Server **MUST** support client-initiated (`revokeCert`) and server-initiated revocation (RP List removal or instance-specific revocation), and publish status via OCSP and/or CRL.

For multi-instance deployments, revocation of one instance's WRPAC MUST be scoped to that instance and MUST NOT affect WRPACs issued to other instances of the same WRP.

> [!NOTE]
> CS-RPAC_09: For interoperability testing, RP List removal MAY be simulated.

## 7.7 Trusted List Integration

1. The test environment MUST include a simulated Trusted List containing the trust anchor certificate(s) of the CA(s) participating in the WE BUILD pilot. Individual WRPAC end-entity certificates are NOT listed in the Trusted List; trust is established through the CA trust anchor chain.
2. Wallet Units MUST verify WRPACs by building and validating the certificate chain up to a CA trust anchor present in the Trusted List.

## 7.8 WE BUILD RP Lists

In the WE BUILD pilot, participating TSPs acting as mock Registrars establish and maintain the Lists of authorized Relying Parties, in accordance with the Blueprint [5] MVP governance model. This is the functional equivalent of the national register of wallet-relying parties.

1. The ACME Server MUST check these lists as a precondition for issuance.
2. The RP List MUST support an `acme-challenge` metadata structure that accommodates multiple concurrent challenge tokens keyed by `instanceId`, to support multi-instance issuance.
3. In the absence of multi-instance ordering, the `acme-challenge` attribute MAY be a single string value (equivalent to `instanceId = "default"`).

Each RP List entry MUST contain at minimum:

* WRP unique identifier
* WRP legal name
* Authorization status (active / revoked)
* Metadata fields including `acme-challenge`, structured as follows:

```json
{
  "acme-challenge": {
    "default": "<key-authorization for single-instance or unnamed order>",
    "instance-A": "<key-authorization for instance-A>",
    "instance-B": "<key-authorization for instance-B>"
  }
}
```

For single-instance deployments, the following shorthand form is also valid:

```json
{
  "acme-challenge": "<key-authorization>"
}
```

The ACME Server MUST accept both forms and normalize them internally.

## 7.9 IANA Considerations

This specification defines extensions to the ACME protocol that fall within IANA registries established by RFC 8555 and its successors, and introduces a custom URI suffix. For interoperability-testing purposes within WE BUILD ITB+, registration is not a prerequisite; for any future production use, the following registrations would be required.

**ACME Identifier Types registry** (established by RFC 8555): the identifier type `wrp-id` (§5.2) would need to be registered.

**Well-Known URI registry** (RFC 8615 [19]): the URI suffix `acme-eudi-wrpac` (§8.1) would need to be registered if the `/.well-known/` prefix is used. Alternatively, since RFC 8555 does not mandate the use of `/.well-known/` for the ACME directory, a conventional (non-`.well-known/`) path MAY be used, as shown in §8.1. Implementations intending to place the ACME directory under `/.well-known/acme-eudi-wrpac/` MUST complete the RFC 8615 registration process.

**ACME directory metadata extensions**: the metadata fields `rprcCoIssuanceSupported` and `multiInstanceIssuanceSupported` (§8.1) are WE BUILD-specific extensions. The IANA "ACME Directory Metadata Fields" registry (established by RFC 8555) would need to be updated for any production deployment.

**ACME order object extension**: the `registrationCertificate` URL field (§5.1, §8.5) is a WE BUILD-specific extension to the standard ACME order object. For production deployment, a URN-style field name (for example, `urn:webuild:acme:wrprc`) MAY be preferred to avoid conflicts with future IETF extensions.

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
    "supportedChallengeTypes": ["registrar-api-01"],
    "rprcCoIssuanceSupported": true,
    "multiInstanceIssuanceSupported": true
  }
}
```

> [!NOTE]
> CS-RPAC_10: `rprcCoIssuanceSupported` and `multiInstanceIssuanceSupported` are WE BUILD extensions to the ACME directory metadata. The former indicates the server can co-issue WRPAC and WRPRC; the latter indicates support for per-instance issuance per the ARF v2.8 Relying Party Instance model [15]. Registration considerations for these extensions are described in §7.9.

## 8.2 Account Management with EBW/POA

* **Method**: `POST` (JWS-signed)

**Pre-condition**: EBW authentication + POA validation completed; EAB credentials received.

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

**Order states** (per RFC 8555 §7.1.6 "Status Changes" [1]): `pending` → `ready` → `processing` → `valid` (or `invalid`).

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

The ACME Client places the computed `key-authorization` in the RP List entry's `acme-challenge` structure under the key matching the `instanceId` of the order (or `"default"` if no `instanceId` was specified), before signalling readiness.

## 8.5 Finalize and Certificate

**Finalize:**

```json
{ "csr": "<base64url DER-encoded PKCS#10 CSR>" }
```

**Order with co-issued WRPRC (WE BUILD extension):**

```json
{
  "status": "valid",
  "identifiers": [
    { "type": "wrp-id", "value": "NLKVK.12345678" }
  ],
  "instanceId": "production-eu-west-1",
  "certificate": "https://acme.example/cert/cert012",
  "registrationCertificate": "https://acme.example/rprc/rprc012",
  "finalize": "https://acme.example/order/ord456/finalize",
  "authorizations": ["https://acme.example/authz/xyz789"]
}
```

The `registrationCertificate` field is a WE BUILD extension to the standard RFC 8555 order object. Like the standard `finalize` and `certificate` fields, it is a URL-valued top-level field of the order object and is dereferenced via an authenticated POST-as-GET. The `instanceId` field in the order response echoes the value from the order request.

**Certificate download**: `application/pem-certificate-chain` per RFC 8555 §7.4.2 [1] (end-entity first).

## 8.6 Revocation

```json
{ "certificate": "<base64url DER-encoded certificate>", "reason": 0 }
```

For multi-instance deployments, revocation targets the specific certificate identified by the DER-encoded value. Other WRPACs issued to the same `wrp-id` are unaffected.

# 9. Conformance

An implementation **conforms as an ACME Server (TSP: RA + CA)** if it:

1. Implements ACME per RFC 8555 [1] with the extensions in §5.
2. Publishes an ACME directory per §8.1.
3. Requires EAB with EBW/POA verification (§5.4).
4. Supports `wrp-id` identifiers and `registrar-api-01` challenges.
5. Verifies WRP presence in WE BUILD RP Lists (§7.8).
6. Issues certificates per §7.4, including compliance with ETSI TS 119 411-8 v1.1.1 [3] and the attribute mapping in ETSI TS 119 475 v1.2.1 clause 5 [4].
7. Logs to CT logs (§7.5).
8. Supports revocation (§7.6).
9. Implements RA function: POA validation + RP List checks (§7.2).
10. Supports multi-instance issuance per §5.2, §7.2, and §8.3.
11. Implements interfaces per §8.

An implementation **conforms as an ACME Client (WRP / EBW)** if it:

1. Implements ACME per RFC 8555 [1] with the extensions in §5.
2. Supports EBW-based EAB provisioning (§5.4).
3. Creates accounts with EAB, orders with `wrp-id` (and optional `instanceId`), and completes `registrar-api-01` challenges.
4. Submits valid CSRs with distinct key pairs per instance, and validates certificate chains.
5. Supports revocation.

An implementation **conforms as a test environment** if it:

1. Provides WE BUILD RP Lists with `acme-challenge` metadata supporting both single-value and multi-instance (`instanceId`-keyed) formats.
2. Provides a simulated Trusted List containing CA trust anchor certificate(s).
3. Provides a CT log (or test equivalent).
4. Supports EAB provisioning (or simulation per MVP scope).
5. Supports automated full-lifecycle testing, including multi-instance issuance scenarios.

An **MVP+ conformant** implementation additionally:

1. Implements the full OID4VP-based EBW authentication flow for EAB provisioning (§5.4, §6.2).
2. Accepts PID/EBWOID and POA (EAA) as presented via the EBW during the pre-ACME authentication phase.

Profiles for specific WE BUILD credential types MUST NOT relax these requirements.

**Mapping of the WE BUILD Blueprint issuance workflow (derived from ETSI TS 119 475 v1.2.1 Annex D, Use Case 1: Integrated model [4]) to ACME protocol operations:**

| Blueprint Step | Description | ACME Operation | Section |
|---|---|---|---|
| **1** | User authenticates to RA using EBW | EBW authentication → EAB provisioning | §5.4, §8.2 |
| **2** | RA requests credentials | OID4VP request from RA to EBW [MVP+] | §5.4 |
| **3** | User supplies EAA (POA) | EBW presents POA to RA | §5.4 |
| **4** | RA requests additional WRPRC attributes | Collected during EAB provisioning or as order metadata | §8.3 |
| **5** | RA checks RP in authorized RP lists | `registrar-api-01` challenge validation | §6.4, §8.4 |
| **6** | RA orders issuance of both certificates | ACME `finalize` (CSR submission) | §8.5 |
| **7** | CA issues WRPAC and WRPRC | ACME Server generates certificates, order → `valid` | §8.5 |
| **8** | CA transmits certificates to RA | Internal (ACME Server encapsulates RA+CA) | — |
| **9** | RA notifies user (e.g. by email) | Order polling: status → `valid`. Optional out-of-band notification. | §8.5 |
| **10** | User authenticates via EBW | Certificate download authenticated via JWS-signed POST-as-GET (account key bound to EBW via EAB) | §8.6 |
| **11** | User retrieves WRPAC and WRPRC | ACME certificate download from `certificate` URL | §8.6 |

> [!NOTE]
> CS-RPAC_11: The table above maps the eleven-step workflow used by the WE BUILD Blueprint [5] — which is derived from the integrated issuance model described in ETSI TS 119 475 v1.2.1 Annex D, Use Case 1 [4] — to the ACME protocol operations defined by this specification. ETSI TS 119 475 Annex D is informative and presents four use cases (D.1 Integrated model, D.2 Registrar-initiated, D.3 RP-initiated, D.4 Provider-assisted); the eleven discrete steps enumerated above are a WE BUILD refinement of the D.1 flow and are not themselves a normative ETSI enumeration.

**Key design decisions:**

* **Steps 1-3** (EBW auth + POA) are a **pre-ACME phase** producing EAB credentials. This cleanly separates human authentication from the machine protocol. Full OID4VP-based EBW authentication is required for MVP+ conformance.
* **Step 4** (WRPRC attributes) is collected either during EAB provisioning or as ACME order metadata.
* **Step 5** (RP list check) maps directly to the `registrar-api-01` challenge.
* **Steps 6-8** (order, issue, transmit) map to ACME `finalize` → `processing` → `valid`.
* **Steps 9-11** (notify, auth, retrieve) map to order polling and certificate download, with optional email notification.

> [!NOTE]
> CS-RPAC_12: The Blueprint specifies RA and CA as separate actors. In this ACME profile they are encapsulated in a single endpoint. Implementations MAY separate them internally. This is consistent with real-world ACME CAs where the RA front-end and CA signing backend are separate systems behind one protocol interface.

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