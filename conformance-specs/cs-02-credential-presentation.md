# WE BUILD - Conformance Specification:  Credential Presentation

Version 1.0

Table Of Contents

- [WE BUILD - Conformance Specification:  Credential Presentation](#we-build---conformance-specification--credential-presentation)
- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language](#3-normative-language)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
- [6. High-level Flows](#6-high-level-flows)
  - [6.1 Same-device Presentation Flow](#61-same-device-presentation-flow)
    - [6.1.1 Presentation Request Creation](#611-presentation-request-creation)
    - [6.1.2 WU Invocation](#612-wu-invocation)
    - [6.1.3 WU Validation](#613-wu-validation)
    - [6.1.4 Holder Consent](#614-holder-consent)
    - [6.1.5 Presentation Generation](#615-presentation-generation)
    - [6.1.6 Presentation Submission](#616-presentation-submission)
    - [6.1.7 Result Handling](#617-result-handling)
  - [6.2 Cross-device Presentation Flow](#62-cross-device-presentation-flow)
    - [6.2.1 Presentation Request Creation and Display](#621-presentation-request-creation-and-display)
    - [6.2.2 Wallet Unit Invocation via QR](#622-wallet-unit-invocation-via-qr)
    - [6.2.3 Wallet Validation](#623-wallet-validation)
    - [6.2.4 Holder Consent](#624-holder-consent)
    - [6.2.5 Presentation Generation](#625-presentation-generation)
    - [6.2.6 Presentation Submission](#626-presentation-submission)
    - [6.2.7 Result Handling](#627-result-handling)
- [7. Normative Requirements](#7-normative-requirements)
  - [7.1 Wallet Unit Requirements](#71-wallet-unit-requirements)
  - [7.2 Verifier Requirements](#72-verifier-requirements)
- [8. Interface Definitions](#8-interface-definitions)
  - [8.1 Wallet Invocation Interface](#81-wallet-invocation-interface)
  - [8.2 Presentation Request Object Interface](#82-presentation-request-object-interface)
  - [8.3 Presentation Endpoint](#83-presentation-endpoint)
  - [8.4 Verifier Metadata Interface](#84-verifier-metadata-interface)
- [9. Conformance](#9-conformance)
- [References](#references)

# 1. Introduction

This document defines the **WE BUILD Conformance Specification for Credential Presentation**, describing how Wallet Units (WU) and Verifiers interoperate using OpenID for Verifiable Presentations (OpenID4VP) 1.0 [1] in alignment with the OpenID4VC High Assurance Interoperability Profile (HAIP) 1.0 - Implementer’s Draft 1 [2], based on the decision recorded in WE BUILD [ADR Base Protocols](https://github.com/webuild-consortium/architecture/blob/main/adr/base-protocols.md).

It specifies a high‑assurance presentation profile for use within the WE BUILD ecosystem, covering:

* Presentation request and response flows
* Interfaces between Wallets and Verifiers
* Security, privacy and interoperability requirements
* Support for SD‑JWT‑VC credentials [3]
* Same‑device and cross‑device invocation patterns

This document complements the WE BUILD Conformance Specification: Credential Issuance v1.0. The document is used to build the WE BUILD Interoperability Test Bed Plus (ITB+) [4].


# 2. Scope

This specification defines the conformance profile for high‑assurance credential presentation:

* Requirements for:
    * WUs that respond to presentation requests
    * Verifiers that initiate presentation requests
* Mandatory features:
    * OpenID4VP 1.0
    * HAIP ID‑1 Section 5 requirements
    * JWT‑based Presentation Proof
    * SD‑JWT‑VC selective disclosure
    * Same‑device and cross‑device invocation
    * openid4vp:// Wallet invocation

# 3. Normative Language

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, REQUIRED, RECOMMENDED, MAY and OPTIONAL are to be interpreted as described in RFC 2119.


# 4. Roles and Components

This specification uses the following roles:

* **Wallet Unit (WU):** A client application or component acting on behalf of the Holder to obtain and store Verifiable Credentials.
* **Holder:** The subject or representative of the subject who controls the Wallet Unit.
* **Verifier:** Entity requesting verifiable presentations, validating responses and making authorisation decisions.

# 5. Protocol Overview

The WE BUILD presentation profile is based on OpenID4VP with the following mandatory features defined by HAIP ID-1:

* JWT-Secured Authorisation Request (JAR): All authorisation requests MUST be signed.
* Digital Credentials Query Language (DCQL): MUST be used for querying credentials.
* Client Identifier Schemes: Usage of `x509_san_dns` or `verifier_attestation`, `decentralized_identifiers` is also recommended (`did:web`, `did:jwk`)
* Crypto Suites: Strict adherence to P-256 (secp256r1) with ES256 for signing.
* Holder Binding: Mandatory Key Binding JWT (KB-JWT) for SD-JWT VCs. (See **NOTE_CS02_01**)

High‑level steps:

1. Verifier creates Presentation Request
2. Wallet is invoked via openid4vp:// (same or cross device)
3. Wallet validates Presentation Request
4. Holder consents
5. Wallet generates Presentation Proof + Disclosures
6. Wallet submits Presentation Response
7. Verifier validates and produces outcome

***NOTE_CS02_01: ISO18013-5 and  ISO18013-7 will be supported in subsequent versions based on use case requirements.***


# 6. High-level Flows

This chapter defines the presentation flows required by WE BUILD.

## 6.1 Same-device Presentation Flow

### 6.1.1 Presentation Request Creation

The Verifier prepares a signed Presentation Request Object containing:

* Requested credential types
* Disclosure constraints
* Proof requirements (nonce, audience)
* Expiry (exp)
* Verifier identifier (client_id)

The request MUST be integrity‑protected (JAR‑style or equivalent).

### 6.1.2 WU Invocation

The Verifier redirects the user-agent to the WU using:

```
openid4vp://present?request_uri=<URL>
```

Wallet retrieves or validates the signed Presentation Request Object.

### 6.1.3 WU Validation

The WU MUST validate:

* Signature of Presentation Request
* Nonce freshness
* Audience matches Wallet
* Expiry validity
* Credential types and disclosure constraints
* Request integrity

Unsigned or invalid requests MUST be rejected.


### 6.1.4 Holder Consent

The WU MUST display:

* Verifier identity
* Requested credential types
* Requested attributes or claims
* Any selective disclosure details

Holder MUST explicitly consent.

### 6.1.5 Presentation Generation

Upon consent, the Wallet MUST generate:

* JWT‑based Presentation Proof
* Selective disclosures for SD‑JWT‑VC
* Binding between:
    * Presentation Proof and Wallet‑held key
    * Nonce
    * Audience


### 6.1.6 Presentation Submission

The Wallet MUST POST the Presentation Response to the Verifier’s Presentation Endpoint, including:

* `vp_token` containing the JWT‑encoded Presentation
* format specifying SD‑JWT‑VC

Sender‑constrained token usage MUST be applied if configured.


### 6.1.7 Result Handling

The Verifier MUST return:

* A success object if verification succeeded
* Error information when the presentation is invalid or incomplete

Wallet MUST correctly display the outcome to the Holder.


## 6.2 Cross-device Presentation Flow


### 6.2.1 Presentation Request Creation and Display

Verifier constructs the Presentation Request Object (as in 6.1.1) and encodes it in a QR‑based `openid4vp://` URL.


### 6.2.2 Wallet Unit Invocation via QR

Holder scans the QR code. WU retrieves the Presentation Request Object (embedded or via `request_uri`).

### 6.2.3 Wallet Validation

The same validation rules as 6.1.3 apply.

### 6.2.4 Holder Consent

Same as 6.1.4.


### 6.2.5 Presentation Generation

Same as 6.1.5.

### 6.2.6 Presentation Submission

WU delivers the Presentation directly to the Verifier’s Presentation Endpoint (back channel). Redirection flow MAY be used if supported.

### 6.2.7 Result Handling

Verifier processes the Presentation and returns the outcome as in 6.1.7.


# 7. Normative Requirements


## 7.1 Wallet Unit Requirements

Wallets MUST:

1. Support HAIP‑compliant OpenID4VP.
2. Support the same‑device and cross‑device flows.
3. Support openid4vp://present invocation.
4. Validate signed Presentation Requests.
5. Implement SD‑JWT‑VC selective disclosure.
6. Provide transparent Holder consent.
7. Generate JWT‑based Presentation Proof.
8. Bind Presentation Proof to Verifier’s nonce and audience.
9. Submit Presentation Responses to the Presentation Endpoint.

Wallets MUST NOT:

* Accept unsigned or invalid Presentation Requests
* Auto‑consent
* Add unsolicited claims

## 7.2 Verifier Requirements

Verifiers MUST:

1. Create a signed Presentation Request Object.
2. Use nonces and audience restrictions.
3. Support same‑device and cross‑device invocation.
4. Publish Verifier Metadata.
5. Provide a Presentation Endpoint.
6. Validate all Presentation Responses, including:
    * Signature of Presentation Proof
    * Credential authenticity
    * SD‑JWT‑VC disclosure integrity
    * Holder binding
    * Nonce and audience binding
    * Satisfaction of request constraints

Verifiers MUST NOT:

* Request unnecessary personal information
* Disable nonce or audience validation

# 8. Interface Definitions

Interfaces in this chapter follow the structure from the Issuance Conformance Specification.

## 8.1 Wallet Invocation Interface

Direction: Verifier → Wallet \
Transport: `openid4vp://` scheme \
Usage: Same-device or cross-device scanning

Example:


```
openid4vp://present?request_uri=https://verifier.example.org/request/123
```


Wallet MUST retrieve or validate the Presentation Request Object.


## 8.2 Presentation Request Object Interface

The Presentation Request Object MUST include:

* Verifier identifier (`client_id`)
* `nonce`
* `audience`
* Requested credential types
* Disclosure constraints
* Proof requirements
* Expiry
* Signature (integrity-protected object)

Wallet Units reject incomplete or invalid request objects.


## 8.3 Presentation Endpoint

Direction: Wallet → Verifier \
Method: POST \
Authentication: MAY use sender-constrained tokens

**Request Body Example**

```
{ "vp_token": "<JWT-Presentation>", "format": "vc+sd-jwt" }
```

**Success Response Example**

```
{ "status": "ok" }
```

**Error Example**


```
{ "error": "invalid_presentation", "error_description": "Nonce invalid or expired" }
```

## 8.4 Verifier Metadata Interface

Verifiers MUST publish metadata containing:

* Presentation_endpoint
* Supported vp_formats
* Supported proof mechanisms
* JWK set for Request signing
* Required credential types

Wallet Units retrieves this metadata where available.


# 9. Conformance

An implementation **conforms to this specification as a Wallet Provider** if it:

1. Implements all Wallet requirements in Section 7.1
2. Implements all interfaces and behaviours in Section 8
3. Supports flows defined in Section 6
4. Supports SD‑JWT‑VC as defined for OpenID4VP

An implementation **conforms to this specification as an Issuer** if it:

1. Implements all Verifier requirements in Section 7.2
2. Publishes required Verifier Metadata
3. Implements the Presentation Request and Presentation Endpoint interfaces
4. Supports both same‑device and cross‑device flows

# References

[1]	OpenID Foundation (2025). OpenID for Verifiable Credential Issuance 1.0. OpenID Foundation, 16 September. Available at: [https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) (Accessed: 24 November 2025).

[2]	OpenID Foundation (2025) OpenID4VC High Assurance Interoperability Profile – draft 03. OpenID Foundation. Available at: [https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-ID1.html](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-ID1.html)  (Accessed: 24 November 2025)

[3]	IETF (2025) SD‑JWT‑based Verifiable Credentials. IETF. Available at: https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-09.html (Accessed: 24 November 2025).

[4]	WE BUILD (2025) Interoperability Test Bed - Reference Specification, 12 November, Available at: [https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md) (Accessed: 24 November 2025).