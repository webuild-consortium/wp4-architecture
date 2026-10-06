# WE BUILD - Conformance Specification:  Credential Issuance

Version 1.3
Date: 28 August 2026

**Revision history**

* Version 1.3 (28 August 2026): Clarified that re-issuance and the Deferred Credential Endpoint are OPTIONAL for Issuers, resolving issue [#297](https://github.com/webuild-consortium/wp4-architecture/issues/297).
* Version 1.2 (15 July 2026): Added the re-issuance chapter, resolving issue [#244](https://github.com/webuild-consortium/wp4-architecture/issues/244).
* Version 1.1 (10 July 2026): Added the pre-authorised code-flow to support payments
* Version 1.0 (28 November 2025): Initial version.

**Authors / Contributors**: WP4 Architecture

* Lal Chandran, iGrant.io, Sweden
* Sander Dijkhuis, Cleverbase, Netherlands
* George J Padayatti, iGrant.io, Sweden
* Nikolaos Triantafyllou, University of Aegean, Greece
* Malin Norlander, Bolagsverket, Sweden
* Tomasz Blachowicz, Mastercard, Poland
* George Fourtounis, GRNET, Greece

## Table Of Contents

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
    - [6.2.5 Authorisation and token exchange (Authorisation Code grant)](#625-authorisation-and-token-exchange-authorisation-code-grant)
    - [6.2.6 Token request (Pre-Authorised Code grant)](#626-token-request-pre-authorised-code-grant)
    - [6.2.7 Credential Request, validation and storage](#627-credential-request-validation-and-storage)
  - [6.3 Deferred Credential Request](#63-deferred-credential-request)
  - [6.4 Re-issuance Flow](#64-re-issuance-flow)
    - [6.4.1 Re-issuance triggers](#641-re-issuance-triggers)
    - [6.4.2 Re-issuance using the Refresh Token grant](#642-re-issuance-using-the-refresh-token-grant)
    - [6.4.3 Fallback to the full authorisation flow](#643-fallback-to-the-full-authorisation-flow)
- [7. Normative Requirements](#7-normative-requirements)
  - [7.1 Common requirements (WU and Issuer)](#71-common-requirements-wu-and-issuer)
  - [7.2 Credential Offer](#72-credential-offer)
  - [7.3 Authorisation Endpoint and PAR](#73-authorisation-endpoint-and-par)
  - [7.4 Token Endpoint and Wallet Attestation](#74-token-endpoint-and-wallet-attestation)
  - [7.5 Credential Endpoint](#75-credential-endpoint)
  - [7.6 Deferred Credential Endpoint](#76-deferred-credential-endpoint)
  - [7.7 Server Metadata](#77-server-metadata)
  - [7.8 Re-issuance](#78-re-issuance)
- [8. Interface Definitions](#8-interface-definitions)
  - [8.1 WU Invocation Interface](#81-wu-invocation-interface)
  - [8.2 Credential Offer Interface](#82-credential-offer-interface)
  - [8.3 PAR Endpoint](#83-par-endpoint)
  - [8.4 Token Endpoint](#84-token-endpoint)
  - [8.5 Credential Endpoint](#85-credential-endpoint)
  - [8.6 Deferred Credential Endpoint](#86-deferred-credential-endpoint)
  - [8.7 Metadata Endpoints](#87-metadata-endpoints)
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
    * Re-issuance of previously issued attestations
    * Issuer-initiated issuance via Credential Offer, using the Authorisation Code grant or the Pre-Authorised Code grant

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

The WE BUILD issuance profile is based on the OAuth 2.0 Authorisation Code Flow and the OpenID4VCI Pre-Authorised Code Flow (grant type `urn:ietf:params:oauth:grant-type:pre-authorized_code`) with the following mandatory features:

* Authorisation Code Flow for Wallet-initiated and Issuer-initiated issuance, and Pre-Authorised Code Flow for Issuer-initiated issuance (See NOTES **CS01_02**, **CS01_03**, **CS01_04** and **CS01_05**)
* OpenID4VCI SD-JWT-VC credential format profile (See NOTE **CS01_01**)
* Sender-constrained tokens, for example, using Demonstration of Proof of Possession (DPoP) or mutual TLS
* PKCE with `S256` code challenge method for all authorisation requests (Authorisation Code Flow)
* Pushed Authorisation Requests (PAR) for all authorisation requests (Authorisation Code Flow; the Pre-Authorised Code Flow does not use the Authorisation Endpoint and therefore involves no authorisation request)
* Wallet Unit Attestation (WUA = WIA + KA), per ARF 2.9 [6] and TS-03 [5] and profiled in CS-04 [7]: the WIA is used for client authentication and session binding at the PAR and Token endpoints (Authorisation Code Flow) or at the Token endpoint (Pre-Authorised Code Flow), and the KA for key binding at the Credential Endpoint

Issuance can be:

* **Wallet-initiated**: the Holder starts from the WU and selects a credential type
* **Issuer-initiated**: the Issuer provides a **Credential Offer** that the WU consumes, using either the Authorisation Code grant or the Pre-Authorised Code grant

Both modes are required in this profile.

> [!NOTE]
> **CS01_01**: ISO18013-5 and ISO18013-7 will be supported in subsequent versions, based on use-case requirements.

> [!NOTE]
> **CS01_02**: HAIP [2] mandates only the Authorisation Code Flow. Support for the Pre-Authorised Code Flow is a WE BUILD extension profiled directly on OpenID4VCI [1], for Issuer-initiated use cases where the Issuer has authenticated the Holder and prepared the issuance before the Wallet interaction starts; it is therefore used for Issuer-initiated issuance only (section 7.1).

> [!NOTE]
> **CS01_03**: OpenID4VCI [1] makes the Transaction Code (`tx_code`) OPTIONAL at the protocol level, but section 13.6.1 states that Pre-Authorised Code replay "must be prevented using other means" and names the Transaction Code as the single mitigation the design facilitates for that purpose. The other controls available in this profile, namely short-lived single-use codes and WIA client authentication, restrict redemption to attested Wallet Units but do not bind the code to the intended Holder (NOTE **CS01_04**). This profile therefore REQUIRES a Transaction Code for every Credential Offer that uses the Pre-Authorised Code grant, delivered via a channel separate from the Credential Offer (sections 7.2 and 7.4).

> [!NOTE]
> **CS01_04**: The Pre-Authorised Code Flow provides no PKCE-like mechanism to protect the Pre-Authorised Code. Unlike the authorisation code, which is bound to the WU session via PKCE and to the DPoP key via `dpop_jkt` at PAR (section 7.3), the Pre-Authorised Code is not bound to a session or key, so anyone who obtains a valid code can attempt to redeem it (OpenID4VCI [1], section 13.6.1). The WIA client authentication required at the Token Endpoint (section 7.4) restricts redemption to attested Wallet Units but does not bind the code to the intended Holder: an attacker who obtains the code, for example by scanning a QR code over the Holder's shoulder, can redeem it in their own attested Wallet Unit. Pre-Authorised Codes are therefore short-lived and single-use (section 7.2), and a Transaction Code is REQUIRED to bind the code to the Holder (NOTE **CS01_03**).

> [!NOTE]
> **CS01_05**: OpenID4VCI [1] section 13.6.2 describes a Transaction Code phishing attack, in which an attacker operating a Credential Issuer site induces the Holder to enter into the Wallet a Transaction Code issued by an unrelated service, such as a payment service, and thereby obtains access to that service. OpenID4VCI RECOMMENDS that Wallets interact with trusted Credential Issuers only, and states that the Wallet MAY show the End-User the Credential Issuer endpoint before the Transaction Code is sent. Because this profile requires a Transaction Code for the Pre-Authorised Code grant (NOTE **CS01_03**), both mitigations are profiled as normative requirements in section 7.2.

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
 	* the requested credential format (SD-JWT-VC; see NOTE **CS01_01**)
  	* a `proof` object using the `JWT` proof type that binds the credential to the WU’s subject key

3. The Credential Issuer validates:
	* the access token and its sender-constraining mechanism
 	* the proof JWT
  	* issuance policy

5. The Issuer returns the issued SD-JWT-VC.


### 6.1.7 Storage

1. The WU validates the credential signature and Issuer binding.
2. The WU stores the credential under the Holder's control.


## 6.2 Issuer-initiated Issuance via Credential Offer

**Actors**: Holder, WU, Issuer (AS and Credential Issuer).

Issuer-initiated issuance always starts from a **Credential Offer**. The offer carries the `authorization_code` grant, the `urn:ietf:params:oauth:grant-type:pre-authorized_code` grant, or both (section 8.2). Sections 6.2.1 to 6.2.4 are common to both grants. The flows diverge only at the token step, 6.2.5 for the Authorisation Code grant and 6.2.6 for the Pre-Authorised Code grant, and converge again at 6.2.7.

Where the Pre-Authorised Code grant is used, the Issuer authenticates the Holder and prepares the issuance **before** the Wallet interaction starts. That grant does not use the Authorisation Endpoint or PAR: the WU exchanges the Pre-Authorised Code for an Access Token directly at the Token Endpoint (OpenID4VCI [1], Pre-Authorized Code Flow). Because there is no authorisation request, no PKCE-like mechanism protects the Pre-Authorised Code (see NOTE **CS01_04**).

### 6.2.1 Issuance decision

1. The Holder interacts with the Issuer through an Issuer-specific business process, for example, digital onboarding, customer due diligence or contract signing.
2. As part of this process, the Issuer authenticates the Holder and obtains the consent and data required for issuance. How this is done is out of scope of this specification.
3. Following successful internal checks, the Issuer decides to issue one or more credentials.

### 6.2.2 Credential Offer creation

1. The Issuer constructs a **Credential Offer object** (section 8.2) that includes:
   * the `credential_issuer` identifier
   * `credential_configuration_ids`: one or more identifiers, each matching a key in `credential_configurations_supported` in the Credential Issuer metadata (section 7.7)
   * a `grants` object carrying one or both of:
     * `authorization_code`, optionally with `issuer_state`
     * `urn:ietf:params:oauth:grant-type:pre-authorized_code`, containing a short-lived, single-use `pre-authorized_code` and a `tx_code` object (section 7.2)

2. Where the offer uses the Pre-Authorised Code grant, the Issuer generates the Transaction Code and delivers it to the Holder via a channel **separate** from the Credential Offer, for example, by text message or email (section 7.2, NOTE **CS01_03**).

### 6.2.3 Credential Offer delivery and Wallet invocation

1.	The Issuer delivers the offer to the Holder by one of:

	* displaying a QR code that encodes a URL which uses the `openid-credential-offer://` scheme to invoke the WU
   * sending a link that uses the `openid-credential-offer://` scheme to a device with a registered WU

2.	Both same-device and cross-device delivery methods MUST be supported.

### 6.2.4 WU processes the offer

1.	The WU is invoked via `openid-credential-offer://` and receives the Credential Offer.

2. The WU verifies that the `credential_issuer` value identifies a trusted Credential Issuer, and terminates processing otherwise (section 7.2, NOTE **CS01_05**).

3.	The WU parses the offer and determines:
   * Issuer base URL
   * the offered `credential_configuration_ids`
   * which grant type(s) the offer carries, and for the Pre-Authorised Code grant the `pre-authorized_code` and the `tx_code` requirements (`input_mode`, `length`, `description`)

4. The WU retrieves Issuer metadata and resolves each `credential_configuration_ids` value against `credential_configurations_supported`, obtaining the credential type and, for the Authorisation Code grant, the `scope` value to use in the authorisation request (section 7.7).

5. The WU displays the offer to the Holder and asks for confirmation to proceed.

### 6.2.5 Authorisation and token exchange (Authorisation Code grant)

1. The WU initiates the Authorisation Code Flow using PAR as defined in Section 6.1, using the `scope` values resolved in 6.2.4 and including `issuer_state` unchanged where the offer provided one.

2. The remainder of the flow, including authorisation, token request, credential request and storage, is identical to the Wallet-initiated flow.

### 6.2.6 Token request (Pre-Authorised Code grant)

1. The WU prompts the Holder to enter the Transaction Code received from the Issuer, rendering the input screen according to the `tx_code` object and displaying its `description` where present. Before submitting, the WU displays the Credential Issuer endpoint to which the Transaction Code will be sent (section 7.2, NOTE **CS01_05**).

2. The WU sends a token request directly to the Token Endpoint, without any prior Authorisation Endpoint or PAR interaction, including:
   * `grant_type=urn:ietf:params:oauth:grant-type:pre-authorized_code`
   * `pre-authorized_code` from the Credential Offer
   * `tx_code` entered by the Holder
   * client authentication using WUA

3. The Token Endpoint validates the Pre-Authorised Code and the Transaction Code, and returns:
   * sender-constrained `access_token`
   * optional `refresh_token` for credential refresh

### 6.2.7 Credential Request, validation and storage

The Wallet sends a Credential Request (or Batch Request) to the Credential Endpoint, including:

* `Authorization: Bearer {access_token}`
* SD‑JWT‑VC configuration
* `proof` object

Credential validation and storage are identical to the Wallet-initiated flow, Sections 6.1.6 and 6.1.7. Deferred issuance applies as described in Section 6.3.

## 6.3 Deferred Credential Request

Support for deferred issuance is OPTIONAL for Issuers (section 7.6). Where supported, deferred issuance applies to both wallet-initiated and issuer-initiated flows.

When the Credential Issuer cannot immediately produce one or more credentials:

1. The Issuer returns:
    * `transaction_id`
    * optional `interval` (retry hint) \

2. The WU MUST store the `transaction_id` associated with the pending credential(s). \

3. The WU periodically retries the Deferred Credential Endpoint with the `transaction_id` until:
    * the credential is successfully issued, or
    * the Issuer signals an unrecoverable error. \

4. Batch requests may contain a mix of immediate and deferred items. Each deferred item receives its own `transaction_id` and can be polled independently.

## 6.4 Re-issuance Flow

Re-issuance is the replacement of an attestation that already exists in a Wallet Unit by an attestation of the same attestation type, issued by the same Attestation Provider to the same Wallet Unit. Re-issuance keeps a valid technical attestation available throughout the administrative validity of the underlying attestation, is always initiated by the WU, and, to the maximum extent possible, requires no User authentication or interaction (ARF 2.9 [6], Annex 2, Topic 10, ISSU_42; Discussion Paper for Topic B [9]).

Support for re-issuance is OPTIONAL for Issuers. The Issuer requirements in this section and in sections 7.8 and 8.4 apply where the Issuer supports re-issuance (section 9).

**Actors**: Holder, WU, Issuer (AS and Credential Issuer).

### 6.4.1 Re-issuance triggers

Re-issuance can be triggered by:

* **Approaching end of technical validity**: the WU initiates re-issuance ahead of expiry, some time before the existing attestation expires (ARF 2.9 [6], ISSU_50).
* **Attribute value changes**: when the value of one or more attributes changes, the Issuer revokes the existing attestation and, where the User's contact details are known, notifies the User out of band with a request to obtain a re-issued attestation (ARF 2.9 [6], VCR_09).
* **Depletion of once-only or batch credentials**: the WU initiates re-issuance when the supply of single-use or batch-issued attestations is exhausted.
* **Manual re-issuance**: the User manually initiates re-issuance of an attestation from the WU (ARF 2.9 [6], ISSU_58).

### 6.4.2 Re-issuance using the Refresh Token grant

The primary re-issuance mechanism is the OpenID4VCI Refresh Token grant at the Token Endpoint, so that re-issuance requires no User authentication or interaction to the maximum extent possible.

1. During the original issuance, the Issuer returns a `refresh_token` alongside the `access_token` (section 6.1.5). The refresh token is sender-constrained (DPoP-bound) and bound to the WU that received the original attestation (section 7.8).
2. When a re-issuance trigger occurs, the WU sends a token request to the Token Endpoint, including:
   * `grant_type=refresh_token`
   * the `refresh_token` issued during the previous exchange
   * a DPoP proof using the key to which the refresh token is bound
   * client authentication using the WIA, as at the original Token Request (section 7.4)
4. The Token Endpoint validates the refresh token, the DPoP proof and the WIA, verifies that re-issuance is to the same WU as the existing attestation, and returns:
   * a new sender-constrained `access_token`
   * a rotated `refresh_token` for the next re-issuance
5. The WU sends a Credential Request to the Credential Endpoint as in section 6.1.6, using the new access token, and presenting a fresh Key Attestation where required, so that the Issuer can verify that the re-issued device-bound attestation is bound to the same WSCA/WSCD as the attestation it replaces (section 7.8).
6. The Issuer returns the re-issued attestation in the profiled credential format.
7. The WU validates and stores the re-issued attestation, compares its attribute values with those of the existing attestation and notifies the User of any differences, and deletes the replaced attestation after successful re-issuance (section 7.8).

Because no authorisation code is involved, no front-channel User interaction takes place in this flow.

### 6.4.3 Fallback to the full authorisation flow

Where no valid refresh token exists, or the Authorisation Server requires re-authentication (for example, after attribute value changes), the WU falls back to the full Authorisation Code Flow with PAR (section 6.1) or processes a new Credential Offer (section 6.2). The remainder of the flow, including authorisation, token request, credential request and storage, is identical to those flows.

> [!NOTE]
> CS01_02: Batch issuance and batch re-issuance per ARF 2.9 [6] and the Discussion Paper for Topic B [9] will be specified in a subsequent version of this document.

# 7. Normative Requirements

This section summarises the mandatory requirements for WE BUILD implementations.

## 7.1 Common requirements (WU and Issuer)

Both WU and Issuer **MUST**:

1. Support the Authorisation Code Flow for Wallet-initiated and Issuer-initiated credential issuance. Grant types other than `authorization_code` and `urn:ietf:params:oauth:grant-type:pre-authorized_code` MUST NOT be used for credential issuance.
2. Support the SD-JWT-VC credential format profile as defined for OpenID4VCI.
3. Support sender-constrained tokens, for example, using DPoP or mutual TLS.
4. Support PKCE with the `S256` code challenge method for all authorisation requests.
5. Use the WUA (WIA and KA) as defined in CS-04 [7]; CS-04 is authoritative for WUA structure, validity, revocation and binding, and this specification references it rather than restating those rules.

WUs **MUST** additionally:

1. Support the Pre-Authorised Code Flow (grant type `urn:ietf:params:oauth:grant-type:pre-authorized_code`) for Issuer-initiated issuance, since a Wallet Unit does not control which grant type an Issuer offers.

Issuers **MAY**:

1. Support the Pre-Authorised Code Flow for Issuer-initiated issuance where the use case calls for it (NOTE **CS01_02**). Issuers that do so MUST meet the additional requirements in sections 7.2, 7.4 and 7.7.

## 7.2 Credential Offer

Issuers **MUST**:

1. Support the grant type `authorization_code` in Credential Offers, aligned with OpenID4VCI.
2. Include `credential_configuration_ids` in every Credential Offer, each value matching a key in `credential_configurations_supported` in the Credential Issuer metadata (section 7.7). Credential Offers do not carry `scope` values in either grant type; the Wallet resolves the `scope` for the Authorisation Code Flow from Issuer metadata (OpenID4VCI [1], sections 4.1.1 and 5.1.2).
3. Support both same-device and cross-device sending of Credential Offers.
4. Support at least the `openid-credential-offer://` custom URL scheme for Wallet invocation.

Issuers that support the Pre-Authorised Code Flow (section 7.1) **MUST** additionally:

1. Support the grant type `urn:ietf:params:oauth:grant-type:pre-authorized_code` in Credential Offers, aligned with OpenID4VCI.
2. Ensure that each `pre-authorized_code` is short-lived and single-use.
3. Include a `tx_code` object in every Credential Offer that uses the `urn:ietf:params:oauth:grant-type:pre-authorized_code` grant type, as the replay mitigation required by OpenID4VCI [1] section 13.6.1 (NOTES **CS01_03** and **CS01_04**).
4. Deliver the Transaction Code to the Holder via a channel separate from the Credential Offer, for example, by text message or email (OpenID4VCI [1], section 4.1.1).

WUs **MUST**:

1. Be able to parse a Credential Offer that uses `authorization_code` as the grant type.
2. Resolve each `credential_configuration_ids` value against `credential_configurations_supported` in the Issuer metadata, and use the `scope` value from the resolved entry in the authorisation request.
3. Support invocation via the `openid-credential-offer://` custom URL scheme.
4. Be able to parse a Credential Offer that uses `urn:ietf:params:oauth:grant-type:pre-authorized_code` as the grant type, including the `tx_code` object and its `input_mode`, `length` and `description` parameters.
5. Where the Credential Offer contains a `tx_code` object (including an empty one), prompt the Holder for the Transaction Code, supporting both the `numeric` (default) and `text` input modes, and send the entered value in the `tx_code` parameter of the Token Request.
6. Where the `authorization_code` grant object in a Credential Offer contains an `issuer_state` value, include it unchanged as the `issuer_state` parameter of the subsequent authorisation request (OpenID4VCI [1], section 4.1.1).
7. Process Credential Offers only from Credential Issuers that the WU trusts, terminating processing where the `credential_issuer` value is not trusted (OpenID4VCI [1], section 13.6.2, NOTE **CS01_05**).

WUs **SHOULD**:

1. Display the Credential Issuer endpoint to which a Transaction Code will be sent, and ask the Holder for confirmation, before submitting the Token Request (OpenID4VCI [1], section 13.6.2, NOTE **CS01_05**).

## 7.3 Authorisation Endpoint and PAR

The requirements in this section apply to the Authorisation Code Flow only. The Pre-Authorised Code Flow does not use the Authorisation Endpoint or PAR; its Token Endpoint requirements are given in section 7.4.

Issuers **MUST**:

1. Require Pushed Authorisation Requests (PAR) for all authorisation requests. Direct front-channel authorisation requests without PAR MUST NOT be used.
2. Ensure that the Wallet authenticates at the PAR endpoint using the same method as used for client authentication at the Token Endpoint.
3. Verify the WIA presented at the PAR endpoint as at the Token Endpoint, including that its `x5c` signing certificate chains to a trust anchor on the Trusted List for Wallet Providers (see section 7.4; TS-03 [5], clause 2.2.1.1; CS-04 [7]).

WUs **MUST**:

1. Use PAR for all authorisation requests.
2. Use the `scope` parameter to indicate the credential type to be issued. Each `scope` value MUST map to a specific credential type that is known from Issuer metadata or from the Credential Offer.
3. Ensure that the `client_id` in the PAR request matches the `sub` claim in the WIA (Wallet Instance Attestation) JWT used for client authentication.
4. Include `dpop_jkt` (the JWK Thumbprint of the WIA `cnf` key) in the PAR request to bind the issued authorisation code to the DPoP key (RFC 9449 [8], Section 10), so that the sender-constraint holds from PAR through to the Access Token. TS-03 [5] mandates the `cnf.jkt` check at the Token Request (section 7.4); binding the code at PAR is the OpenID4VCI / RFC 9449 mechanism and is to be confirmed for this profile.

## 7.4 Token Endpoint and Wallet Attestation

WUs **MUST**:

1. Authenticate at the Token Endpoint using the WIA, a Wallet Attestation per OpenID4VCI [1] v1.0 Appendix E (`typ: oauth-client-attestation+jwt`), sent with its Proof-of-Possession (`oauth-client-attestation-pop+jwt`) in the PAR and Token Request. The WIA is profiled in CS-04 [7] (TS-03 [5], clause 2.2.1.1).
2. Convey the Wallet Provider signing certificate in the `x5c` JOSE header of the WIA, with intermediate certificates as needed. The Wallet Provider identity is inferred from this certificate; `iss` is not used (TS-03 [5], clause 2.2.1).
3. Use the WIA `cnf` key as the DPoP key when requesting the Access Token, and on receipt verify that the Access Token's `cnf.jkt` matches the JWK Thumbprint of that `cnf` key, aborting the issuance session on mismatch. This session binding is the obligation profiled in CS-04 [7], section 7.3 (TS-03 [5], clause 2.2.1.1).
4. Ensure the `sub` claim in the WIA equals the `client_id` used in PAR and Token Requests.

Issuers **MUST**:

1. Verify the WIA signature under the signing certificate in the `x5c` JOSE header, and verify that this certificate chains to a trust anchor on the Trusted List for Wallet Providers, using `x5c` intermediate certificates as needed (TS-03 [5], clause 2.2.1.1).
2. Verify the WIA Proof-of-Possession under the `cnf` key (TS-03 [5], clause 2.2.1.1).

Issuers **SHOULD**:

1. Support refresh tokens for credential refresh, following OpenID4VCI guidance on refresh usage and lifetime. Where re-issuance is supported, sender-constrained refresh tokens are REQUIRED and are specified normatively in section 7.8.

> [!NOTE]
> Because the WIA `cnf` key is used as the DPoP key (WUs item 3 above), for WUA-based issuance the Access Token is DPoP-bound (section 7.1).

In the Pre-Authorised Code Flow, WUs **MUST** additionally:

1. Authenticate at the Token Endpoint using the WIA and its Proof-of-Possession as specified in items 1 and 2 above; since this flow has no PAR step, both are sent with the Token Request only. OpenID4VCI [1] makes client authentication OPTIONAL for the `urn:ietf:params:oauth:grant-type:pre-authorized_code` grant type; this profile REQUIRES it.
2. Include the `pre-authorized_code` from the Credential Offer in the Token Request, together with the Transaction Code entered by the Holder in the `tx_code` parameter (section 7.2).
3. Use the WIA `cnf` key as the DPoP key when requesting the Access Token, as in item 3 above. Because this flow has no PAR step (and hence no `dpop_jkt` code binding, section 7.3), the DPoP binding is established at the Token Request.

In the Pre-Authorised Code Flow, Issuers **MUST** additionally:

1. Reject Token Requests that use the `urn:ietf:params:oauth:grant-type:pre-authorized_code` grant type without client authentication with a valid WIA. Anonymous access (`pre-authorized_grant_anonymous_access_supported`) MUST NOT be offered.
2. Verify that the `pre-authorized_code` was issued by their AS, has not expired and has not been used before, returning the `invalid_grant` error otherwise (OpenID4VCI [1], Token Error Response).
3. Verify the Transaction Code value presented in the `tx_code` parameter, returning `invalid_grant` if the value is wrong, and `invalid_request` if a Transaction Code is provided but not expected, or expected but not provided.
4. Limit the number of failed Transaction Code attempts for a given `pre-authorized_code` and invalidate that code once the limit is exceeded (OpenID4VCI [1], section 13.6.1).

In the Pre-Authorised Code Flow, Issuers **SHOULD**:

1. Issue Access Tokens that are valid only for the credential(s) indicated in the corresponding Credential Offer.
2. Treat Transaction Codes as short-lived and single-use.

## 7.5 Credential Endpoint

Issuers **MUST**:

1. Support the `JWT` proof type in the Credential Endpoint.
2. Support the SD-JWT-VC credential format and validate the proof binding between the Wallet subject and credential.
3. Where a Key Attestation (KA) is required, accept the KA in the `key_attestation` header of the `jwt` proof, verify the KA (its signature under the `x5c` signing certificate, chaining to a trust anchor on the Trusted List for Wallet Providers) and verify the proof of possession under the key at index 0 of `attested_keys` (TS-03 [5], clauses 2.2.2.1 and 2.2.2.2; CS-04 [7], section 7.3).
4. Where `key_attestations_required` is published, verify the KA's `key_storage` and `user_authentication` against the required levels and decide acceptability per issuance policy. The KA claims are defined in CS-04 [7] / TS-03 [5], clause 2.3.2.
5. Re-check the revocation status of the WIA and KA during the credential's validity period as specified in CS-04 [7], section 7.2 (TS-03 [5], clause 2.4.3).

Wallets **MUST**:

1. Send a proof JWT that contains claims required by the Issuer to bind the credential to the Wallet’s subject key.
2. Validate the returned SD-JWT-VC, including:
    * signature
    * Issuer identifier
    * key binding and any status information, according to the SD-JWT-VC profile
3. Where the Issuer requires a Key Attestation, include the KA in the `key_attestation` header of the `jwt` proof, signed by the key at index 0 of `attested_keys` (TS-03 [5], clause 2.2.2.1; CS-04 [7]).
4. Where the Issuer requires key-attestation levels, present a KA whose `key_storage` and `user_authentication` meet or exceed the required levels; a higher level satisfies the requirement, and a lower level MUST NOT be used.

## 7.6 Deferred Credential Endpoint

Issuers **MAY** support a `deferred_credential_endpoint`. Support for deferred issuance is OPTIONAL for Issuers, as in OpenID4VCI [1].

Issuers that support deferred issuance **MUST**:

* Return a `transaction_id` (as defined in OpenID4VCI v1.0 §8.3) when issuance is delayed.
* Validate `transaction_id` and ensure proper lifetime and binding to the issuance session.
* Publish endpoint in metadata.

Issuers that support deferred issuance **SHOULD**:

* Provide clear retry guidance via the `interval` parameter.
* Return explicit errors when the `transaction_id` is expired or the credential cannot be issued.

Wallets **MUST**:

* Recognise deferred responses and store the `transaction_id`.
* Call the Deferred Credential Endpoint with the `transaction_id` until the credential is ready or the transaction ends.
* Distinguish *pending* vs *failed* issuance in UI.

Wallets **SHOULD**:

* Apply poll intervals/back‑off.
* Allow users to stop polling.


## 7.7 Server Metadata

Issuers **MUST** publish metadata that includes:

1. OAuth 2.0 and OpenID configuration, including Authorisation, Token and PAR endpoints.
2. Credential Issuer metadata that describes:
    * all supported credential types, as entries in `credential_configurations_supported`
    * for each entry, the `scope` value that the Wallet uses in authorisation requests
3. `grant_types_supported` in the Authorisation Server metadata, listing `authorization_code` and, where the Issuer supports the Pre-Authorised Code Flow (section 7.1), `urn:ietf:params:oauth:grant-type:pre-authorized_code`; when this parameter is published it replaces the default values defined for OAuth Authorisation Server Metadata, so every supported grant type MUST be listed. The `pre-authorized_grant_anonymous_access_supported` parameter MUST NOT be set to `true`, since client authentication with the WIA is required (section 7.4).

Wallets **MUST**:

1. Retrieve and process Issuer metadata, including `credential_configurations_supported` and the `scope` value of each entry.
2. Resolve the `credential_configuration_ids` values of a Credential Offer against that metadata, and use the resolved `scope` values when constructing authorisation requests.

Issuers **MAY**:

1. Publish a `key_attestations_required` object in Credential Issuer metadata stating the minimum acceptable `key_storage` and `user_authentication` levels (ISO 18045 AVA_VAN), per OpenID4VCI [1] Appendix D. The KA claims are defined in CS-04 [7] / TS-03 [5], clause 2.3.2.

## 7.8 Re-issuance

Support for re-issuance is OPTIONAL for Issuers (section 6.4). The Issuer requirements in this section apply where the Issuer supports re-issuance.

Issuers that support re-issuance **MUST**:

1. Issue sender-constrained refresh tokens (DPoP-bound), and support the OpenID4VCI features that enable re-issuance of attestations (ARF 2.9 [6], ISSU_63; OpenID4VCI [1], section 14.5).
2. Verify that a re-issued device-bound attestation is bound to the same WSCA/WSCD as the attestation it replaces, using the DPoP-bound refresh token and, where required, a fresh Key Attestation, reusing the KA mechanism defined in section 7.5 and CS-04 [7] (ARF 2.9 [6], ISSU_65).
3. Define the refresh token lifetime and rotation relative to the administrative validity of the credential, and return explicit errors when re-issuance is refused.

WUs **MUST**:

1. Request re-issuance some time before the existing attestation expires (ARF 2.9 [6], ISSU_50).
2. Give the User the option to manually initiate re-issuance for any attestation, attempt to start the process immediately when the User does so, and notify the User if the request did not succeed (ARF 2.9 [6], ISSU_58).
3. Compare the attribute values of the re-issued attestation with those of the existing attestation and notify the User of any differences (ARF 2.9 [6], ISSU_59).
4. Handle re-issuance refusals gracefully, for example by retrying after an appropriate delay and applying back-off, consistent with section 7.6 (ARF 2.9 [6], ISSU_60).
5. Delete the replaced attestation after successful re-issuance and no longer present it (ARF 2.9 [6], ISSU_62).

**Wallet Unit Attestation.** On the `refresh_token` grant, the WU re-presents the WIA as client authentication at the Token Endpoint, in the same way as on the original Token Request (section 7.4), together with the DPoP proof for the key to which the refresh token is bound. Re-issuance of the WIA and KA themselves takes place without User action (ARF 2.9 [6], ISSU_42). Where the WUA has rotated, the WU presents the current valid WIA and, at the Credential Endpoint, a Key Attestation for the current keys, which the Issuer verifies as for first issuance. CS-04 [7] is authoritative for WUA structure, validity, revocation and binding, and this specification references it rather than restating those rules (section 7.1, item 6).

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
* `credential_configuration_ids`: non-empty array of strings, each matching a key in `credential_configurations_supported` in the Credential Issuer metadata (section 7.7)
* `grants`: object that includes `authorization_code`, `urn:ietf:params:oauth:grant-type:pre-authorized_code`, or both

When the `grants` object contains the `authorization_code` grant type, that grant object MAY contain:

* `issuer_state`: an opaque string created by the Issuer that binds the subsequent authorisation request to the context of this offer.
* `authorization_server`: identifies the Authorisation Server to use with this grant type. It MUST be used when the `authorization_servers` parameter in the Credential Issuer metadata has multiple entries, and MUST NOT be used otherwise.

When the `grants` object contains the `urn:ietf:params:oauth:grant-type:pre-authorized_code` grant type, that grant object MUST contain:

* `pre-authorized_code`: short-lived, single-use code to be sent in the subsequent Token Request
* `tx_code`: object indicating that a Transaction Code is required, REQUIRED by this profile as replay mitigation (sections 7.2 and 7.4, NOTES **CS01_03** and **CS01_04**), with the OPTIONAL parameters:
    * `input_mode`: `numeric` (default) or `text`
    * `length`: length of the Transaction Code
    * `description`: guidance for the Holder on how to obtain the Transaction Code (maximum 300 characters)

and MAY contain:

* `authorization_server`: as defined for the `authorization_code` grant object above.

> [!NOTE]
> Credential Offers do not carry `scope` values, in either grant type. The Wallet resolves the `scope` required for the Authorisation Code Flow by looking up each `credential_configuration_ids` value in `credential_configurations_supported` in the Credential Issuer metadata (OpenID4VCI [1], sections 4.1.1 and 5.1.2).

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
* `issuer_state`, when provided in the `authorization_code` grant object of a Credential Offer (section 8.2)

**Response**

* `request_uri`
* `expires_in`

All PAR requests MUST be client-authenticated according to Section 7.4.


## 8.4 Token Endpoint

* **Direction**: WU to Issuer (AS)
* **Method**: `POST`

**Request (logical fields — Authorisation Code grant)**

* `grant_type=authorization_code`
* `code`
* `redirect_uri`
* `code_verifier`
* client authentication using Wallet attestation JWT, for example, `client_assertion` and `client_assertion_type`

**Request (logical fields — Pre-Authorised Code grant)**

* `grant_type=urn:ietf:params:oauth:grant-type:pre-authorized_code`
* `pre-authorized_code`
* `tx_code`: the Transaction Code value entered by the Holder; present if and only if the Credential Offer contained a `tx_code` object (section 7.2)
* client authentication using Wallet attestation JWT, for example, `client_assertion` and `client_assertion_type`

**Response**

* `access_token` (sender-constrained)
* `token_type`
* `expires_in`
* optional `refresh_token`

**Refresh Token grant**

Where the Issuer supports re-issuance (section 6.4), the Token Endpoint also supports the `refresh_token` grant.

**Request (logical fields)**

* `grant_type=refresh_token`
* `refresh_token` issued during a previous token exchange
* DPoP proof for the key to which the refresh token is bound
* client authentication using the WIA, as for the `authorization_code` grant

**Response**

* `access_token` (sender-constrained)
* `token_type`
* `expires_in`
* `refresh_token` (rotated for the next re-issuance)

**Error Respond**

In line with the OpenID4VCI [1] Token Error Response, the AS returns:

* `invalid_grant` (for example, an expired, revoked or unknown refresh token), the WU MUST fall back to the full Authorisation Code Flow with PAR (section 6.1) or a new Credential Offer (section 6.2). The `pre-authorized_code` is invalid, expired or already used, or the Transaction Code value is wrong
* `invalid_request`: a Transaction Code was provided but not expected, or expected but not provided
* `invalid_client`: the Token Request lacks the client authentication required by this profile

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

## 8.6 Deferred Credential Endpoint

This endpoint is OPTIONAL for Issuers (section 7.6). Issuers that support deferred issuance provide it as follows.

**Direction:** WU → Issuer \
**Method:** POST
**Request (logical fields)**

* HTTP header:
    * `Authorization: Bearer {access_token}`
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

## 8.7 Metadata Endpoints

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
4. Implements the WU re-issuance requirements in sections 6.4 and 7.8.

An implementation **conforms to this specification as an Issuer** if it:

1. Implements the Issuer requirements in Sections 6 and 7.
2. Publishes server metadata, including type to `scope` mappings.
3. Provides the PAR, Token, Credential and WU invocation interfaces described in Section 8.
4. Where it supports re-issuance, implements the Issuer re-issuance requirements in sections 6.4 and 7.8, including the Refresh Token grant at the Token Endpoint (section 8.4). Support for re-issuance is OPTIONAL for Issuers (section 6.4).

Profiles may define additional constraints for specific WE BUILD credential types, such as PID, QEAA, or business credentials. Such profiles MUST NOT relax the mandatory requirements in this document. The specific issuance will be taken into a separate CS.

# References

[1]	OpenID Foundation (2025) OpenID for Verifiable Credential Issuance 1.0. OpenID Foundation. Available at: [https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) (Accessed: 24 November 2025).

[2]	OpenID Foundation (2025) OpenID4VC High Assurance Interoperability Profile 1.0 - Implementers Draft 1. OpenID Foundation. Available at: [https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-ID1.html](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-ID1.html)  (Accessed: 24 November 2025)

[3] IETF (2025) SD‑JWT‑based Verifiable Credentials. IETF. Available at: https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-09.html (Accessed: 24 November 2025).

[4]	WE BUILD (2025) Interoperability Test Bed - Reference Specification, 12 November, Available at: [https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md) (Accessed: 24 November 2025).

[5] European Commission (2026) Wallet Unit Attestation (TS3). eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications. Available at: [https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/blob/main/docs/technical-specifications/ts3-wallet-unit-attestation.md](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/blob/main/docs/technical-specifications/ts3-wallet-unit-attestation.md) (Accessed: 5 June 2026).

[6] European Commission (2026) The European Digital Identity Wallet Architecture and Reference Framework, version 2.9.0. Available at: [https://eudi.dev/2.9.0/architecture-and-reference-framework-main/](https://eudi.dev/2.9.0/architecture-and-reference-framework-main/) (Accessed: 5 June 2026).

[7] WE BUILD (2026) Conformance Specification CS-04: Individual Wallet Unit Attestation (WUA) Lifecycle. webuild-consortium/wp4-architecture.

[8] IETF (2023) RFC 9449: OAuth 2.0 Demonstrating Proof of Possession (DPoP). Available at: [https://www.rfc-editor.org/rfc/rfc9449](https://www.rfc-editor.org/rfc/rfc9449) (Accessed: 5 June 2026).

[9] European Digital Identity Cooperation Group (2025) The European Digital Identity Wallet Architecture and Reference Framework, Discussion Paper for Topic B: Re-issuance and batch issuance of PIDs and Attestations, version 0.9, 17 February. Available at: [https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/v2.9.0/docs/discussion-topics/b-re-issuance-and-batch-issuance-of-pids-and-attestations.md](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/v2.9.0/docs/discussion-topics/b-re-issuance-and-batch-issuance-of-pids-and-attestations.md) (Accessed: 10 July 2026).
