# WE BUILD - Conformance Specification:  Credential Presentation

Version 1.2
Date: 23 September 2026

**Revision history**

* Version 1.2 (23 September 2026): Restricted the Verifier's `client_id` to the `x509_hash` Client Identifier Scheme, added `haip-vp://` and `eu-eaap://` as additional Wallet invocation schemes, and added the mandatory `verifier_info` parameter (RP Registrar-provided data and, where available, the WRPRC) to the Presentation Request Object, aligning with the finalised OpenID4VC HAIP 1.0 and ETSI TS 119 472-2, resolving issue [#341](https://github.com/webuild-consortium/wp4-architecture/issues/341). Also corrected and restructured Section 8.3 (Presentation Response Endpoint) to match OpenID4VP 1.0's actual `direct_post.jwt` semantics (encrypted `response` parameter, form-urlencoded transport, defined error codes, and the `redirect_uri` acknowledgement), and aligned Sections 6.1.6/6.1.7/6.2.6/6.2.7 accordingly.
* Version 1.1 (30 April 2026): Approved.

**Authors / Contributors**: WP4 Architecture

* Lal Chandran, iGrant.io, Sweden
* Sander Dijkhuis, Cleverbase, Netherlands
* George J Padayatti, iGrant.io, Sweden
* Nikolaos Triantafyllou, University of Aegean, Greece
* Malin Norlander, Bolagsverket, Sweden
* Martin Micuch, IDUnion, Germany

