# WE BUILD - Conformance Specification: EBW–QTSP DIDComm Interface

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language](#3-normative-language)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
- [Part 1: did:euid Method](#part-1-dideuid-method)
  - [6. did:euid Method Specification](#6-dideuid-method-specification)
  - [7. DID Document Structure](#7-did-document-structure)
  - [8. did:euid Registration](#8-dideuid-registration)
  - [9. did:euid Resolution](#9-dideuid-resolution)
  - [10. Normative Requirements - did:euid](#10-normative-requirements--dideuid)
- [Part 2: DIDComm over QTSP](#part-2-didcomm-over-qtsp)
  - [11. QTSP Metadata Discovery](#11-qtsp-metadata-discovery)
  - [12. Subscriber Onboarding and Registration](#12-subscriber-onboarding-and-registration)
    - [12.5 Token Renewal for Registered Subscribers](#125-token-renewal-for-registered-subscribers)
    - [12.6 Key Rotation for Registered Subscribers](#126-key-rotation-for-registered-subscribers)
  - [13. DIDComm Transport](#13-didcomm-transport)
  - [14. Message Submission Flow](#14-message-submission-flow)
  - [15. Message Reception Flow](#15-message-reception-flow)
  - [16. DIDComm Message Types](#16-didcomm-message-types)
  - [17. Normative Requirements - DIDComm over QTSP](#17-normative-requirements--didcomm-over-qtsp)
- [Part 3: WACI-DIDComm Credential Interactions](#part-3-waci-didcomm-credential-interactions)
  - [18. Overview](#18-overview)
    - [18.1 Transport and Encryption Model](#181-transport-and-encryption-model)
    - [18.2 Thread Continuity and Evidence Correlation](#182-thread-continuity-and-evidence-correlation)
  - [19. Credential Issuance over QERDS](#19-credential-issuance-over-qerds)
    - [19.1 Credential Issuance Flow](#191-credential-issuance-flow)
    - [19.2 QERDS Audit Trail for Issuance](#192-qerds-audit-trail-for-issuance)
  - [20. Credential Presentation over QERDS](#20-credential-presentation-over-qerds)
    - [20.1 Credential Presentation Flow](#201-credential-presentation-flow)
    - [20.2 QERDS Audit Trail for Presentation](#202-qerds-audit-trail-for-presentation)
- [21. Interface Definitions](#21-interface-definitions)
  - [21.1 QTSP Metadata Endpoint](#211-qtsp-metadata-endpoint)
  - [21.2 Onboarding Endpoint](#212-onboarding-endpoint)
  - [21.3 Token Renewal Endpoint](#213-token-renewal-endpoint)
  - [21.4 DIDComm WebSocket Endpoint](#214-didcomm-websocket-endpoint)
  - [21.5 DIDComm HTTPS POST Endpoint](#215-didcomm-https-post-endpoint)
  - [21.6 DIDComm Inbox Polling Endpoint](#216-didcomm-inbox-polling-endpoint)
  - [21.7 DIDComm Inbox Acknowledgement](#217-didcomm-inbox-acknowledgement)
- [22. Conformance](#22-conformance)
- [23. Security Considerations](#23-security-considerations)
- [References](#references)

---

# 1. Introduction

This document defines the **WE BUILD Conformance Specification for the European Business Wallet (EBW)–QTSP Interface** (WBCS-004).

It specifies how a European Business Wallet interacts with a Qualified Trust Service Provider (QTSP) offering a Qualified Electronic Registered Delivery Service (QERDS), using DIDComm Messaging v2.1 as the wallet-facing communication protocol and `did:euid` as the decentralized identifier method for EBW subscribers.

The specification covers the **optional API access protocol** mandated by the ADR as an abstraction layer between the EBW and the QERDS, and is one of the Conformance Specifications required by the ADR's consequences section. It additionally specifies how credential issuance and presentation are performed between EBWs using WACI-DIDComm [WACI-DIDCOMM] over the QERDS channel.

This specification is based on the [WE BUILD ADR: Deliver business wallet data using QERDS](https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/build-qerds.md), the [WE BUILD QERDS Architecture](https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qerds/architecture.md), the [WE BUILD QERDS Interoperability Framework](https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qerds/interop-framework.md), and [WBCS-002: Credential Presentation](cs-02-credential-presentation.md).

# 2. Scope

This specification covers:

- Discovery of QTSP DIDComm metadata by the EBW
- Subscriber onboarding and identity verification using OpenID4VP (per WBCS-002)
- Establishment and maintenance of a DIDComm channel between the EBW and the QTSP
- Message submission by the EBW (Interface 14 - Data submission)
- Credential issuance between EBWs using WACI-DIDComm Issue Credential 3.0
- Credential presentation between EBWs using WACI-DIDComm Present Proof 3.0
- Message notification and data delivery to the EBW (Interface 10 - Data transmission)
- QERDS evidence delivery to the EBW (Interface 11 - Evidence transmission)
- Consignment identity verification at the recipient EBW (Interface 4 - Identity verification)
- The `did:euid` decentralised identifier method: syntax, document structure, registration, and resolution

This specification covers the **EBW–QTSP** leg of the four-corner QERDS model only. QTSP-to-QTSP message relay (Interface 16) is out of scope and is governed by the eDelivery AS4 profile specified separately. EU Digital Directory (EDD) operator requirements are out of scope.

**Out of scope:**
- Internal QTSP services (QESeal creation, QTS creation, Evidence creation - Interfaces 5–9)
- AS4 inter-QTSP relay (Interface 16)
- EUDIW-to-QERDS interface
- Gateway flows to legacy systems (Peppol, OOTS)
- Group messaging and multi-party encryption

# 3. Normative Language

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as described in [RFC 2119].

# 4. Roles and Components

| Role | Description |
|---|---|
| **European Business Wallet (EBW)** | Software acting on behalf of a business (the Subscriber), implementing both wallet and QERDS subscriber capabilities. Referred to as the EBW or wallet throughout this specification. |
| **Subscriber** | The legal entity (business) that owns and controls the EBW. Identified by a European Unique Identifier (EUID). |
| **QTSP** | A Qualified Trust Service Provider offering a QERDS to Subscribers. Acts as QERDS provider and, during onboarding, as Verifier of the Subscriber's identity credentials. |
| **QERDS** | The Qualified Electronic Registered Delivery Service provided by the QTSP. |
| **WE BUILD Discovery Infrastructure** | The discovery service operated by WP4 Trust Registry Infrastructure enabling EUID-to-QTSP endpoint resolution. |
| **Identity Proofing Service (IPS)** | An internal QTSP service responsible for identity verification using credential presentations. Acts as OpenID4VP Verifier. |
| **Sender EBW** | The EBW initiating a QERDS message submission. |
| **Recipient EBW** | The EBW designated to receive a QERDS message. |

# 5. Protocol Overview

This specification defines the EBW–QTSP interface within the QERDS four-corner model:

```mermaid
graph LR
    S_EBW["Sender EBW"]
    S_QTSP["Sender QTSP"]
    R_QTSP["Recipient QTSP"]
    R_EBW["Recipient EBW"]

    S_EBW <-->|DIDComm| S_QTSP
    S_QTSP <-->|AS4| R_QTSP
    R_QTSP <-->|DIDComm| R_EBW
```

The wallet never communicates with another wallet or another QTSP directly. All QERDS interactions are mediated by the Subscriber's own QTSP.

**DIDComm Messaging v2.1** [DIDComm] is used for the EBW–QTSP leg. DIDComm provides:
- Application-layer end-to-end encryption independent of the transport layer (TLS)
- Multi-transport support (WebSocket and HTTP POST)
- A cryptographic identity model compatible with decentralized identifiers
- A clear path toward post-quantum algorithm migration via crypto-agility

**OpenID4VP** (per WBCS-002) is used for identity verification during Subscriber onboarding and token renewal, to establish the identity of the EBW owner. The resulting Bearer access token is short-lived (≤1 hour) and serves as proof of identity for all subsequent message exchanges within its validity period.

**`did:euid`** is the identifier method for EBW Subscribers. A `did:euid` deterministically encodes a business's EUID and resolves to a DID Document containing the EBW's public keys and DIDComm service endpoint. Resolution is delegated to the QTSP, which queries the WE BUILD discovery infrastructure on the EBW's behalf.

---

# Part 1: did:euid Method

## 6. did:euid Method Specification

### 6.1 Method Name

The method name is `euid`.

### 6.2 DID Syntax

A `did:euid` identifier has the following syntax (ABNF):

```
did-euid     = "did:euid:" euid-string
euid-string  = country-code national-id "." register-id [ "." local-id ]
country-code = 2ALPHA
national-id  = 1*( ALPHA / DIGIT )
register-id  = 1*( ALPHA / DIGIT )
local-id     = 1*( ALPHA / DIGIT / "-" / "_" )
```

The EUID format follows ISO 6523 [ISO-6523] and the BRIS (Business Registers Interconnection System) standard [BRIS]. The `euid-string` **MUST** be the entity's official EUID as registered in the national business register and interconnected via BRIS.

**Examples:**

| Entity | EUID | DID |
|---|---|---|
| German company, Berlin register | `DEK1101R.HRB116737` | `did:euid:DEK1101R.HRB116737` |
| Swedish company | `SE5560188240.BO` | `did:euid:SE5560188240.BO` |
| Dutch company | `NL813384960.KVK` | `did:euid:NL813384960.KVK` |

### 6.3 EUID Namespace and Uniqueness

EUID uniqueness is guaranteed by the BRIS interconnection of national business registers across EU Member States [BRIS]. No two registered legal entities share an EUID. The `did:euid` method therefore inherits BRIS's uniqueness guarantees and does not require a separate uniqueness mechanism.

---

## 7. DID Document Structure

A `did:euid` DID Document represents the EBW's cryptographic identity and the QTSP endpoint through which it is reachable. The document structure follows the W3C DID Core specification [DID-CORE].

### 7.1 Full DID Document Example

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1",
    "https://didcomm.org/messaging/contexts/v2"
  ],
  "id": "did:euid:DEK1101R.HRB116737",
  "verificationMethod": [
    {
      "id": "did:euid:DEK1101R.HRB116737#key-agreement-1",
      "type": "JsonWebKey2020",
      "controller": "did:euid:DEK1101R.HRB116737",
      "publicKeyJwk": {
        "kty": "OKP",
        "crv": "X25519",
        "x": "<base64url>"
      }
    },
    {
      "id": "did:euid:DEK1101R.HRB116737#assertion-key-1",
      "type": "JsonWebKey2020",
      "controller": "did:euid:DEK1101R.HRB116737",
      "publicKeyJwk": {
        "kty": "EC",
        "crv": "P-256",
        "x": "<base64url>",
        "y": "<base64url>"
      }
    },
    {
      "id": "did:euid:DEK1101R.HRB116737#auth-key-1",
      "type": "JsonWebKey2020",
      "controller": "did:euid:DEK1101R.HRB116737",
      "publicKeyJwk": {
        "kty": "EC",
        "crv": "P-256",
        "x": "<base64url>",
        "y": "<base64url>"
      }
    }
  ],
  "keyAgreement": [
    "did:euid:DEK1101R.HRB116737#key-agreement-1"
  ],
  "assertionMethod": [
    "did:euid:DEK1101R.HRB116737#assertion-key-1"
  ],
  "authentication": [
    "did:euid:DEK1101R.HRB116737#auth-key-1"
  ],
  "service": [
    {
      "id": "did:euid:DEK1101R.HRB116737#didcomm",
      "type": "DIDCommMessaging",
      "serviceEndpoint": {
        "uri": "urn:webuild:qerds:v1",
        "routingKeys": [],
        "accept": ["didcomm/v2"]
      }
    }
  ]
}
```

### 7.2 Verification Methods and Relationships

| Verification relationship | Key type | Requirement | Notes |
|---|---|---|---|
| `keyAgreement` | ECDH-compatible: `OKP` (X25519) or `EC` (P-256, P-384, P-521) | SHOULD | JWE key agreement. Required if the EBW participates in WACI-DIDComm as Holder or Recipient - Sender EBWs use this key to encrypt inner payloads (Sections 18–22). |
| `assertionMethod` | Signing-capable: `EC` (P-256, P-384, P-521) or `OKP` (Ed25519) | MAY | Only needed if signing SD-JWT-VCs with a DID key. Not required for X.509/QESeal-based signing. |
| `authentication` | Signing-capable: `EC` (P-256, P-384, P-521) or `OKP` (Ed25519) | MAY | Only needed for DIDComm Signed Messages (Section 13.4). |

> **`cnf.jwk` keys:** The per-credential key pair generated during `request-credential` (Section 19.1) is a holder binding key separate from the entries above and is not published in the DID Document.

### 7.3 DIDCommMessaging Service Endpoint

The `DIDCommMessaging` service is **MUST**. It signals that this EBW is reachable via QERDS and that routing is handled by the WE BUILD discovery infrastructure.

| Field | Requirement | Notes |
|---|---|---|
| `id` | MUST | `did:euid:<euid>#didcomm` by convention |
| `type` | MUST | Must equal `DIDCommMessaging` |
| `serviceEndpoint.uri` | MUST | **MUST** be set to the reserved value `urn:webuild:qerds:v1` |
| `serviceEndpoint.accept` | SHOULD | `["didcomm/v2"]` |

---

## 8. did:euid Registration

Registration of a `did:euid` is performed as part of Subscriber onboarding (Section 12). After successfully verifying the Subscriber's identity and receiving their public key, the QTSP registers the Subscriber's `did:euid`, public key, and its own DIDComm endpoint in the WE BUILD discovery infrastructure on the Subscriber's behalf.

The internal mechanism of this registration - the discovery infrastructure's API, data format, and trust model - is **out of scope** for this specification and is governed by a separate WE BUILD Trust Registry Infrastructure specification.

The `did:euid` is considered **active** once the QTSP has confirmed registration in the discovery infrastructure and the QTSP is listed on the Trusted List as a qualified TSP.

The QTSP **MUST**:
- Register the Subscriber's `did:euid` within the onboarding transaction before issuing the access token.
- Include the Subscriber's key agreement public key and the QTSP's DIDComm endpoint URI in the registration entry.
- Update the registration entry within 24 hours of any Subscriber key rotation or QTSP endpoint change.

---

## 9. did:euid Resolution

An EBW **SHOULD** delegate `did:euid` resolution to its QTSP. The QTSP resolves the identifier via the WE BUILD discovery infrastructure and returns a DID Document. The resolution mechanism used internally by the QTSP is **out of scope** for this specification.

### 9.1 Resolution Flow

```mermaid
sequenceDiagram
    participant EBW as EBW
    participant QTSP as QTSP
    participant DI as Discovery Infrastructure

    EBW->>QTSP: DIDComm: ebw/resolve-did/1.0<br>{ did: "did:euid:DEK1101R.HRB116737" }

    QTSP->>DI: Resolve EUID
    DI-->>QTSP: Subscriber record<br>{ public_key_jwk, didcomm_endpoint, valid_until }

    QTSP->>QTSP: Construct DID Document

    QTSP-->>EBW: DIDComm: ebw/resolve-did-response/1.0<br>{ did_document, resolved_at, valid_until }

    note over EBW: EBW verifies DID Document structure
```

### 9.2 Resolution Message Types

**ebw/resolve-did/1.0** (EBW -> QTSP):
```json
{
  "type": "https://webuild.example/didcomm/ebw/resolve-did/1.0",
  "id": "<uuid>",
  "from": "did:euid:<resolver_euid>",
  "to": ["<qtsp_did>"],
  "body": {
    "did": "did:euid:<target_euid>"
  }
}
```

**ebw/resolve-did-response/1.0** (QTSP -> EBW):
```json
{
  "type": "https://webuild.example/didcomm/ebw/resolve-did-response/1.0",
  "id": "<uuid>",
  "thid": "<request_message_id>",
  "from": "<qtsp_did>",
  "to": ["did:euid:<resolver_euid>"],
  "body": {
    "did_document": { "...": "..." },
    "resolved_at": 1234567890,
    "valid_until": 1234567890
  }
}
```

If resolution fails (unknown EUID, expired entry, unreachable discovery infrastructure), the QTSP **MUST** respond with an `ebw/problem-report/1.0` message instead.

---

## 10. Normative Requirements - did:euid

### 10.1 QTSP Requirements

The QTSP **MUST**:

1. Register each Subscriber's `did:euid`, public key, and DIDComm endpoint in the WE BUILD discovery infrastructure within the onboarding transaction.
2. Update the registration entry within 24 hours of any key rotation or endpoint change.
3. Support the `ebw/resolve-did/1.0` message type and return a valid DID Document for any registered `did:euid`.
4. Return an `ebw/problem-report/1.0` if the target `did:euid` cannot be resolved or its registration has expired.
5. Not serve DID Documents whose `valid_until` has passed.

### 10.2 EBW Requirements

The EBW **MUST**:

1. Use the `did:euid` of the intended Recipient when addressing WACI-DIDComm messages.
2. Verify that the `id` field of a resolved DID Document matches the requested `did:euid` exactly before using its key material or service endpoint.

The EBW **SHOULD**:

1. Cache resolved DID Documents until their `valid_until` time, but not beyond.
2. Re-resolve a `did:euid` before sending a message if the cached DID Document has expired.

---

# Part 2: DIDComm over QTSP

## 11. QTSP Metadata Discovery

Before onboarding, the EBW retrieves the QTSP's connection metadata from a well-known endpoint.

### 11.1 Discovery Flow

```mermaid
sequenceDiagram
    participant EBW as EBW
    participant QTSP as QTSP

    EBW->>QTSP: GET /.well-known/qtsp-configuration
    QTSP-->>EBW: QTSP Metadata (JSON)
```

### 11.2 QTSP Metadata Document

The QTSP **MUST** serve a JSON metadata document at `/.well-known/qtsp-configuration` over HTTPS. The document **MUST** include:

| Field                       | Type | Description |
|-----------------------------|---|---|
| `qtsp_id`                   | string | QTSP's EUID or TSL identifier |
| `qtsp_did`                  | string | The QTSP's DID (used as DIDComm recipient for outbound messages) |
| `didcomm_endpoint`          | string | WSS and/or HTTPS POST URI for DIDComm messages |
| `onboarding_endpoint`       | string | URI to initiate the OpenID4VP onboarding flow |
| `token_endpoint`            | string | URI to obtain a refreshed access token for an already-registered Subscriber |
| `key_rotation_endpoint`     | string | URI to initiate a key rotation for an already-registered Subscriber |
| `identity_proofs_supported` | array | Credential types accepted for identity proofing (e.g. `PID`, `EBWOID`) |

**Example:**

```json
{
  "qtsp_id": "DEK1101R.QTSP001",
  "qtsp_did": "did:web:qtsp.example",
  "didcomm_endpoint": "wss://qtsp.example/didcomm",
  "onboarding_endpoint": "https://qtsp.example/onboarding",
  "token_endpoint": "https://qtsp.example/token",
  "key_rotation_endpoint": "https://qtsp.example/keys/rotate",
  "identity_proofs_supported": ["PID", "EBWOID"]
}
```

The QTSP **MUST** serve the metadata document as a signed JWT (JWS compact serialization), signed with a key from its qualified certificate or TSL entry. The `Content-Type` of the response **MUST** be `application/jwt`. The EBW **MUST** verify the JWT signature against the QTSP's TSL entry before using the metadata.

> The QTSP has its own DID, used as the `from` field when sending DIDComm messages to the EBW (e.g. `ebw/erds-evidence/1.0`, Section 16.3). For simplicity the `did:web` method is used for QTSP DIDs.

---

## 12. Subscriber Onboarding and Registration

Onboarding is a one-time process in which the Subscriber's identity is verified and a DIDComm channel is established. It uses the OpenID4VP credential presentation flow specified in WBCS-002, with the QTSP acting as Verifier.

### 12.1 Onboarding Flow

```mermaid
sequenceDiagram
    participant EBW as EBW
    participant IPS as QTSP Identity Proofing Service<br>(OpenID4VP Verifier)
    participant QTSP as QTSP (QERDS)

    note over EBW: EBW generates key pair<br>(EUID keypair for did:euid)

    EBW->>IPS: POST /onboarding/start<br>{ ebw_did_key: <public_key_jwk> }
    IPS-->>EBW: OpenID4VP Authorization Request<br>(per WBCS-002, nonce, response_uri)

    note over EBW: EBW selects PID or EBWOID<br>containing company EUID

    EBW->>IPS: OpenID4VP VP Token Response<br>(SD-JWT-VC, signed)
    IPS->>IPS: Verify VP Token<br>Extract EUID from credential

    IPS-->>EBW: Onboarding Response<br>{ subscriber_did, access_token, token_expiry }

    QTSP->>QTSP: Register subscriber in discovery infrastructure
    
    note over EBW,QTSP: Subscriber registered.<br>did:euid:<EUID> now resolvable.
```

### 12.2 Onboarding Request

The EBW **MUST** include its public key in the onboarding request. This key will appear as the `verificationMethod` in the EBW's `did:euid` DID Document. Keys **SHOULD** be generated inside a hardware-backed secure element or WSCA/QSCD. The EBW **SHOULD** register keys for the verification relationships defined in Section 7.2 as needed for its role.

### 12.3 Identity Verification Requirements

The identity proofing requirements for onboarding are further specified in the WP4 QTSP group specification [QTSP-SPEC]. The QTSP **MUST** require the EBW to present a credential containing the Subscriber's EUID. Accepted credential types:

- **PID** (Person Identification Data) - for natural-person-operated EBWs
- **EBWOID** (European Business Wallet Organisation Identity Document) - for legal entities

The credential presentation **MUST** comply with WBCS-002 (OpenID4VP, SD-JWT-VC). The QTSP **MUST** act as Verifier per WBCS-002 Section 7.2.

### 12.4 Access Token

On successful verification, the QTSP **MUST** issue a Bearer access token. The token:

- **MUST** be a signed JWT
- **MUST** contain the `sub` claim set to the Subscriber's `did:euid`
- **MUST** contain `iat` and `exp` claims
- **MUST** have an expiry no longer than 1 hour
- **MUST NOT** be issued without a completed OpenID4VP verification.

Token binding to the EBW's key pair (e.g. via DPoP, RFC 9449(include normative reference)) is **OPTIONAL** and **RECOMMENDED** for deployments requiring higher assurance.

For token renewal after an already-registered Subscriber's token expires, see Section 12.5.

### 12.5 Token Renewal for Registered Subscribers

When a Subscriber's access token expires, the EBW **MUST** obtain a new token by repeating the OpenID4VP identity verification at the token renewal endpoint. The flow is identical to onboarding (Section 12.1) except that the Subscriber's `did:euid` is **not** re-registered - the QTSP issues a new access token for the existing registration.

```mermaid
sequenceDiagram
    participant EBW as EBW
    participant QTSP as QTSP

    note over EBW: Access token has expired

    EBW->>QTSP: POST /token/start<br>{ subscriber_did: "did:euid:..." }
    QTSP->>QTSP: Look up registered subscriber
    QTSP-->>EBW: OpenID4VP Authorization Request<br>(per WBCS-002, nonce, response_uri)

    EBW->>QTSP: OpenID4VP VP Token Response<br>(PID or EBWOID credential)
    QTSP->>QTSP: Verify VP Token<br>Match EUID to registered subscriber

    QTSP-->>EBW: { access_token, token_expiry }
```

The QTSP **MUST**:
- Verify that the EUID in the presented credential matches the `did:euid` of the registered Subscriber
- Issue a new access token with the same constraints as Section 12.4
- Not modify the Subscriber's DID Document or re-register the `did:euid`

### 12.6 Key Rotation for Registered Subscribers

A Subscriber **MAY** rotate its keys at any time - for example, when a key is compromised, when a key expires, or when migrating to new cryptographic algorithms. Key rotation updates the Subscriber's DID Document in the discovery infrastructure with the new public key(s). It does **not** re-register the `did:euid` and does **not** issue a new access token.

The flow is identical to onboarding (Section 12.1) with two differences: the Subscriber provides new key material instead of requesting a fresh registration, and the QTSP updates the existing DID Document entry rather than creating a new one.

```mermaid
sequenceDiagram
    participant EBW as EBW
    participant QTSP as QTSP

    note over EBW: EBW generates new key pair(s)

    EBW->>QTSP: POST /keys/rotate/start<br>{ subscriber_did: "did:euid:...",<br>  new_keys: [ { id, type, publicKeyJwk, verificationRelationships } ] }
    QTSP->>QTSP: Look up registered subscriber
    QTSP-->>EBW: OpenID4VP Authorization Request<br>(per WBCS-002, nonce, response_uri)

    EBW->>QTSP: OpenID4VP VP Token Response<br>(PID or EBWOID credential)
    QTSP->>QTSP: Verify VP Token<br>Match EUID to registered subscriber

    QTSP->>QTSP: Update DID Document in discovery infrastructure<br>Replace old key(s) with new_keys

    QTSP-->>EBW: { subscriber_did, rotated_at }
```

**Key rotation request fields:**

| Field | Type | Requirement | Notes |
|---|---|---|---|
| `subscriber_did` | string | MUST | The `did:euid` of the Subscriber requesting rotation |
| `new_keys` | array | MUST | One or more new verification method objects to replace the existing keys |
| `new_keys[].id` | string | MUST | Key identifier, e.g. `did:euid:<euid>#key-2` |
| `new_keys[].type` | string | MUST | Key type, e.g. `JsonWebKey2020` |
| `new_keys[].publicKeyJwk` | object | MUST | The new public key in JWK format |
| `new_keys[].verificationRelationships` | array | MUST | Verification relationships this key should be listed under (e.g. `["keyAgreement"]`) |

The QTSP **MUST**:
- Require the EBW to complete the OpenID4VP identity verification flow before applying any key update.
- Verify that the EUID in the presented credential matches the `did:euid` in the rotation request.
- Replace the Subscriber's key(s) in the DID Document atomically - old keys are removed and new keys are added in a single update.
- Propagate the updated DID Document to the discovery infrastructure within 24 hours of confirmation.
- Not re-register the `did:euid` and not issue a new access token as part of key rotation.
- Return an error if the `subscriber_did` is not found in its registry.

The QTSP **MUST NOT**:
- Accept a key rotation request without a completed OpenID4VP verification.
- Accept new keys of a type or size that does not meet the requirements in Section 7.2.

The EBW **MUST**:
- Continue using the existing access token (if still valid) after key rotation; a new token is not issued.
- Ensure the new `keyAgreement` key is available before the rotation completes, as incoming messages encrypted to the old key will no longer be decryptable after the DID Document is updated.

> **Note on transition:** There is an inherent window between when the new DID Document is published and when senders have refreshed their cached resolution of the Subscriber's DID. During this window, a sender may encrypt to the old key. EBWs **SHOULD** retain old private keys for a short grace period (e.g. 24 hours) after rotation to decrypt any in-flight messages that were encrypted before the DID Document update propagated.

---

## 13. DIDComm Transport

### 13.1 Transport Options

This specification defines two transport bindings for DIDComm messages between the EBW and the QTSP.

| Transport | QTSP | EBW | Notes |
|---|---|---|---|
| **HTTPS POST + inbox polling** | MUST | MUST | Baseline transport; works for any EBW deployment model |
| **WebSocket** | MUST | MAY | Enables push delivery from QTSP to EBW; required for real-time automated flows |

A conforming QTSP **MUST** support both transports so that any EBW can connect regardless of its deployment model. A conforming EBW **MUST** support HTTPS POST and **MAY** additionally support WebSocket to receive push notifications without polling.

### 13.2 WebSocket Channel Establishment

```mermaid
sequenceDiagram
    participant EBW as EBW
    participant QTSP as QTSP

    EBW->>QTSP: HTTP UPGRADE to WebSocket<br>wss://qtsp.example/didcomm<br>Authorization: Bearer <access_token>
    QTSP->>QTSP: Validate Bearer token<br>(verify EUID binding + key)
    QTSP-->>EBW: 101 Switching Protocols

    note over EBW,QTSP: WebSocket connection established.<br>DIDComm messages flow bidirectionally.

    EBW->>QTSP: DIDComm Message<br>(type: ebw/ping/1.0, return_route: all)
    QTSP-->>EBW: DIDComm Message<br>(type: ebw/ping-response/1.0)

    note over EBW,QTSP: Channel confirmed live.
```

The EBW **MUST** set the `return_route: all` header in the initial DIDComm message to instruct the QTSP to use the established WebSocket connection for inbound messages. The `return_route` header is defined in [DIDCOMM] Section 4 (Transports).

### 13.3 HTTPS POST (Polling Mode)

When using HTTPS POST, the EBW sends outbound messages by posting to the QTSP's DIDComm endpoint. Inbound messages are retrieved by polling.

```mermaid
sequenceDiagram
    participant EBW as EBW
    participant QTSP as QTSP

    note over EBW: Outbound message
    EBW->>QTSP: POST https://qtsp.example/didcomm<br>Authorization: Bearer <access_token><br>Content-Type: application/didcomm+json (or didcomm-encrypted+json)<br>[DIDComm Message]
    QTSP-->>EBW: 202 Accepted

    note over EBW: Poll for inbound messages
    EBW->>QTSP: GET https://qtsp.example/didcomm/inbox<br>Authorization: Bearer <access_token>
    QTSP-->>EBW: 200 OK<br>[array of DIDComm Messages]

    EBW->>QTSP: POST https://qtsp.example/didcomm<br>DIDComm ebw/ack/1.0<br>{ thid: <message_id> }
    QTSP-->>EBW: 202 Accepted
```

The QTSP **SHOULD** retain undelivered inbound messages for a reasonable period; the minimum retention period **MAY** be defined by the QTSP's service terms. The EBW **MUST** acknowledge each received message by sending a DIDComm `ebw/ack/1.0` message (Section 16).

### 13.4 DIDComm Message Envelope

#### EBW - QTSP messages

Messages on the EBW–QTSP leg **MUST** be valid [DIDCOMM] messages and **MUST** include the fields `type`, `id`, `thid`, `from`, `to`, `created_time`, and `body`. They **MAY** be sent as plain DIDComm messages or as JWE-encrypted DIDComm messages. Transport confidentiality is provided by TLS in both cases.

JWE encryption is **OPTIONAL**. Implementations that choose to encrypt **MUST** use:

- **Key agreement:** ECDH-ES+A256KW with X25519, P-256, P-384, or P-521 keys
- **Content encryption:** A256CBC-HS512 or A256GCM

When JWE is not used, the `Content-Type` is `application/didcomm+json`. When JWE is used, the `Content-Type` is `application/didcomm-encrypted+json`.

Signing via DIDComm Signed Messages (JWS) is **OPTIONAL** for non-repudiation when required by use cases.

#### WACI inner payloads (EBW-to-EBW)

EBW-to-EBW messages are sent as the attachment of a DIDComm routing forward message [DIDCOMM]. The QTSP acts as a mediator: it routes by `body.next` and treats the attachment as opaque bytes. The forward message **MUST** comply with the following structure:

```json
{
  "type": "https://didcomm.org/routing/2.0/forward",
  "id": "<uuid>",
  "thid": "<thread_id>",
  "from": "did:euid:<sender_euid>",
  "to": ["<qtsp_did>"],
  "created_time": 1234567890,
  "body": {
    "next": "did:euid:<recipient_euid>"
  },
  "attachments": [
    {
      "id": "<uuid>",
      "media_type": "application/didcomm-encrypted+json",
      "data": {
        "json": {}
      }
    }
  ]
}
```

The attachment **MUST** be a DIDComm Encrypted Message (JWE) encrypted to the **final recipient EBW's `keyAgreement` key**. The QTSP delivers the attachment directly to the Recipient EBW without any wrapper, per the DIDComm routing spec. The algorithms in the EBW–QTSP section above apply.

> **Note on post-quantum readiness:** The key agreement and encryption algorithms listed are not post-quantum safe. Implementations **MUST** use modular cryptographic interfaces to permit future algorithm migration (e.g. to ML-KEM) when standardized for DIDComm. This is consistent with the ADR requirement for a PQC pathway before 2035.

---

## 14. Message Submission Flow

This flow covers the Sender EBW submitting a message to the QERDS (Interfaces 14 and 11).

The Sender EBW's identity is established by the Bearer access token, which the QTSP issued only after a completed OpenID4VP verification. No additional identity check is required at submission.

```mermaid
sequenceDiagram
    actor User as Sender (User/Agent)
    participant EBW as Sender EBW
    participant S_QTSP as Sender QTSP
    participant R_QTSP as Recipient QTSP
    participant R_EBW as Recipient EBW

    User->>EBW: Request to send message<br>(recipient EUID, payload)

    EBW->>S_QTSP: DIDComm: routing/2.0/forward<br>{ next: recipient_did, attachment: <inner JWE> }

    note over S_QTSP: Validate Bearer token<br>Create SubmissionAcceptanceRejection evidence<br>(QESeal + QTS - Interfaces 5-9 internal)
    S_QTSP-->>EBW: DIDComm: ebw/erds-evidence/1.0<br>{ evidence_type: SubmissionAcceptanceRejection,<br>  attachment: EN 319 522-3 XML }

    note over S_QTSP,R_QTSP: QTSP resolves recipient QTSP endpoint<br>via discovery infrastructure (out of scope)<br>then relays (Interface 16 - AS4, out of scope)
    S_QTSP->>R_QTSP: AS4 Message relay

    R_QTSP->>R_EBW: DIDComm: ebw/delivery-notification/1.0<br>{ thread_id, sender_euid }

    note over R_QTSP,R_EBW: Recipient delivery flow (see Section 15)

    R_QTSP-->>S_QTSP: Consignment confirmed (AS4)
    S_QTSP-->>EBW: DIDComm: ebw/erds-evidence/1.0<br>{ evidence_type: DeliveryToRecipient,<br>  attachment: EN 319 522-3 XML }
```

**Key ordering rule (submission):** The QTSP **MUST** deliver the `SubmissionAcceptanceRejection` evidence to the Sender EBW **before** relaying the message to the Recipient QTSP. The evidence timestamp records the moment of submission acceptance.

---

## 15. Message Reception Flow

This flow covers the Recipient EBW receiving a message from the QERDS (Interfaces 10 and 11).

The Recipient EBW's identity is established by its Bearer access token. No additional identity check is required at delivery.

```mermaid
sequenceDiagram
    participant S_QTSP as Sender QTSP
    participant R_QTSP as Recipient QTSP
    participant R_EBW as Recipient EBW
    actor User as Recipient (User/Agent)

    S_QTSP->>R_QTSP: AS4 Message relay (Interface 16)

    R_QTSP->>R_EBW: DIDComm: ebw/delivery-notification/1.0<br>{ thread_id, sender_euid, message_size, content_type }

    R_EBW->>User: Display incoming message notification
    User->>R_EBW: Accept / auto-accept

    R_QTSP->>R_EBW: DIDComm: <inner JWE><br>(forwarded attachment, opaque)

    R_EBW-->>R_QTSP: DIDComm: ebw/ack/1.0<br>{ thread_id }

    note over R_QTSP: Create DeliveryToRecipient evidence<br>(triggered by ack - QESeal + QTS internal)

    R_QTSP->>R_EBW: DIDComm: ebw/erds-evidence/1.0<br>{ evidence_type: DeliveryToRecipient,<br>  attachment: EN 319 522-3 XML }

    R_QTSP-->>S_QTSP: Delivery confirmed (AS4)
```

**Key ordering rule (reception):** The QTSP **MUST** generate and deliver `DeliveryToRecipient` evidence only after receiving `ebw/ack/1.0` from the Recipient EBW. The evidence timestamp records confirmed receipt - the moment the EBW acknowledged the message - rather than the moment the QTSP attempted delivery.

---

## 16. DIDComm Message Types

All message types are defined under the `ebw` protocol namespace. Message bodies are JSON objects inside a DIDComm Encrypted Message envelope.

### 16.1 ebw/ping/1.0

**Direction:** EBW -> QTSP  
**Purpose:** Channel liveness check during WebSocket establishment.

```json
{
  "type": "https://webuild.example/didcomm/ebw/ping/1.0",
  "id": "<uuid>",
  "from": "did:euid:<sender_euid>",
  "to": ["<qtsp_did>"],
  "created_time": 1234567890,
  "body": {}
}
```

### 16.2 Message Submission (DIDComm Routing Forward)

**Direction:** EBW -> QTSP  
**Purpose:** Submit a message for QERDS delivery (Interface 14). Uses the standard DIDComm routing forward protocol [DIDCOMM] - the QTSP acts as a mediator.

```json
{
  "type": "https://didcomm.org/routing/2.0/forward",
  "id": "<uuid>",
  "thid": "<thread_id>",
  "from": "did:euid:<sender_euid>",
  "to": ["<qtsp_did>"],
  "created_time": 1234567890,
  "body": {
    "next": "did:euid:<recipient_euid>"
  },
  "attachments": [
    {
      "id": "<uuid>",
      "media_type": "application/didcomm-encrypted+json",
      "data": {
        "json": { }
      }
    }
  ]
}
```

The `body.next` field **MUST** be the recipient EBW's `did:euid`. The QTSP resolves this DID against the WE BUILD discovery infrastructure to determine the recipient QTSP and route the message via AS4. The attachment **MUST** be a DIDComm JWE encrypted to the recipient EBW's `keyAgreement` key - the QTSP treats it as opaque bytes.

### 16.3 ebw/erds-evidence/1.0

**Direction:** QTSP -> EBW  
**Purpose:** Deliver QERDS evidence to the EBW (Interface 11).

```json
{
  "type": "https://webuild.example/didcomm/ebw/erds-evidence/1.0",
  "id": "<uuid>",
  "thid": "<thread_id>",
  "from": "<qtsp_did>",
  "to": ["did:euid:<subscriber_euid>"],
  "created_time": 1234567890,
  "body": {
    "evidence_type": "SubmissionAcceptanceRejection | RelayAcceptanceRejection | DeliveryNonDeliveryToRecipient"
  },
  "attachments": [
    {
      "id": "<uuid>",
      "description": "ETSI EN 319 522-3 evidence XML, sealed with QTSP QESeal",
      "media_type": "application/xml",
      "data": {
        "base64": "<base64url-encoded ETSI EN 319 522-3 XML>"
      }
    }
  ]
}
```

The attachment carries the signed ETSI EN 319 522-3 XML. The QTSP QESeal is embedded within the XML structure itself per EN 319 522-3, so no separate `qtsp_seal` field is needed.

### 16.4 ebw/delivery-notification/1.0

**Direction:** QTSP -> EBW  
**Purpose:** Notify the Recipient EBW of a pending inbound message (Interface 10).

```json
{
  "type": "https://webuild.example/didcomm/ebw/delivery-notification/1.0",
  "id": "<uuid>",
  "thid": "<thread_id>",
  "from": "<qtsp_did>",
  "to": ["did:euid:<recipient_euid>"],
  "created_time": 1234567890,
  "body": {
    "sender_euid": "<sender_euid>",
    "content_type": "<IANA media type>",
    "message_size_bytes": 12345
  }
}
```

### 16.5 ebw/ack/1.0

**Direction:** EBW -> QTSP  
**Purpose:** Acknowledge receipt of a delivered message or evidence record.

```json
{
  "type": "https://webuild.example/didcomm/ebw/ack/1.0",
  "id": "<uuid>",
  "thid": "<thread_id>",
  "from": "did:euid:<subscriber_euid>",
  "to": ["<qtsp_did>"],
  "created_time": 1234567890,
  "body": {
    "ack_id": "<id of the message being acknowledged>"
  }
}
```

---

## 17. Normative Requirements - DIDComm over QTSP

### 17.1 QTSP Requirements

The QTSP **MUST**:

1. Serve a valid QTSP metadata document at `/.well-known/qtsp-configuration` signed with a key from its qualified certificate.
2. Support the OpenID4VP onboarding flow per WBCS-002 as Verifier, accepting PID and EBWOID credentials.
3. Issue a signed JWT Bearer access token on successful onboarding with `sub` set to the Subscriber's `did:euid` and expiry ≤1 hour.
4. Register the Subscriber's `did:euid`, public key, and DIDComm service endpoint in the WE BUILD discovery infrastructure upon successful onboarding.
5. Support the token renewal flow (Section 12.5), accepting OpenID4VP VP Token presentations at the `token_endpoint` to issue new access tokens for registered Subscribers without re-registering the `did:euid`.
6. Support the key rotation flow (Section 12.6), accepting OpenID4VP VP Token presentations at the `key_rotation_endpoint` to update the Subscriber's DID Document with new key material, without re-registering the `did:euid` or issuing a new access token.
7. Support both WebSocket (`wss://`) and HTTPS POST DIDComm transports.
8. Validate the Bearer access token on every incoming WebSocket upgrade and HTTPS POST request.
9. Deliver `SubmissionAcceptanceRejection` evidence to the Sender EBW before relaying the message to the Recipient QTSP.
10. Deliver `DeliveryToRecipient` evidence to the Recipient EBW after receiving `ebw/ack/1.0` confirming the Recipient EBW received the message content.
11. Retain undelivered inbound messages for a minimum of 30 days.
12. Seal all ERDS evidence with a Qualified Electronic Seal (QESeal) and Qualified Timestamp (QTS) per ETSI EN 319 522-3.

The QTSP **SHOULD**:

1. Require the EBW to set `return_route: all` on WebSocket connections to enable push delivery ([DIDCOMM] Section 4).
2. Implement reconnection deduplication using DIDComm message `id` fields.

The QTSP **MUST NOT**:

1. Generate or deliver `DeliveryToRecipient` evidence before receiving `ebw/ack/1.0` from the Recipient EBW.

### 17.2 EBW Requirements

The EBW **MUST**:

1. Retrieve and verify the QTSP metadata document before initiating onboarding.
2. Generate a dedicated key pair for the `did:euid` DID Document during onboarding. The private key **MUST** be stored in a hardware-backed secure element or WSCA/QSCD where available.
3. Complete the OpenID4VP presentation flow during onboarding, presenting a valid PID or EBWOID credential.
4. Renew the access token when it expires or is about to expire by repeating the OpenID4VP identity verification via the token renewal endpoint (Section 12.5).
5. JWE-encrypt all WACI inner payloads to the final recipient EBW's key agreement key and place them as the attachment of the DIDComm routing forward message.
6. Store all received ERDS evidence records durably, associating each with its thread identifier.
7. Send `ebw/ack/1.0` upon successful receipt of each delivered message.
8. Support HTTPS POST transport. WebSocket transport is **OPTIONAL** for EBWs and **RECOMMENDED** for server-side or always-on deployments that benefit from push delivery.

The EBW **SHOULD**:

1. Use WebSocket transport when operating as a server-side or always-on deployment.
2. Use HTTPS POST with polling when operating in a mobile or intermittent-connectivity context.

---

# Part 3: WACI-DIDComm Credential Interactions

## 18. Overview

This part specifies how credential issuance and credential presentation are performed between EBWs using the WACI-DIDComm protocols [WACI-DIDCOMM] over the QERDS channel defined in Part 2.

WACI-DIDComm defines two protocol families used here:

- **Issue Credential 3.0** (`https://didcomm.org/issue-credential/3.0/`) - for issuing Verifiable Credentials from an Issuer EBW to a Holder EBW
- **Present Proof 3.0** (`https://didcomm.org/present-proof/3.0/`) - for requesting and submitting Verifiable Presentations from a Holder EBW to a Verifier EBW

### 18.1 Transport and Encryption Model

The two DIDComm layers operate at different scopes and are independent of each other:

| Layer | Scope | Notes |
|---|---|---|
| Outer (`routing/2.0/forward`) | EBW ↔ own QTSP | QTSP acts as DIDComm mediator - routes by `body.next`, handles QERDS transport and evidence |
| Inner (WACI message in `attachments`) | EBW ↔ remote EBW | JWE encrypted to recipient EBW's `keyAgreement` key - end-to-end, opaque to both QTSPs |

The QTSP treats the attachment as an opaque byte sequence. It does not parse, decrypt, or inspect it. The inner message is a standard WACI-DIDComm Encrypted Message [DIDCOMM] encrypted to the recipient EBW's `keyAgreement` key (resolved via Section 9). This is the standard DIDComm mediator pattern: the routing forward message carries an encrypted DIDComm message as an opaque attachment.

### 18.2 Thread Continuity and Evidence Correlation

Each WACI protocol run (issuance or presentation) uses a single DIDComm thread identifier (`thid`) shared across all messages in that run. The QERDS evidence records (Sections 14 and 15) reference this same `thid`, allowing the EBW to associate every ERDS evidence record with the specific credential operation it covers.

---

## 19. Credential Issuance over QERDS

Credential issuance follows the WACI-DIDComm Issue Credential 3.0 protocol. The Issuer EBW initiates with an offer; the Holder EBW responds with a key proof; the Issuer delivers the bound credential.

### 19.1 Credential Issuance Flow

```mermaid
sequenceDiagram
    participant I_EBW as Issuer EBW
    participant I_QTSP as Issuer QTSP
    participant R_QTSP as Recipient QTSP
    participant H_EBW as Holder EBW

    note over I_EBW,H_EBW: Thread ID T1 runs through all messages

    rect rgb(235, 245, 255)
        note over I_EBW,H_EBW: Step 1 - offer-credential
        I_EBW->>I_EBW: Resolve did:euid of Holder<br>(Section 9)
        I_EBW->>I_EBW: Create inner DIDComm message:<br>issue-credential/3.0/offer-credential<br>encrypted to Holder EBW key
        I_EBW->>I_QTSP: routing/2.0/forward<br>{ next: Holder did, attachment: <encrypted offer> }
        I_QTSP-->>I_EBW: ebw/erds-evidence/1.0<br>{ SubmissionAcceptanceRejection, thid: T1 }
        I_QTSP->>R_QTSP: AS4 relay
        R_QTSP->>H_EBW: ebw/erds-evidence/1.0<br>{ RelayAcceptanceRejection, thid: T1 }
        R_QTSP->>H_EBW: <inner JWE><br>(forwarded attachment)
        H_EBW->>H_EBW: Decrypt inner message<br>Extract credential template + nonce
        H_EBW-->>R_QTSP: ebw/ack/1.0
        R_QTSP-->>I_QTSP: Delivery confirmed (AS4)
        I_QTSP-->>I_EBW: ebw/erds-evidence/1.0<br>{ DeliveryToRecipient, thid: T1 }
    end

    rect rgb(235, 255, 235)
        note over I_EBW,H_EBW: Step 2 - request-credential (key proof)
        H_EBW->>H_EBW: Generate key pair (WSCA/QSCD)<br>Sign PoP JWT with new private key<br>(see Section 19.1 for full structure)
        H_EBW->>H_EBW: Create inner DIDComm message:<br>issue-credential/3.0/request-credential<br>encrypted to Issuer EBW key
        H_EBW->>R_QTSP: routing/2.0/forward<br>{ next: Issuer did, attachment: <encrypted request> }
        R_QTSP-->>H_EBW: ebw/erds-evidence/1.0<br>{ SubmissionAcceptanceRejection, thid: T1 }
        R_QTSP->>I_QTSP: AS4 relay
        I_QTSP->>I_EBW: ebw/erds-evidence/1.0<br>{ RelayAcceptanceRejection, thid: T1 }
        I_QTSP->>I_EBW: <inner JWE><br>(forwarded attachment)
        I_EBW->>I_EBW: Decrypt inner message<br>Verify PoP JWT:<br>- nonce matches offer<br>- credential_hash matches template<br>- cnf.jwk valid
        I_EBW-->>I_QTSP: ebw/ack/1.0
        I_QTSP-->>R_QTSP: Delivery confirmed (AS4)
        R_QTSP-->>H_EBW: ebw/erds-evidence/1.0<br>{ DeliveryToRecipient, thid: T1 }
    end

    rect rgb(255, 245, 235)
        note over I_EBW,H_EBW: Step 3 - issue-credential
        I_EBW->>I_EBW: Issue SD-JWT-VC:<br>bind cnf.jwk = Holder public key
        I_EBW->>I_EBW: Create inner DIDComm message:<br>issue-credential/3.0/issue-credential<br>encrypted to Holder EBW key
        I_EBW->>I_QTSP: routing/2.0/forward<br>{ next: Holder did, attachment: <encrypted credential> }
        I_QTSP-->>I_EBW: ebw/erds-evidence/1.0<br>{ SubmissionAcceptanceRejection, thid: T1 }
        I_QTSP->>R_QTSP: AS4 relay
        R_QTSP->>H_EBW: <inner JWE><br>(forwarded attachment)
        H_EBW->>H_EBW: Decrypt inner message<br>Verify SD-JWT-VC issuer signature<br>Verify cnf.jwk matches generated key<br>Store credential
        H_EBW-->>R_QTSP: ebw/ack/1.0
        note over R_QTSP: Create DeliveryToRecipient evidence<br>(triggered by ack - QESeal + QTS internal)
        R_QTSP->>H_EBW: ebw/erds-evidence/1.0<br>{ DeliveryToRecipient, thid: T1 }
        R_QTSP-->>I_QTSP: Delivery confirmed (AS4)
        I_QTSP-->>I_EBW: ebw/erds-evidence/1.0<br>{ DeliveryToRecipient, thid: T1 }
    end
```

### 19.2 QERDS Audit Trail for Issuance

At the end of a successful issuance exchange, each EBW holds the following evidence records:

| Evidence type | Direction | Held by |
|---|---|---|
| `SubmissionAcceptanceRejection` | Issuer -> Holder (offer) | Issuer EBW |
| `RelayAcceptanceRejection` | Issuer -> Holder (offer) | Holder EBW |
| `DeliveryToRecipient` | Issuer -> Holder (offer) | Issuer EBW |
| `SubmissionAcceptanceRejection` | Holder -> Issuer (request) | Holder EBW |
| `RelayAcceptanceRejection` | Holder -> Issuer (request) | Issuer EBW |
| `DeliveryToRecipient` | Holder -> Issuer (request) | Holder EBW |
| `SubmissionAcceptanceRejection` | Issuer -> Holder (credential) | Issuer EBW |
| `DeliveryToRecipient` | Issuer -> Holder (credential) | Issuer EBW + Holder EBW |

All six transmission events in the credential lifecycle are recorded with qualified timestamps, giving a verifiable audit trail that is not available in OID4VCI-based issuance.

---

## 20. Credential Presentation over QERDS

Credential presentation follows the WACI-DIDComm Present Proof 3.0 protocol. The Verifier EBW initiates with a presentation request; the Holder EBW responds with a Verifiable Presentation containing the requested SD-JWT-VC disclosures.

This flow is suitable for **automated and agent-based verification** where no real-time user redirect is required. For interactive flows that require immediate user consent (e.g. login or on-premises access), OpenID4VP (WBCS-002) remains appropriate.

### 20.1 Credential Presentation Flow

```mermaid
sequenceDiagram
    participant V_EBW as Verifier EBW
    participant V_QTSP as Verifier QTSP
    participant H_QTSP as Holder QTSP
    participant H_EBW as Holder EBW

    note over V_EBW,H_EBW: Thread ID T2 runs through all messages

    rect rgb(235, 245, 255)
        note over V_EBW,H_EBW: Step 1 - request-presentation
        V_EBW->>V_EBW: Resolve did:euid of Holder (Section 9)
        V_EBW->>V_EBW: Create inner DIDComm message:<br>present-proof/3.0/request-presentation<br>{ presentation_definition, nonce }<br>encrypted to Holder EBW key
        V_EBW->>V_QTSP: routing/2.0/forward<br>{ next: Holder did, attachment: <encrypted request> }
        V_QTSP-->>V_EBW: ebw/erds-evidence/1.0<br>{ SubmissionAcceptanceRejection, thid: T2 }
        V_QTSP->>H_QTSP: AS4 relay
        H_QTSP->>H_EBW: ebw/erds-evidence/1.0<br>{ RelayAcceptanceRejection, thid: T2 }
        H_QTSP->>H_EBW: <inner JWE><br>(forwarded attachment)
        H_EBW->>H_EBW: Decrypt inner message<br>Parse presentation_definition<br>Select matching credential(s)
        H_EBW-->>H_QTSP: ebw/ack/1.0
        H_QTSP-->>V_QTSP: Delivery confirmed (AS4)
        V_QTSP-->>V_EBW: ebw/erds-evidence/1.0<br>{ DeliveryToRecipient, thid: T2 }
    end

    rect rgb(255, 245, 235)
        note over V_EBW,H_EBW: Step 2 - presentation
        H_EBW->>H_EBW: Apply selective disclosure:<br>choose claims to reveal<br>Create VP: SD-JWT-VC~disclosure~kb-jwt<br>kb-jwt binds nonce + verifier DID
        H_EBW->>H_EBW: Create inner DIDComm message:<br>present-proof/3.0/presentation<br>{ vp_token, presentation_submission }<br>encrypted to Verifier EBW key
        H_EBW->>H_QTSP: routing/2.0/forward<br>{ next: Verifier did, attachment: <encrypted presentation> }
        H_QTSP-->>H_EBW: ebw/erds-evidence/1.0<br>{ SubmissionAcceptanceRejection, thid: T2 }
        H_QTSP->>V_QTSP: AS4 relay
        V_QTSP->>V_EBW: <inner JWE><br>(forwarded attachment)
        V_EBW->>V_EBW: Decrypt inner message<br>Verify SD-JWT-VC issuer signature<br>Verify kb-jwt (nonce + aud = verifier DID)<br>Verify presentation_submission<br>Extract disclosed claims
        V_EBW-->>V_QTSP: ebw/ack/1.0
        note over V_QTSP: Create DeliveryToRecipient evidence<br>(triggered by ack - QESeal + QTS internal)
        V_QTSP->>V_EBW: ebw/erds-evidence/1.0<br>{ DeliveryToRecipient, thid: T2 }
        V_QTSP-->>H_QTSP: Delivery confirmed (AS4)
        H_QTSP-->>H_EBW: ebw/erds-evidence/1.0<br>{ DeliveryToRecipient, thid: T2 }
    end
```

### 20.2 QERDS Audit Trail for Presentation

| Evidence type | Direction | Held by |
|---|---|---|
| `SubmissionAcceptanceRejection` | Verifier -> Holder (request) | Verifier EBW |
| `RelayAcceptanceRejection` | Verifier -> Holder (request) | Holder EBW |
| `DeliveryToRecipient` | Verifier -> Holder (request) | Verifier EBW |
| `SubmissionAcceptanceRejection` | Holder -> Verifier (presentation) | Holder EBW |
| `DeliveryToRecipient` | Holder -> Verifier (presentation) | Verifier EBW + Holder EBW |

The `DeliveryToRecipient` evidence for the presentation records the moment the Verifier received the VP, establishing a qualified timestamped record of the presentation event.

---

# 21. Interface Definitions

### 21.1 QTSP Metadata Endpoint

*Direction:* EBW -> QTSP  
*Method:* HTTPS GET  
*Path:* `/.well-known/qtsp-configuration`

**Response fields:**

| Field | Type | Requirement | Description |
|---|---|---|---|
| `qtsp_id` | string | MUST | QTSP's EUID or TSL identifier |
| `qtsp_did` | string | MUST | The QTSP's DID |
| `didcomm_endpoint` | string | MUST | WSS and/or HTTPS POST URI for DIDComm messages |
| `onboarding_endpoint` | string | MUST | URI to initiate the OpenID4VP onboarding flow |
| `token_endpoint` | string | MUST | URI to renew an access token for an already-registered Subscriber (Section 12.5) |
| `supported_credentials` | array of string | MUST | Credential types accepted for identity proofing |

**Example response:**
```json
{
  "qtsp_id": "DEK1101R.QTSP001",
  "qtsp_did": "did:web:qtsp.example",
  "didcomm_endpoint": "wss://qtsp.example/didcomm",
  "onboarding_endpoint": "https://qtsp.example/onboarding",
  "token_endpoint": "https://qtsp.example/token",
  "supported_credentials": ["PID", "EBWOID"]
}
```

The response **MUST** be signed with a key from the QTSP's qualified certificate or TSL entry.

---

### 21.2 Onboarding Endpoint

*Direction:* EBW -> QTSP IPS  
*Method:* HTTPS POST  
*Path:* `/onboarding/start`

**Request fields:**

| Field | Type | Requirement | Description |
|---|---|---|---|
| `ebw_did_key` | JWK object | MUST | The EBW's public key to be registered in the `did:euid` DID Document |

**Example request:**
```json
{
  "ebw_did_key": {
    "kty": "EC",
    "crv": "P-256",
    "x": "<base64url>",
    "y": "<base64url>"
  }
}
```

The QTSP responds with an OpenID4VP Authorization Request per WBCS-002. After successful presentation, the QTSP issues:

**Response fields:**

| Field | Type | Requirement | Description |
|---|---|---|---|
| `subscriber_did` | string | MUST | The Subscriber's assigned `did:euid` |
| `access_token` | string | MUST | Signed JWT Bearer token; expiry ≤ 1 hour |
| `token_expiry` | integer | MUST | Unix timestamp of token expiry |

**Example response:**
```json
{
  "subscriber_did": "did:euid:DEK1101R.HRB116737",
  "access_token": "eyJhbGciOiJFUzI1NiJ9.<payload>.<signature>",
  "token_expiry": 1234571490
}
```

---

### 21.3 Token Renewal Endpoint

*Direction:* EBW -> QTSP  
*Method:* HTTPS POST  
*Path:* Value of `token_endpoint` from QTSP metadata

This endpoint is used by already-registered Subscribers to obtain a new access token by repeating OpenID4VP identity verification (Section 12.5). No DID registration occurs.

**Step 1 - Start renewal:**

*Path:* `{token_endpoint}/start`

**Request fields:**

| Field | Type | Requirement | Description |
|---|---|---|---|
| `subscriber_did` | string | MUST | The registered Subscriber's `did:euid` |

**Example request:**
```json
{
  "subscriber_did": "did:euid:DEK1101R.HRB116737"
}
```

The QTSP responds with an OpenID4VP Authorization Request per WBCS-002. The EBW completes the VP Token presentation as in onboarding.

**Step 2 - Response (after VP verification):**

**Response fields:**

| Field | Type | Requirement | Description |
|---|---|---|---|
| `access_token` | string | MUST | New signed JWT Bearer token; expiry ≤ 1 hour |
| `token_expiry` | integer | MUST | Unix timestamp of access token expiry |

**Example response:**
```json
{
  "access_token": "eyJhbGciOiJFUzI1NiJ9.<new_payload>.<signature>",
  "token_expiry": 1234575090
}
```

**Responses:**

| Status | Meaning |
|---|---|
| `200 OK` | New access token issued |
| `400 Bad Request` | Missing `subscriber_did` or unknown subscriber |
| `401 Unauthorized` | VP verification failed or EUID mismatch |

---

### 21.4 DIDComm WebSocket Endpoint

*Direction:* EBW -> QTSP (upgrade), then bidirectional  
*Method:* HTTP UPGRADE (WebSocket)  
*Path:* Value of `didcomm_endpoint` from QTSP metadata  
*Authentication:* `Authorization: Bearer <access_token>` on UPGRADE request

**Request headers:**

| Header | Requirement | Description |
|---|---|---|
| `Authorization` | MUST | `Bearer <access_token>` |
| `Upgrade` | MUST | `websocket` |

**Responses:**

| Status | Meaning |
|---|---|
| `101 Switching Protocols` | Connection established; DIDComm messages flow bidirectionally as `application/didcomm-encrypted+json` |
| `401 Unauthorized` | Missing or invalid access token |
| `403 Forbidden` | Token valid but subscriber not registered |

**Example upgrade request:**
```http
GET /didcomm HTTP/1.1
Host: qtsp.example
Upgrade: websocket
Connection: Upgrade
Authorization: Bearer eyJhbGciOiJFUzI1NiJ9.<payload>.<signature>
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

---

### 21.5 DIDComm HTTPS POST Endpoint

*Direction:* EBW -> QTSP (outbound messages)  
*Method:* HTTPS POST  
*Path:* Value of `didcomm_endpoint` from QTSP metadata  

**Request headers:**

| Header | Requirement | Description |
|---|---|---|
| `Authorization` | MUST | `Bearer <access_token>` |
| `Content-Type` | MUST | `application/didcomm-encrypted+json` or `application/didcomm+json` |

**Request body:** DIDComm message (plain or JWE-encrypted per Section 13.4)

**Responses:**

| Status | Meaning |
|---|---|
| `202 Accepted` | Message accepted for processing |
| `400 Bad Request` | Malformed DIDComm message |
| `401 Unauthorized` | Missing or invalid access token |

**Example request:**
```http
POST /didcomm HTTP/1.1
Host: qtsp.example
Authorization: Bearer eyJhbGciOiJFUzI1NiJ9.<payload>.<signature>
Content-Type: application/didcomm-encrypted+json

{"ciphertext":"<base64url>","protected":"<base64url>","recipients":[...],"tag":"<base64url>","iv":"<base64url>"}
```

---

### 21.6 DIDComm Inbox Polling Endpoint

*Direction:* EBW -> QTSP  
*Method:* HTTPS GET  
*Path:* `{didcomm_endpoint}/inbox`

**Request headers:**

| Header | Requirement | Description |
|---|---|---|
| `Authorization` | MUST | `Bearer <access_token>` |

**Response fields (per message object):**

| Field | Type | Requirement | Description |
|---|---|---|---|
| `message_id` | string | MUST | Unique identifier for this inbox entry; used for acknowledgement |
| `received_at` | integer | MUST | Unix timestamp of when the QTSP received the message |
| `message` | object | MUST | DIDComm message (`application/didcomm-encrypted+json` or `application/didcomm+json`) |

**Responses:**

| Status | Meaning |
|---|---|
| `200 OK` | JSON array of pending messages (empty array if none) |
| `401 Unauthorized` | Missing or invalid access token |

**Example response:**
```json
[
  {
    "message_id": "3f2a1b4c-8d9e-4f5a-b6c7-d8e9f0a1b2c3",
    "received_at": 1234567890,
    "message": {
      "ciphertext": "<base64url>",
      "protected": "<base64url>",
      "recipients": [{"header": {"kid": "did:euid:DEK1101R.HRB116737#key-agreement-1"}}],
      "tag": "<base64url>",
      "iv": "<base64url>"
    }
  }
]
```

---

### 21.7 DIDComm Inbox Acknowledgement

*Direction:* EBW -> QTSP  
*Method:* HTTPS DELETE  
*Path:* `{didcomm_endpoint}/inbox/{message_id}`

**Path parameters:**

| Parameter | Requirement | Description |
|---|---|---|
| `message_id` | MUST | The `message_id` from the inbox polling response |

**Request headers:**

| Header | Requirement | Description |
|---|---|---|
| `Authorization` | MUST | `Bearer <access_token>` |

**Responses:**

| Status | Meaning |
|---|---|
| `204 No Content` | Message acknowledged and removed from inbox |
| `401 Unauthorized` | Missing or invalid access token |
| `404 Not Found` | Message not found or already acknowledged |

**Example request:**
```http
DELETE /didcomm/inbox/3f2a1b4c-8d9e-4f5a-b6c7-d8e9f0a1b2c3 HTTP/1.1
Host: qtsp.example
Authorization: Bearer eyJhbGciOiJFUzI1NiJ9.<payload>.<signature>
```

---

# 22. Conformance

An implementation **conforms to this specification** if it implements the requirements in Sections 17 and 10 for its role and supports the flows in Sections 12–15, 8–9, 19, and 20.

**Conformance class: QTSP**

An implementation conforms as a **QTSP** if it:

1. Implements all MUST requirements in Sections 17.1 and 10.1
2. Supports the onboarding flow (Section 12), message submission (Section 14), and message reception (Section 15) flows
3. Supports `did:euid` registration (Section 8) and delegated resolution (Section 9.1)
4. Serves a valid signed QTSP metadata document (Section 11)
5. Complies with WBCS-002 as Verifier for identity verification steps
6. Relays WACI-DIDComm payloads without modification (Sections 19 and 20)

**Conformance class: EBW (Issuer)**

An implementation conforms as an **EBW Issuer** if it:

1. Implements all MUST requirements in Sections 17.2 and 10.2
2. Supports the onboarding flow as the subscriber (Section 12)
3. Supports HTTPS POST transport (WebSocket OPTIONAL)
4. Supports the credential issuance flow (Section 19)
5. Stores all received ERDS evidence records durably

**Conformance class: EBW (Holder)**

An implementation conforms as an **EBW Holder** if it:

1. Implements all MUST requirements in Sections 17.2 and 10.2
2. Supports the onboarding flow as the subscriber (Section 12)
3. Supports HTTPS POST transport (WebSocket OPTIONAL)
4. Supports the credential issuance (Section 19) and presentation (Section 20) flows
5. Generates credential key pairs inside a hardware-backed secure element or WSCA/QSCD where available
6. Stores all received ERDS evidence records and issued credentials durably

**Conformance class: EBW (Verifier)**

An implementation conforms as an **EBW Verifier** if it:

1. Implements all MUST requirements in Sections 17.2 and 10.2
2. Supports the onboarding flow as the subscriber (Section 12)
3. Supports HTTPS POST transport (WebSocket OPTIONAL)
4. Supports the credential presentation flow (Section 20)
5. Stores all received ERDS evidence records durably

An EBW implementation **MAY** conform to multiple conformance classes simultaneously. Additional WE BUILD profiles **MAY** define stricter requirements for specific use cases. Such profiles **MUST NOT** weaken the mandatory requirements in this specification.

---

# 23. Security Considerations

**Access token lifetime:** Access tokens MUST expire within 1 hour. This short window compensates for the absence of mandatory key-binding (DPoP). Token binding via DPoP (RFC 9449) is OPTIONAL and RECOMMENDED for deployments requiring higher assurance against token theft.

**DIDComm message integrity:** EBW↔QTSP messages are protected by TLS. JWE encryption at the application layer is OPTIONAL for this leg. WACI inner payloads (EBW-to-EBW) MUST be JWE-encrypted since they traverse two QTSP hops where TLS is terminated. Signing (JWS) is OPTIONAL but RECOMMENDED for use cases requiring non-repudiation beyond the ERDS evidence chain.

**DID Document authenticity:** Resolved DID Documents are only as trustworthy as the WE BUILD discovery infrastructure that produced them. QTSPs MUST NOT serve DID Documents from untrusted or unauthenticated sources. The trust model for the discovery infrastructure is defined by the WE BUILD Trust Registry Infrastructure specification.

**Key rotation:** Subscriber key rotation invalidates the existing DID Document. The EBW MUST generate a new key pair and re-register via onboarding. The QTSP MUST update the discovery infrastructure entry within 24 hours. Any cached DID Documents referencing the old key MUST be discarded.

**Post-quantum readiness:** The encryption algorithms specified in Section 13.4 (ECDH-ES family, A256GCM) are not post-quantum safe. Implementations MUST use modular cryptographic interfaces to permit future migration to ML-KEM or equivalent post-quantum key encapsulation mechanisms when standardized for DIDComm. This is consistent with the WE BUILD ADR requirement for a PQC-safe path before 2035.

**OpenID4VP reuse attacks:** The nonce in each OpenID4VP challenge MUST be unique per session to prevent replay of a prior presentation.

**Credential content privacy from QTSP:** WACI-DIDComm payloads (credential offers, requests, issued credentials, and presentations) are encrypted to the final recipient EBW's key and MUST be treated as opaque by both QTSPs. A QTSP MUST NOT attempt to decrypt, log, or inspect the inner payload of a WACI-DIDComm transmission. The QERDS evidence records the *fact* of transmission with a qualified timestamp - not the credential content.

**PoP JWT replay:** The `proof_of_possession` JWT in `request-credential` MUST be single-use. An Issuer MUST reject any second `request-credential` message presenting the same nonce, even if the PoP JWT signature is valid.

**Presentation nonce binding:** The `nonce` in `request-presentation` prevents replay of a prior presentation. The Holder MUST generate a fresh `kb-jwt` for every presentation response and MUST NOT cache or reuse `kb-jwt` values across requests.

---

# References

[RFC 2119] Bradner, S. (1997) *Key words for use in RFCs to indicate Requirement Levels*. IETF. Available at: https://datatracker.ietf.org/doc/html/rfc2119

[DIDComm] Hardman, D. et al. (2024) *DIDComm Messaging v2.1*. Decentralised Identity Foundation. Available at: https://identity.foundation/didcomm-messaging/spec/v2.1/

[DID-CORE] Sporny, M. et al. (2022) *Decentralised Identifiers (DIDs) v1.0*. W3C Recommendation. Available at: https://www.w3.org/TR/did-core/

[ADR-QERDS] Dijkhuis, S., Johansson, L. (2026) *WE BUILD ADR: Deliver business wallet data using QERDS*. WE BUILD Consortium. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/build-qerds.md

[QERDS-ARCH] WP4 QTSP Group (2026) *Architecture overview for QERDS in WE BUILD*. WE BUILD Consortium. Available at: https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qerds/architecture.md

[QTSP-SPEC] WP4 QTSP Group (2026) *WE BUILD QTSP Specification*. WE BUILD Consortium. Available at: https://github.com/webuild-consortium/wp4-qtsp-group (URL to be confirmed)

[BRIS] European Commission (2017) *Business Registers Interconnection System (BRIS)*. Available at: https://e-justice.europa.eu/489/EN/business_registers__search_for_a_company_in_the_eu

[QERDS-INTEROP] WP4 QTSP Group (2026) *QERDS Interoperability Framework Requirements*. WE BUILD Consortium. Available at: https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qerds/interop-framework.md

[WBCS-002] WE BUILD Consortium (2025) *WE BUILD Conformance Specification: Credential Presentation v1.0*. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/cs-02-credential-presentation.md

[EN-319-522-3] ETSI (2022) *Electronic Signatures and Infrastructures (ESI); Electronic Registered Delivery Services; Part 3: Formats*. ETSI EN 319 522-3.

[EN-319-522-4-1] ETSI (2023) *Electronic Signatures and Infrastructures (ESI); Electronic Registered Delivery Services; Part 4-1: Bindings; Sub-part 1: Bindings for Message Transfer*. ETSI EN 319 522-4-1.

[EU-2025-1944] European Commission (2025) *Commission Implementing Regulation (EU) 2025/1944*. Available at: https://eur-lex.europa.eu/eli/reg_impl/2025/1944/oj

[RFC 9449] Fett, D. et al. (2023) *OAuth 2.0 Demonstrating Proof of Possession (DPoP)*. IETF RFC 9449. Available at: https://datatracker.ietf.org/doc/html/rfc9449

[ISO-6523] ISO (1998) *Information technology - Structure for the identification of organizations and organization parts*. ISO 6523.

[WACI-DIDCOMM] Decentralised Identity Foundation (2023) *WACI-DIDComm: Wallet and Credential Interaction over DIDComm*. DIF Working Group. Available at: https://identity.foundation/waci-didcomm/

[WACI-ISSUE] Decentralised Identity Foundation (2023) *WACI-DIDComm: Issue Credential Protocol 3.0*. DIF Working Group. Available at: https://github.com/decentralized-identity/waci-didcomm/blob/main/issue_credential/README.md

[WACI-PRESENT] Decentralised Identity Foundation (2023) *WACI-DIDComm: Present Proof Protocol 3.0*. DIF Working Group. Available at: https://github.com/decentralized-identity/waci-didcomm/blob/main/present_proof/README.md

[DIF-PE] Decentralised Identity Foundation (2023) *Presentation Exchange 2.0*. DIF Working Group. Available at: https://identity.foundation/presentation-exchange/spec/v2.0.0/

[SD-JWT-VC] Fett, D. et al. (2024) *SD-JWT-based Verifiable Credentials*. IETF. Available at: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-sd-jwt-vc