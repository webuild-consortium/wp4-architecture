# WE BUILD - Conformance Specification:  Credential Issuance

Version 1.0

Table Of Contents

- [WE BUILD - Conformance Specification:  Credential Issuance](#we-build---conformance-specification--credential-issuance)
- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language](#3-normative-language)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
- [6. High-level Flows](#6-high-level-flows)
  - [6.1 Wallet-initiated Issuance Flow](#61-wallet-initiated-issuance-flow)
    - [6.1.1 Configuration and discovery](#611-configuration-and-discovery)
    - [6.1.2 User selects credential](#612-user-selects-credential)
    - [6.1.3 Pushed Authorisation Request (PAR)](#613-pushed-authorisation-request-par)
    - [6.1.4 User authorisation](#614-user-authorisation)
    - [6.1.5 Token request](#615-token-request)
    - [6.1.6 Credential request](#616-credential-request)
    - [6.1.7 Storage](#617-storage)
  - [6.2 Issuer-initiated Issuance via Credential Offer](#62-issuer-initiated-issuance-via-credential-offer)
    - [6.2.1 Issuance decision](#621-issuance-decision)
    - [6.2.2 Credential Offer creation](#622-credential-offer-creation)
    - [6.2.3 Credential Offer delivery and Wallet invocation](#623-credential-offer-delivery-and-wallet-invocation)
    - [6.2.4 WU processes the offer](#624-wu-processes-the-offer)
    - [6.2.5 Authorisation and token exchange](#625-authorisation-and-token-exchange)
    - [6.2.6 Credential Request](#626-credential-request)
    - [6.2.7 Deferred Credential Request](#627-deferred-credential-request)
  - [6.3 Deferred Credential Request](#63-deferred-credential-request)
- [7. Normative Requirements](#7-normative-requirements)
  - [7.1 Common requirements (WU and Issuer)](#71-common-requirements-wu-and-issuer)
  - [7.2 Credential Offer](#72-credential-offer)
  - [7.3 Authorisation Endpoint and PAR](#73-authorisation-endpoint-and-par)
  - [7.4 Token Endpoint and Wallet Attestation](#74-token-endpoint-and-wallet-attestation)
  - [7.5 Credential Endpoint](#75-credential-endpoint)
  - [7.6 Deferred Credential Endpoint](#76-deferred-credential-endpoint)
  - [7.7 Server Metadata](#77-server-metadata)
- [8. Interface Definitions](#8-interface-definitions)
  - [8.1 WU Invocation Interface](#81-wu-invocation-interface)
  - [8.2 Credential Offer Interface](#82-credential-offer-interface)
  - [8.3 PAR Endpoint](#83-par-endpoint)
  - [8.4 Token Endpoint](#84-token-endpoint)
  - [8.5 Credential Endpoint](#85-credential-endpoint)
  - [8.7 Deferred Credential Endpoint](#87-deferred-credential-endpoint)
  - [8.8 Metadata Endpoints](#88-metadata-endpoints)
- [9. Conformance](#9-conformance)
- [References](#references)


# 1. Introduction

This document defines the **WE BUILD Consortium Conformance Specification (CS)** for high assurance credential issuance based on the decision recorded in WE BUILD [ADR Base Protocols](https://github.com/webuild-consortium/architecture/blob/main/adr/base-protocols.md).

It profiles:

* OpenID for Verifiable Credential Issuance (OpenID4VCI) v1.0 [1]
* The OpenID4VC High Assurance Interoperability Profile (HAIP) 1.0 - Implementers Draft 1 [2]

The aim is to ensure that Wallet Units and Credential Issuers within the WE BUILD ecosystem interoperate consistently for the **issuance of SD-JWT-VC credentials** [3] with high security and privacy.

This specification focuses **only on issuance**. Presentation, verification of requirements, and trust management are out of scope and covered in separate documents. The document is used to build the WE BUILD Interoperability Test Bed Plus (ITB+) [4].


# 2. Scope

This specification defines:

* A profile of OpenID4VCI for issuing SD-JWT-VC credentials
* Requirements for:
    * Wallets that receive credentials
    * Credential Issuers and their Authorisation Servers
* Support for:
    * Wallet-initiated issuance
    * Issuer-initiated issuance via Credential Offer

This document describes:

* Protocol flows for high assurance issuance
* Interfaces and endpoints, including Wallet invocation, Credential Offer, Pushed Authorisation Requests (PAR), Token Endpoint, Credential Endpoint and metadata

# 3. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are to be interpreted as commonly used in technical specifications.

# 4. Roles and Components

This specification uses the following roles:

* **Wallet Unit (WU):** A client application or component acting on behalf of the Holder to obtain and store Verifiable Credentials.
* **Holder:** The subject or representative of the subject who controls the Wallet Unit.
* **Attestation Provider (Issuer):** The entity that decides to issue Verifiable Credentials and controls issuance policy.
* **Authorisation Server (AS):** The OAuth 2.0 and OpenID provider responsible for authenticating the user and issuing tokens for the Issuer. It may be co-located with the Issuer.


# 5. Protocol Overview

The WE BUILD issuance profile is based on the OAuth 2.0 Authorisation Code Flow with the following mandatory features:

* Authorisation Code and Pre-Authorised Code Flow for all issuance interactions
* OpenID4VCI SD-JWT-VC credential format profile (See NOTE **CS01_01**)
* Sender-constrained tokens, for example, using Demonstration of Proof of Possession (DPoP) or mutual TLS
* PKCE with `S256` code challenge method
* Pushed Authorisation Requests (PAR) for all authorisation requests
* *Wallet Unit Attestation (WUA) for client authentication as defined in OpenID4VCI-based ADR XX (To be written).*

Issuance can be:

* **Wallet-initiated**: the Holder starts from the WU and selects a credential type
* **Issuer-initiated**: the Issuer provides a **Credential Offer** that the WU consumes

Both modes are required in this profile.

> [!NOTE]
> CS01_01: ISO18013-5 and ISO18013-7 will be supported in subsequent versions, based on use-case requirements.

# 6. High-level Flows

This section presents the flows as text-based sequence descriptions.

## 6.1 Wallet-initiated Issuance Flow

**Actors**: Holder, WU, Issuer (AS and Credential Issuer).


### 6.1.1 Configuration and discovery

1. The WU retrieves Issuer metadata, which includes:
    * OAuth and OpenID configuration
    * Credential Issuer metadata
    * Mapping between credential types and `scope` values

### 6.1.2 User selects credential

1. The Holder chooses a credential type, for example, a PID, QEAA or business credential.
2. The WU selects the appropriate Issuer and the corresponding `scope` value.


### 6.1.3 Pushed Authorisation Request (PAR)

1. The WU constructs an authorisation request containing, at a minimum:
        * `client_id`
        * `scope` identifying the credential type
        * `code_challenge` using PKCE `S256`
        * `redirect_uri`
        * `response_type=code`
        * `state`
        * `nonce`
1. The WU sends this request to the Issuer’s PAR endpoint, with client authentication bound to the WUA. \

2. The PAR endpoint returns a `request_uri` and a validity period.


### 6.1.4 User authorisation

1. The WU directs the Holder’s user-agent to the Authorisation Endpoint with the `request_uri` obtained from PAR.
2. The Holder authenticates to the AS in accordance with the Issuer’s policy.
3. The Holder consents to the issuance of the requested credential.
4. The AS redirects back to the WU with an authorisation `code` and `state`.

### 6.1.5 Token request

1. The WU sends a token request to the Token Endpoint, including:
        * `grant_type=authorization_code`
        * `code`
        * `redirect_uri`
        * `code_verifier` matching the earlier `code_challenge`
        * client authentication using WUA
2. The Token Endpoint validates the request and returns:
        * sender-constrained `access_token`
        * optional `refresh_token` for credential refresh

### 6.1.6 Credential request

1. The WU sends a request to the Credential Endpoint containing:
        * `Authorization: Bearer {access_token}`
        * the requested credential format (SD-JWT-VC / mdoc)
        * a `proof` object using the `JWT` proof type that binds the credential to the WU’s subject key

2. The Credential Issuer validates:
        * the access token and its sender-constraining mechanism
        * the proof JWT
        * issuance policy

3. The Issuer returns the issued SD-JWT-VC.


### 6.1.7 Storage

1. The WU validates the credential signature and Issuer binding.
2. The WU stores the credential under the Holder's control.


## 6.2 Issuer-initiated Issuance via Credential Offer

**Actors**: Holder, WU, Issuer.

### 6.2.1 Issuance decision

1. The Holder interacts with the Issuer, for example, digital onboarding, customer due diligence or contract signing.

2. Following successful internal checks, the Issuer decides to issue one or more credentials.

### 6.2.2 Credential Offer creation

1. The Issuer constructs a **Credential Offer object** that includes:
   * the `credential_issuer` identifier
   * grant information for the `authorization_code` grant type
   * one or more identifiers for supported credential types
   * for each type, a `scope` value that maps unambiguously to that credential type

### 6.2.3 Credential Offer delivery and Wallet invocation

1.	The Issuer delivers the offer to the Holder by one of:

	* displaying a QR code that encodes a URL which uses the `openid-credential-offer://` scheme to invoke the WU
   * sending a link that uses the `openid-credential-offer://` scheme to a device with a registered WU

2.	Both same-device and cross-device delivery methods MUST be supported.

### 6.2.4 WU processes the offer

1.	The WU is invoked via `openid-credential-offer://` and receives the Credential Offer.

2.	The WU parses the offer and determines:
   * Issuer base URL
 * offered credential types
 * associated `scope` values used for authorisation 

3. The WU displays the offer to the Holder and asks for confirmation to proceed.


### 6.2.5 Authorisation and token exchange

1. The WU initiates the Authorisation Code Flow using PAR as defined in Section 6.1, reusing `scope` values from the offer.

2. The remainder of the flow, including authorisation, token request, credential request and storage, is identical to the Wallet-initiated flow.

### 6.2.6 Credential Request

The Wallet sends a Credential Request (or Batch Request) to the Credential Endpoint, including:

* `Authorization: Bearer {access_token}`
* SD‑JWT‑VC configuration
* `proof` object


### 6.2.7 Deferred Credential Request

If issuance cannot be completed immediately, the Issuer returns:

* `acceptance_token`
* optional `interval` (retry hint)

Batch requests may contain both immediate and deferred items.

## 6.3 Deferred Credential Request

Deferred issuance applies to both wallet-initiated and issuer-initiated flows.

When the Credential Issuer cannot immediately produce one or more credentials:

1. The Issuer returns:
    * `acceptance_token`
    * optional `interval` (retry hint) \

2. The WU MUST store the acceptance_token associated with the pending credential(s). \

3. The WU periodically retries using the acceptance_token until:
    * the credential is successfully issued, or
    * The Issuer signals an unrecoverable error. \

4. Batch requests may contain a mix of immediate and deferred items. Each deferred item receives its own acceptance_token and can be polled independently.

# 7. Normative Requirements

This section summarises the mandatory requirements for WE BUILD implementations.

## 7.1 Common requirements (WU and Issuer)

Both WU and Issuer **MUST**:

1. Support the Authorisation Code Flow as the only flow for credential issuance.
2. Support the SD-JWT-VC credential format profile as defined for OpenID4VCI.
3. Support sender-constrained tokens, for example, using DPoP or mutual TLS.
4. Support PKCE with the `S256` code challenge method for all authorisation requests.
5. Support Wallet-initiated and Issuer-initiated issuance.

## 7.2 Credential Offer

Issuers **MUST**:

1. Support the grant type `authorization_code` in Credential Offers, aligned with OpenID4VCI.
2. Include a `scope` value for each offered credential type so that the Wallet can identify the correct type and use the same value in the authorisation request.
3. Support both same-device and cross-device sending of Credential Offers.
4. Support at least the `openid-credential-offer://` custom URL scheme for Wallet invocation.

WUs **MUST**:

1. Be able to parse a Credential Offer that uses `authorization_code` as the grant type.
2. Use the `scope` value from the offer in the authorisation request.
3. Support invocation via the `openid-credential-offer://` custom URL scheme.

## 7.3 Authorisation Endpoint and PAR

Issuers **MUST**:

1. Require Pushed Authorisation Requests (PAR) for all authorisation requests. Direct front-channel authorisation requests without PAR MUST NOT be used.
2. Ensure that the Wallet authenticates at the PAR endpoint using the same method as used for client authentication at the Token Endpoint.

WUs **MUST**:

1. Use PAR for all authorisation requests.
2. Use the `scope` parameter to indicate the credential type to be issued. Each `scope` value MUST map to a specific credential type that is known from Issuer metadata or from the Credential Offer.
3. Ensure that the `client_id` in the PAR request matches the `sub` claim in the Wallet attestation JWT used for client authentication.

## 7.4 Token Endpoint and Wallet Attestation

WUs **MUST**:

1. Perform client authentication at the Token Endpoint using wallet attestation as defined in Annexe E of the OpenID4VCI specification.
2. Include the public key, and optionally a trust chain, used to validate the Wallet attestation in the `x5c` JOSE header of the attestation JWT.
3. Ensure the `sub` claim in the Wallet attestation JWT equals the `client_id` used in PAR and token requests.

Issuers **SHOULD**:

1. Support refresh tokens for credential refresh, following OpenID4VCI guidance on refresh usage and lifetime.

## 7.5 Credential Endpoint

Issuers **MUST**:

1. Support the `JWT` proof type in the Credential Endpoint.
2. Support the SD-JWT-VC credential format and validate the proof binding between the Wallet subject and credential.

Wallets **MUST**:

1. Send a proof JWT that contains claims required by the Issuer to bind the credential to the Wallet’s subject key.
2. Validate the returned SD-JWT-VC, including:
    * signature
    * Issuer identifier
    * key binding and any status information, according to the SD-JWT-VC profile

## 7.6 Deferred Credential Endpoint

Issuers **MUST**:

* Support a `deferred_credential_endpoint`.
* Return `acceptance_token` when issuance is delayed.
* Validate `acceptance_token` and ensure proper lifetime and binding.
* Publish endpoint in metadata.

Issuers **SHOULD**:

* Provide clear retry guidance.
* Return explicit errors when expired or failed.

Wallets **MUST**:

* Recognise deferred responses and store the `acceptance_token`.
* Call the Deferred Credential Endpoint until the credential is ready or the transaction ends.
* Distinguish *pending* vs *failed* issuance in UI.

Wallets **SHOULD**:

* Apply poll intervals/back‑off.
* Allow users to stop polling.


## 7.7 Server Metadata

Issuers **MUST** publish metadata that includes:

1. OAuth 2.0 and OpenID configuration, including Authorisation, Token and PAR endpoints.
2. Credential Issuer metadata that describes:
    * all supported credential types
    * a mapping from each credential type to a unique `scope` value

Wallets **MUST**:

1. Retrieve and process Issuer metadata, including the mapping from credential type to `scope`.
2. Use this mapping when constructing authorisation requests and when interpreting Credential Offers.

# 8. Interface Definitions

This section defines the logical interfaces for conformance. Exact URL paths are deployment-specific and discovered through metadata.


## 8.1 WU Invocation Interface

* **Direction**: Issuer to Wallet
* **Transport**: custom URL scheme and optional QR code
* **Requirement**:
	* Wallets and Issuers MUST support the `openid-credential-offer://` scheme as a minimal mechanism to invoke Wallets in both same-device and cross-device scenarios

**Example (illustrative)** 

```
openid-credential-offer://credential-offer?request_uri=...
```

The concrete parameters and encoding follow HAIP and OpenID4VCI guidance on Credential Offers.

## 8.2 Credential Offer Interface

* **Direction**: Issuer to WU

The **Credential Offer object** MUST contain at least:

* `credential_issuer`: base URL identifying the Issuer
* `grants`: object that includes support for `authorization_code`
* For each credential type:
    * a credential type identifier
    * the associated `scope` value

The exact JSON structure MUST comply with OpenID4VCI Credential Offer definitions.

## 8.3 PAR Endpoint

* **Direction**: Wallet to Issuer (AS)
* **Method**: `POST`

**Request (logical fields)**

* `client_id`
* `scope`
* `code_challenge` using PKCE `S256`
* `code_challenge_method=S256`
* `redirect_uri`
* `response_type=code`
* `state`, `nonce`

**Response**

* `request_uri`
* `expires_in`

All PAR requests MUST be client-authenticated according to Section 7.4.


## 8.4 Token Endpoint

* **Direction**: WU to Issuer (AS)
* **Method**: `POST`

**Request (logical fields)**

* `grant_type=authorization_code`
* `code`
* `redirect_uri`
* `code_verifier`
* client authentication using Wallet attestation JWT, for example, `client_assertion` and `client_assertion_type`

**Response**

* `access_token` (sender-constrained)
* `token_type`
* `expires_in`
* optional `refresh_token`

## 8.5 Credential Endpoint

* **Direction**: WU to Issuer
* **Method**: `POST`
**Request (logical fields)**

* HTTP header: `Authorization: Bearer {access_token}`
* Body:
    * `format` (for example, `vc+sd-jwt` or the identifier used in the chosen SD-JWT-VC profile)
    * identification of the requested credential configuration
    * `proof` object with:
        * `proof_type="jwt"`
        * `jwt` containing proof claims

**Response**
* SD-JWT-VC credential and any associated metadata defined by the OpenID4VCI SD-JWT-VC profile

## 8.7 Deferred Credential Endpoint

**Direction:** WU → Issuer \
**Method:** POST
**Request (logical fields)**

* HTTP header:
    * `Authorization: Bearer {token}`
    * `Content-Type: application/json`
* Body parameters:
* `transaction_id`

**Response**

A Deferred Credential Response MAY either provide the issued credentials or indicate that issuance is still pending.


If credential issuance is complete:

* The response MUST contain the **credentials** parameter
* HTTP status code MUST be **200 (OK)**.

If credential issuance is still pending

* The response MUST contain:
    * **transaction_id**: MUST match the request.
    * **interval:** recommended waiting time before retrying.
* HTTP status code MUST be **202 (Accepted)**.

**Error Response**
If the Deferred Credential Request is invalid, the Issuer returns an error response. 

* <code>invalid_transaction_id:</code> Indicates that the `transaction_id` was not issued by the Credential Issuer or has already been used.
* If the Credential Issuer can no longer issue the credential(s), it returns `credential_request_denied`. The WU stops retrying for the given `transaction_id`.

## 8.8 Metadata Endpoints

Issuers **MUST** publish:

* OpenID Provider and OAuth discovery document
* Credential Issuer metadata document

The latter MUST include:
* supported credential types
* for each type, the associated `scope` value

WU uses these documents for dynamic configuration.

# 9. Conformance

An implementation **conforms to this specification as a Wallet Provider** if it:

1. Implements the WU requirements in Sections 6 and 7.
2. Supports the interfaces defined for WU behaviour in Section 8.
3. Uses SD-JWT-VC and OpenID4VCI as profiled by the OpenID4VC High Assurance Interoperability Profile Implementer’s Draft, Section 4.

An implementation **conforms to this specification as an Issuer** if it:

1. Implements the Issuer requirements in Sections 6 and 7.
2. Publishes server metadata, including type to `scope` mappings.
3. Provides the PAR, Token, Credential and WU invocation interfaces described in Section 8.

Profiles may define additional constraints for specific WE BUILD credential types, such as PID, QEAA, or business credentials. Such profiles MUST NOT relax the mandatory requirements in this document. The specific issuance will be taken into a separate CS.

# References

[1]	OpenID Foundation (2025) OpenID for Verifiable Presentations 1.0. OpenID Foundation. Available at: [https://openid.net/specs/openid-4-verifiable-presentations-1_0.html](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) (Accessed: 24 November 2025).

[2]	OpenID Foundation (2025) OpenID4VC High Assurance Interoperability Profile – draft 03. OpenID Foundation. Available at: [https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-ID1.html](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-ID1.html)  (Accessed: 24 November 2025)

[3] IETF (2025) SD‑JWT‑based Verifiable Credentials. IETF. Available at: https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-09.html (Accessed: 24 November 2025).

[4]	WE BUILD (2025) Interoperability Test Bed - Reference Specification, 12 November, Available at: [https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md) (Accessed: 24 November 2025).