## Table Of Contents

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
  - [8.3 Presentation Response Endpoint](#83-presentation-response-endpoint)
  - [8.4 Verifier Metadata Interface](#84-verifier-metadata-interface)
- [9. Conformance](#9-conformance)
- [References](#references)

# 1. Introduction

This document defines the **WE BUILD Conformance Specification for Credential Presentation**, describing how Wallet Units (WU) and Verifiers interoperate using OpenID for Verifiable Presentations (OpenID4VP) 1.0 [1] in alignment with the OpenID4VC High Assurance Interoperability Profile (HAIP) 1.0 [2] and ETSI TS 119 472-2 [3], based on the decision recorded in WE BUILD [ADR Base Protocols](https://github.com/webuild-consortium/architecture/blob/main/adr/base-protocols.md).

It specifies a high‑assurance presentation profile for use within the WE BUILD ecosystem, covering:

* Presentation request and response flows
* Interfaces between Wallets and Verifiers
* Security, privacy and interoperability requirements
* Support for SD‑JWT‑VC credentials [4]
* Same‑device and cross‑device invocation patterns

This document complements the WE BUILD Conformance Specification: Credential Issuance v1.0. The document is used to build the WE BUILD Interoperability Test Bed Plus (ITB+) [5].


# 2. Scope

This specification defines the conformance profile for high‑assurance credential presentation:

* Requirements for:
    * WUs that respond to presentation requests
    * Verifiers that initiate presentation requests
* Mandatory features:
    * OpenID4VP 1.0
    * HAIP 1.0 Section 5 requirements
    * JWT‑based Presentation Proof
    * SD‑JWT‑VC selective disclosure
    * Same‑device and cross‑device invocation
    * `openid4vp://` and `eu-eaap://` Wallet invocation (`haip-vp://` OPTIONAL)
    * `x509_hash` Client Identifier Scheme for the Verifier's `client_id`
    * `verifier_info` parameter carrying RP Registrar-provided data and, where available, the WRPRC

# 3. Normative Language

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, REQUIRED, RECOMMENDED, MAY and OPTIONAL are to be interpreted as described in RFC 2119.


# 4. Roles and Components

The role names defined in this specification (Wallet Unit, Holder, Verifier) are **OpenID4VP protocol roles**, not organisational or product roles. A single software product may implement more than one role at different times, and any given role may be fulfilled by software that also performs other functions (for example, a Business Wallet implementing both Holder and Verifier roles in different interactions). The requirements in this specification attach to the role, not to the product or organisation that implements it.

This specification uses the following roles:

* **Wallet Unit (WU):** A software component on the Holder's device acting on behalf of the Holder to obtain, store and present Verifiable Credentials.

> **NOTE_CSCP_OAUTH_CLIENT** In OpenID4VP terminology, the OAuth Client role is played by the Verifier (Relying Party), not by the Wallet Unit. References to `client_id` in this specification refer to the Verifier.
* **Holder:** The subject or representative of the subject who controls the Wallet Unit.
* **Verifier:** Entity requesting verifiable presentations, validating responses and making authorisation decisions.

# 5. Protocol Overview

The WE BUILD presentation profile is based on OpenID4VP with the following mandatory features defined by HAIP 1.0 [2] and ETSI TS 119 472-2 [3]:

* JWT-Secured Authorisation Request (JAR): All authorisation requests MUST be signed.
* Digital Credentials Query Language (DCQL): MUST be used for querying credentials.
* Client Identifier Scheme: The Verifier's `client_id` MUST use the `x509_hash` Client Identifier Prefix. Other prefixes (`x509_san_dns`, `verifier_attestation`, `did:web`, `did:jwk`) MUST NOT be used. (See **NOTE_CS02_02**)
* Wallet Invocation Schemes: `openid4vp://` and `eu-eaap://` MUST be supported for non-API mediated invocation; `haip-vp://` MAY additionally be supported. (See **NOTE_CS02_03**)
* Verifier Info: The Request Object MUST contain the `verifier_info` parameter, carrying RP Registrar-provided data and, where the Verifier holds one, its WRPRC (Wallet-Relying Party Registration Certificate). (See **NOTE_CS02_04**)
* Crypto Suites: Strict adherence to P-256 (secp256r1) with ES256 for signing.
* Holder Binding: Mandatory Key Binding JWT (KB-JWT) for SD-JWT VCs. (See **NOTE_CS02_01**)

High‑level steps:

1. Verifier creates Presentation Request, including `verifier_info`
2. Wallet is invoked via `openid4vp://`, `eu-eaap://`, or `haip-vp://` (same or cross device)
3. Wallet validates Presentation Request
4. Holder consents
5. Wallet generates Presentation Proof + Disclosures
6. Wallet submits Presentation Response
7. Verifier validates and produces outcome

***NOTE_CS02_01: ISO18013-5 and  ISO18013-7 will be supported in subsequent versions based on use case requirements.***

***NOTE_CS02_02: The `x509_hash` Client Identifier Prefix identifies the Verifier by the base64url-encoded SHA-256 hash of its DER-encoded X.509 (access) certificate, as defined in OpenID4VP 1.0 [1] Section 5.9.3 and mandated by HAIP 1.0 [2] Section 5 ("the Verifier MUST use, and the Wallet MUST accept, the Client Identifier Prefix `x509_hash`").***

***NOTE_CS02_03: `eu-eaap://` is the custom URL scheme mandated for non-API mediated Wallet invocation by ETSI TS 119 472-2 [3], clause 6.4.1 (requirement OIDFVP-HAIP-REDIRECTS-03). `haip-vp://` is the OPTIONAL scheme defined by HAIP 1.0 [2] Section 5.1. WUs and Verifiers MUST support `openid4vp://` and `eu-eaap://`; `haip-vp://` support is OPTIONAL.***

***NOTE_CS02_04: `verifier_info` is a JSON array in the Request Object; one element (`format`: `registrar_dataset`) carries the RP Registrar-provided data, and, where the Verifier holds a WRPRC, a further element (`format`: `registration_cert`) carries the base64url-encoded WRPRC, per ETSI TS 119 472-2 [3] clause 6.3.2.2 (requirements OIDFVP-HAIP-COMMON-REQ-RO-01 to -16). See Section 8.2 for the structure.***


# 6. High-level Flows

This chapter defines the presentation flows required by WE BUILD.

## 6.1 Same-device Presentation Flow

### 6.1.1 Presentation Request Creation

The Verifier prepares a signed Presentation Request Object containing:

* Requested credential types
* Disclosure constraints
* Proof requirements (nonce, audience)
* Expiry (exp)
* Verifier identifier (client_id), using the `x509_hash` Client Identifier Scheme (**NOTE_CS02_02**)
* `verifier_info`, containing RP Registrar-provided data and, where available, the WRPRC (**NOTE_CS02_04**)

The request MUST be integrity‑protected (JAR‑style or equivalent).

### 6.1.2 WU Invocation

The Verifier redirects the user-agent to the WU using one of the supported invocation schemes (**NOTE_CS02_03**):

```
openid4vp://?request_uri=<URL>
eu-eaap://?request_uri=<URL>
haip-vp://?request_uri=<URL>   # OPTIONAL
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
* `client_id` uses the `x509_hash` Client Identifier Scheme (**NOTE_CS02_02**)
* `verifier_info` is present and contains RP Registrar-provided data; where a WRPRC is included, its validity

Unsigned or invalid requests, requests using a `client_id` scheme other than `x509_hash`, or requests missing `verifier_info` MUST be rejected.


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

The Wallet MUST POST the Presentation Response to the Verifier’s Presentation Response Endpoint as defined in Section 8.3, encrypted per Response Mode `direct_post.jwt`, including:

* `vp_token` containing the JWT‑encoded Presentation
* `state`, echoing the Presentation Request's `state` parameter, where present

If the Wallet cannot produce a Presentation, it MUST instead submit a Presentation Error Submission as defined in Section 8.3.


### 6.1.7 Result Handling

The Verifier's Response Endpoint MUST acknowledge the submission as defined in Section 8.3 (HTTP `200 OK` with an optional `redirect_uri`). Verification of the Presentation (Section 7.2 item 5) and communication of its outcome to the Holder MUST occur via the Verifier's own user interface, reached either directly (same-device) or via the `redirect_uri` (cross-device, or session-fixation protection).

Wallet MUST correctly display any outcome communicated to it to the Holder.


## 6.2 Cross-device Presentation Flow


### 6.2.1 Presentation Request Creation and Display

Verifier constructs the Presentation Request Object (as in 6.1.1) and encodes it in a QR‑based `openid4vp://`, `eu-eaap://`, or `haip-vp://` URL (**NOTE_CS02_03**).


### 6.2.2 Wallet Unit Invocation via QR

Holder scans the QR code. WU retrieves the Presentation Request Object (embedded or via `request_uri`).

### 6.2.3 Wallet Validation

The same validation rules as 6.1.3 apply.

### 6.2.4 Holder Consent

Same as 6.1.4.


### 6.2.5 Presentation Generation

Same as 6.1.5.

### 6.2.6 Presentation Submission

WU delivers the Presentation Response as in 6.1.6, directly to the Verifier’s Presentation Response Endpoint (back channel).

### 6.2.7 Result Handling

Verifier's Response Endpoint acknowledges the submission and the outcome is communicated to the Holder as in 6.1.7; the `redirect_uri` mechanism is the primary means of conveying the outcome back on the Wallet's device in this cross-device flow.


# 7. Normative Requirements

The requirements in 7.1 and 7.2 attach to the OpenID4VP **roles** of Wallet Unit and Verifier respectively, as defined in chapter 4, not to the products or organisations implementing them. A relying party deploying a multi-role software product (for example a Business Wallet) to implement the Verifier role is a normal and supported pattern; the obligations in 7.2 apply to the Verifier role inside that product.

## 7.1 Wallet Unit Requirements

Wallets MUST:

1. Support HAIP‑compliant OpenID4VP.
2. Support the same‑device and cross‑device flows.
3. Support invocation via the `openid4vp://` and `eu-eaap://` custom URL schemes; `haip-vp://` support is OPTIONAL.
4. Validate signed Presentation Requests.
5. Validate that the Verifier's `client_id` uses the `x509_hash` Client Identifier Scheme.
6. Validate the `verifier_info` parameter, including the RP Registrar-provided data and, where present, the WRPRC.
7. Implement SD‑JWT‑VC selective disclosure.
8. Provide transparent Holder consent.
9. Generate JWT‑based Presentation Proof.
10. Bind Presentation Proof to Verifier’s nonce and audience.
11. Submit Presentation Responses to the Presentation Response Endpoint.

Wallets MUST NOT:

* Accept unsigned or invalid Presentation Requests
* Accept requests whose `client_id` does not use the `x509_hash` Client Identifier Scheme
* Accept requests missing the `verifier_info` parameter
* Auto‑consent
* Add unsolicited claims

## 7.2 Verifier Requirements

Verifier obligations are listed below in two groups: per-transaction protocol behaviours, and deployment-time obligations. All items are normative MUSTs. The wallet's reciprocal duty for the same protocol step is referenced in parentheses.

**Verifiers MUST ensure, on every transaction, that:**

1. The Presentation Request Object is sealed (signed) by the Verifier. (Wallet reciprocal: 7.1.4)
2. Nonces and audience restrictions are generated and included. (Wallet reciprocal: 7.1.10)
3. The `client_id` uses the `x509_hash` Client Identifier Scheme. (Wallet reciprocal: 7.1.5)
4. `verifier_info` is included, carrying RP Registrar-provided data and, where the Verifier holds one, its WRPRC. (Wallet reciprocal: 7.1.6)
5. All Presentation Responses are validated, including:
    * Signature of Presentation Proof
    * Credential authenticity
    * Wallet Unit Attestation validity (per HAIP)
    * SD‑JWT‑VC disclosure integrity
    * Holder binding
    * Nonce and audience binding
    * Satisfaction of request constraints

   (Wallet reciprocal: 7.1.7 to 7.1.10)

**Verifiers MUST, at deployment:**

6. Support same‑device and cross‑device invocation, via `openid4vp://` and `eu-eaap://` (`haip-vp://` OPTIONAL). (Wallet reciprocal: 7.1.2, 7.1.3)
7. Publish Verifier Metadata.
8. Provide a Presentation Response Endpoint. (Wallet reciprocal: 7.1.11)

Verifiers MUST NOT:

* Request unnecessary personal information
* Disable nonce or audience validation
* Use a `client_id` scheme other than `x509_hash`
* Omit `verifier_info` from the Presentation Request Object

# 8. Interface Definitions

Interfaces in this chapter follow the structure from the Issuance Conformance Specification.

## 8.1 Wallet Invocation Interface

Direction: Verifier → Wallet \
Transport: `openid4vp://` or `eu-eaap://` scheme (WUs and Verifiers MUST support both); `haip-vp://` scheme (OPTIONAL) \
Usage: Same-device or cross-device scanning

Example:


```
openid4vp://?request_uri=https://verifier.example.org/request/123
eu-eaap://?request_uri=https://verifier.example.org/request/123
haip-vp://?request_uri=https://verifier.example.org/request/123
```


Wallet MUST retrieve or validate the Presentation Request Object.


## 8.2 Presentation Request Object Interface

The Presentation Request Object MUST include:

* Verifier identifier (`client_id`), using the `x509_hash` Client Identifier Scheme
* `nonce`
* `audience`
* Requested credential types
* Disclosure constraints
* Proof requirements
* Expiry
* `verifier_info`: a JSON array containing:
    * One element with `format`: `registrar_dataset`, whose `data` is a non-empty JSON object carrying the RP Registrar-provided data (identifier, service description, Registrar API URI, intended-use identifier, purpose, and privacy policy URI, and optionally the registered credential/attribute set)
    * Where the Verifier holds a WRPRC, one further element with `format`: `registration_cert`, whose `data` is the base64url‑encoded WRPRC
* Signature (integrity-protected object)

Wallet Units reject incomplete or invalid request objects, including requests with an unsupported `client_id` scheme or a missing `verifier_info` parameter.

**Example**

```json
{
  "client_id": "x509_hash:2jgUeqU3JDzTHXPfZbXgKN99IJJ9AH6f2ggeq1cQ0-o",
  "nonce": "n-0S6_WzA2Mj",
  "aud": "https://wallet.example.org",
  "verifier_info": [
    {
      "format": "registrar_dataset",
      "data": {
        "identifier": "urn:webuild:rp:example-001",
        "srvDescription": [{ "lang": "en", "value": "Example Verifier Service" }],
        "registryURI": "https://registrar.example.org/api",
        "intendedUseIdentifier": "urn:webuild:intended-use:001",
        "purpose": [{ "lang": "en", "value": "Age verification" }],
        "policyURI": "https://verifier.example.org/privacy"
      }
    },
    {
      "format": "registration_cert",
      "data": "<base64url-encoded WRPRC>"
    }
  ]
}
```


## 8.3 Presentation Response Endpoint

Direction: Wallet → Verifier's `response_uri` \
Method: POST \
Response Mode: `direct_post.jwt` (encrypted Authorization Response; MUST, per HAIP requirement OIDFVP-HAIP-COMMON-RESP-01) \
Request Content-Type: `application/x-www-form-urlencoded`

**Successful Presentation Submission**

The Wallet MUST POST a single `response` parameter whose value is a compact-serialized JWE (OpenID4VP 1.0 [1] Section 8.3). The decrypted JWE payload MUST be a JSON object containing:

* `vp_token`: REQUIRED. The JWT‑encoded Presentation(s), keyed by DCQL credential query `id`
* `state`: REQUIRED if a `state` parameter was present in the Presentation Request; its value MUST match

**Decrypted payload example**

```json
{
  "vp_token": { "<credential_query_id>": ["<SD-JWT-VC presentation>"] },
  "state": "<echoed state, if present in the request>"
}
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
3. Implements the Presentation Request and Presentation Response Endpoint interfaces
4. Supports both same‑device and cross‑device flows

# References

[1]	OpenID Foundation (2025). OpenID for Verifiable Presentations 1.0. OpenID Foundation, 9 July. Available at: [https://openid.net/specs/openid-4-verifiable-presentations-1_0.html](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) (Accessed: 24 November 2025).

[2]	OpenID Foundation (2025) OpenID4VC High Assurance Interoperability Profile 1.0. OpenID Foundation, 29 December. Available at: [https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html) (Accessed: 23 September 2026).

[3]	ETSI (2026) ETSI TS 119 472-2 V1.2.1: Electronic Signatures and Trust Infrastructures (ESI); Profiles for Electronic Attestation of Attributes; Part 2: Profiles for EAA/PID Presentations to Relying Party. Available at: [https://www.etsi.org/deliver/etsi_ts/119400_119499/11947202/01.02.01_60/ts_11947202v010201p.pdf](https://www.etsi.org/deliver/etsi_ts/119400_119499/11947202/01.02.01_60/ts_11947202v010201p.pdf) (Accessed: 23 September 2026).

[4]	IETF (2025) SD‑JWT‑based Verifiable Credentials. IETF. Available at: https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-09.html (Accessed: 24 November 2025).

[5]	WE BUILD (2025) Interoperability Test Bed - Reference Specification, 12 November, Available at: [https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md) (Accessed: 24 November 2025).
