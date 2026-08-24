# WE BUILD - Pre-flight Conformance Specification: Credential Presentation and Issuance via the Digital Credentials API

Version 0.1 / Pre-flight Draft
Date: 4 July 2026

**Authors**: WP4 Architecture

* Leif Johansson <leifj@siros.org>

## Table Of Contents

- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language](#3-normative-language)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
- [6. High-level Flows](#6-high-level-flows)
  - [6.1 Same-device Presentation via DC API](#61-same-device-presentation-via-dc-api)
  - [6.2 Cross-device Presentation via DC API Hybrid Transport](#62-cross-device-presentation-via-dc-api-hybrid-transport)
  - [6.3 Credential Issuance via DC API](#63-credential-issuance-via-dc-api)
- [7. Normative Requirements](#7-normative-requirements)
  - [7.1 Wallet Unit Requirements](#71-wallet-unit-requirements)
  - [7.2 Verifier Requirements](#72-verifier-requirements)
  - [7.3 Issuer Requirements](#73-issuer-requirements)
- [8. Platform and Browser Support Considerations (Informative)](#8-platform-and-browser-support-considerations-informative)
  - [8.1 Browser Extension Polyfill (Wallet-side)](#81-browser-extension-polyfill-wallet-side)
  - [8.2 Verifier-side Polyfill](#82-verifier-side-polyfill)
- [9. Conformance](#9-conformance)
- [References](#references)

# 1. Introduction

This document is a **pre-flight conformance specification** as defined in the [Pre-flight CS ADR](../adr/pre-flight-CS.md). It is intended to enable early testing of credential presentation and issuance using the W3C Digital Credentials API (DC API) [1] within the WE BUILD ecosystem. The goal is to gather implementation experience and testing feedback that will inform a future full conformance specification.

The Digital Credentials API provides a browser-native mechanism for verifiers to request credential presentations from wallet units and for issuers to initiate credential issuance to wallet units. For same-device flows, this removes the need for custom protocol schemes (such as `openid4vp://`). For cross-device flows, the DC API leverages CTAP2 hybrid transport to connect the verifier's browser to a remote wallet, with the browser mediating the entire interaction. Both modes integrate credential exchange into the browser's security model.

This specification complements **CS-002 (Credential Presentation)** [2] and **CS-001 (Credential Issuance)** by defining how the same OpenID4VP and OpenID4VCI protocols operate when the browser's DC API serves as the invocation and transport layer, rather than custom URL schemes or redirect flows.

# 2. Scope

This specification defines the conformance expectations for credential presentation and issuance using the Digital Credentials API:

* **In scope:**
  * Same-device web presentation flows using `navigator.credentials.get()` with the `digital` credential type
  * Same-device web issuance flows using `navigator.credentials.create()` with the `digital` credential type
  * Cross-device presentation flows using DC API hybrid transport (CTAP2 / BLE + tunnel)
  * Integration of OpenID4VP request/response with the DC API transport
  * Integration of OID4VCI credential offers with the DC API transport
  * Verifier-side and issuer-side JavaScript API usage
  * Wallet unit registration and response handling via the DC API
  * Limitations of web-based wallet units and known mitigations

* **Out of scope:**
  * Cross-device presentation flows via QR code scanning without browser mediation (covered by CS-002 §6.2)
  * Proximity-based presentation (e.g. ISO 18013-5 / BLE)
  * Detailed trust evaluation and trust list resolution (covered by other WE BUILD specifications)

# 3. Normative Language

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

> **Note:** As a pre-flight specification, the normative requirements herein are preliminary and subject to revision based on testing feedback.

# 4. Roles and Components

| Role | Description |
|------|-------------|
| **Wallet Unit (WU)** | A native application or web application acting on behalf of the Holder, registered with the platform as a digital credential provider. |
| **Holder** | The person controlling the Wallet Unit. |
| **Verifier (Relying Party)** | A web application that requests credential presentations via the DC API. |
| **Issuer** | A web application that initiates credential issuance to a wallet unit via the DC API. |
| **User Agent (Browser)** | The browser mediating the DC API interaction between the Verifier/Issuer and the Wallet Unit. |

# 5. Protocol Overview

The Digital Credentials API [1] extends the W3C Credential Management API [3] to support digital identity credentials. A verifier calls `navigator.credentials.get()` with a `digital` options object containing an OpenID4VP presentation request. An issuer calls `navigator.credentials.create()` with a `digital` options object containing an OID4VCI credential offer. In both cases, the browser mediates the interaction:

1. The verifier constructs an OpenID4VP request object and passes it to the DC API.
2. The browser identifies registered wallet units capable of fulfilling the request.
3. The browser presents a wallet selection UI to the user (if multiple wallets are available).
4. The selected wallet unit receives the request, processes it, obtains holder consent, and returns the presentation response.
5. The browser delivers the response back to the verifier's JavaScript context.

This flow keeps the OpenID4VP request/response semantics from CS-002 intact while replacing the invocation and transport mechanism with the browser-native DC API.

The key specification governing this interaction is the **W3C Digital Credentials API** [1], which at the time of writing is a Working Draft. Browser support is available in Chrome 141+ on Android, macOS, and desktop platforms, and is progressing in other browsers. Cross-device support via hybrid transport is at an earlier stage (see §6.2 and [6]).

# 6. High-level Flows

## 6.1 Same-device Presentation via DC API

This flow describes how a verifier web application requests a credential presentation from a wallet unit using the Digital Credentials API.

### 6.1.1 Verifier Constructs Presentation Request

The verifier constructs an OpenID4VP authorization request as specified in CS-002 §6.1.1. The request is encoded as a JSON object suitable for the DC API.

### 6.1.2 DC API Invocation

The verifier invokes the DC API:

```javascript
const credential = await navigator.credentials.get({
  digital: {
    requests: [{
      protocol: "openid4vp-v1-signed",
      data: {
        request: signedOpenid4vpRequest  // JWS Compact Serialization
      }
    }]
  }
});
```

The `protocol` field MUST be set to `"openid4vp-v1-signed"` (see §7.2 VP-DC-02). The `data` field MUST be a JSON object whose `request` member contains the signed OpenID4VP authorization request in JWS Compact Serialization ([4] §A.3.2.1). The verifier MUST set `response_type` to `vp_token` and `response_mode` to `dc_api.jwt` in the signed request object to ensure encrypted responses (see §7.2 VP-DC-07). The verifier MUST include `expected_origins` in the signed request (see §7.2 VP-DC-08).

### 6.1.3 Browser Mediation

The browser:
1. Identifies installed wallet units registered for the `"openid4vp-v1-signed"` protocol.
2. Presents a selection UI to the user if multiple wallets are available.
3. Forwards the request to the selected wallet unit.

### 6.1.4 Wallet Processing and Holder Consent

The wallet unit:
1. Parses and validates the OpenID4VP request as specified in CS-002 §6.1.3.
2. Identifies matching credentials.
3. Presents a consent screen to the holder, showing the requested attributes and the verifier's identity.
4. Upon consent, generates the verifiable presentation with selective disclosure as appropriate.

### 6.1.5 Response Delivery

The wallet unit returns the OpenID4VP response via the DC API. The browser delivers the response to the verifier's JavaScript context as the resolved value of the `navigator.credentials.get()` promise. The response is a `DigitalCredential` object whose `data` attribute contains the OpenID4VP response and whose `protocol` attribute confirms the protocol used.

### 6.1.6 Verifier Validation

The verifier validates the presentation response as specified in CS-002 §6.1.7, including:
- Signature verification
- Credential status checks
- Trust chain validation

## 6.2 Cross-device Presentation via DC API Hybrid Transport

The DC API supports cross-device presentation using CTAP2 hybrid transport [6]. This is architecturally distinct from the QR-based cross-device flow in CS-002 §6.2: the browser on the verifier's device mediates the entire interaction rather than the wallet connecting directly to the verifier's backend.

### 6.2.1 Verifier Constructs Presentation Request

The verifier constructs the OpenID4VP authorization request identically to §6.1.1. No changes to the request format are required for cross-device operation.

### 6.2.2 DC API Invocation with Hybrid Transport

The verifier invokes the DC API as in §6.1.2. The browser determines that no local wallet is available (or that the user selects a remote device) and initiates hybrid transport:

1. The browser displays a QR code or uses BLE advertisement to establish a CTAP2 hybrid connection to the holder's remote device.
2. The holder scans the QR code or accepts the BLE pairing on their mobile device.
3. A secure tunnel is established between the verifier's browser and the remote wallet unit.

### 6.2.3 Remote Wallet Processing

The remote wallet unit:
1. Receives the OpenID4VP request via the hybrid transport tunnel.
2. Validates and processes the request as specified in §6.1.4.
3. Returns the OpenID4VP response through the same tunnel.

### 6.2.4 Response Delivery

The browser receives the response via the hybrid tunnel and delivers it to the verifier's JavaScript context as the resolved value of `navigator.credentials.get()`. From the verifier's perspective, the response is indistinguishable from a same-device response.

### 6.2.5 Verifier Validation

The verifier validates the response identically to §6.1.6.

> **Note:** Cross-device DC API support via hybrid transport is at an early stage of browser implementation. Implementers SHOULD track [6] for current platform availability and be prepared for the hybrid path to be unavailable on some browser/OS combinations.

## 6.3 Credential Issuance via DC API

The DC API supports credential issuance through `navigator.credentials.create()` [1] §7.4–7.6. The issuer's web page initiates the flow; the browser mediates wallet selection; the wallet then completes the OID4VCI exchange directly with the issuer's endpoints.

### 6.3.1 Issuer Constructs Credential Offer

The issuer constructs an OID4VCI credential offer as specified in CS-001. The offer is encoded as a JSON object suitable for the DC API.

### 6.3.2 DC API Invocation

The issuer invokes the DC API:

```javascript
const result = await navigator.credentials.create({
  digital: {
    requests: [{
      protocol: "openid4vci-v1",
      data: credentialOffer
    }]
  }
});
```

The `protocol` field MUST be set to `"openid4vci-v1"`. The `data` field contains the OID4VCI credential offer object.

### 6.3.3 Browser Mediation

The browser:
1. Identifies installed wallet units registered for the `"openid4vci-v1"` protocol.
2. Presents a wallet selection UI to the user.
3. Forwards the credential offer to the selected wallet unit.

### 6.3.4 Wallet Processing

The wallet unit:
1. Receives the credential offer via the DC API.
2. Initiates the standard OID4VCI flow with the issuer's endpoints (authorization, token, credential).
3. Stores the issued credential.
4. Returns a confirmation response via the DC API.

The DC API's role ends once the offer is delivered to the wallet. The remainder of the OID4VCI flow (authorization, token exchange, credential retrieval) proceeds as specified in CS-001, independent of the DC API.

### 6.3.5 Response Delivery

The wallet unit returns a response via the DC API. The browser delivers it to the issuer's JavaScript context as the resolved value of `navigator.credentials.create()`.

> **Note:** The `"openid4vci-v1"` protocol identifier is defined in the W3C DC API spec (§5, §7.8.3) but is at an earlier stage of adoption than the presentation protocols. Implementers SHOULD track [6] for current browser support.

# 7. Normative Requirements

## 7.1 Wallet Unit Requirements

| ID | Requirement | Reference |
|----|-------------|-----------|
| WU-DC-01 | The WU MUST register itself with the platform as a digital credential provider for the `"openid4vp-v1-signed"` protocol. | [1] §7.8.2 |
| WU-DC-02 | The WU MUST accept OpenID4VP authorization requests received via the DC API. | [1], [4] |
| WU-DC-03 | The WU MUST return OpenID4VP authorization responses via the DC API response mechanism. | [1], [4] |
| WU-DC-04 | The WU MUST support the same credential formats and selective disclosure mechanisms as required by CS-002 §7.1. | [2] |
| WU-DC-05 | The WU SHOULD support both DC API and `openid4vp://` invocation to ensure backward compatibility. | [2], [4] |
| WU-DC-06 | The WU SHOULD support receiving DC API requests via CTAP2 hybrid transport to enable cross-device flows. | [1], [6] |
| WU-DC-07 | The WU SHOULD register as a credential provider for the `"openid4vci-v1"` protocol to support issuance via the DC API. | [1] §7.8.3 |
| WU-DC-08 | The WU MUST, upon receiving a credential offer via the DC API, initiate the standard OID4VCI flow with the issuer's endpoints as specified in CS-001. | [7] |
| WU-DC-09 | The WU MUST validate that the requesting origin matches one of the values in `expected_origins` from the signed authorization request before processing the request. | [4] §A.2 |

## 7.2 Verifier Requirements

| ID | Requirement | Reference |
|----|-------------|-----------|
| VP-DC-01 | The Verifier MUST use `navigator.credentials.get()` with the `digital` options member when the DC API is available. | [1] §7.1 |
| VP-DC-02 | The Verifier MUST set the `protocol` field to `"openid4vp-v1-signed"` in the DC API request to ensure signed authorization requests with verifier authentication. | [1] §7.8.2, [4] §A.3.2 |
| VP-DC-03 | The Verifier MUST construct a valid OpenID4VP authorization request as specified in CS-002 §7.2. | [2], [4] |
| VP-DC-04 | The Verifier SHOULD implement fallback to `openid4vp://` custom URL scheme or cross-device flow when the DC API is not available. | [2] |
| VP-DC-05 | The Verifier MUST call the DC API from a [secure context](https://w3c.github.io/webappsec-secure-contexts/) and in response to a user activation event. | [1] §8.1 |
| VP-DC-06 | The Verifier SHOULD support cross-device presentation via the DC API hybrid transport path where the browser provides it. | [1], [6] |
| VP-DC-07 | The Verifier MUST set `response_type` to `vp_token` and `response_mode` to `dc_api.jwt` in the OpenID4VP authorization request. | [4] §A.2, [4] §8.3 |
| VP-DC-08 | The Verifier MUST include `expected_origins` in signed requests sent via the DC API. | [4] §A.2 |

## 7.3 Issuer Requirements

| ID | Requirement | Reference |
|----|-------------|----------|
| IS-DC-01 | The Issuer MUST use `navigator.credentials.create()` with the `digital` options member to initiate credential issuance when the DC API is available. | [1] §7.4 |
| IS-DC-02 | The Issuer MUST set the `protocol` field to `"openid4vci-v1"` in the DC API issuance request. | [1] §7.8.3 |
| IS-DC-03 | The Issuer MUST construct a valid OID4VCI credential offer as specified in CS-001. | [7] |
| IS-DC-04 | The Issuer MUST call the DC API from a [secure context](https://w3c.github.io/webappsec-secure-contexts/) and in response to a user activation event. | [1] §8.3 |
| IS-DC-05 | The Issuer SHOULD implement fallback to direct OID4VCI credential offer delivery (e.g. via QR code or deep link) when the DC API is not available. | [7] |

# 8. Platform and Browser Support Considerations (Informative)

> **Note:** This section is informative and provides implementation guidance for the testing phase. It does not contain normative requirements.

The DC API is not yet universally supported across browsers and platforms. At the time of writing, presentation support is available in Chrome 141+ on Android, macOS, and desktop platforms, with other browsers at various stages of development [6]. Verifiers and wallet providers MUST plan for environments where the DC API is absent or where the `"openid4vp-v1-signed"` protocol is not natively supported.

Verifiers SHOULD use `DigitalCredential.userAgentAllowsProtocol("openid4vp-v1-signed")` to detect protocol support before attempting a DC API call [1] §7.7.3.

Two complementary polyfill strategies exist to bridge these gaps. They address different sides of the interaction and MAY be deployed independently or together.

## 8.1 Browser Extension Polyfill (Wallet-side)

The DC API requires wallet units to register as credential providers at the OS or browser level. Web-based wallet units — running as ordinary web applications or PWAs — cannot do this because the registration path requires native platform integration (e.g. Android CredentialManager, iOS AuthenticationServices).

A **browser extension** can act as a polyfill on the wallet side by:

1. Registering itself as a credential provider proxy with the browser.
2. Intercepting DC API requests issued by verifiers via `navigator.credentials.get()`.
3. Routing the OpenID4VP request to a web-based wallet that has registered with the extension.
4. Returning the wallet's OpenID4VP response back through the DC API to the verifier.

This approach is transparent to verifiers: they use the standard DC API and are unaware that the response originates from a web wallet via the extension rather than a native wallet. The trade-off is that the user must install the extension.

This pattern enables web wallets to participate in DC API flows on platforms where native wallet registration is not possible.

## 8.2 Verifier-side Polyfill

When the DC API is not available in the browser at all — because the browser does not implement it, or because no wallet (native or extension-based) supports the `"openid4vp"` protocol — the verifier must fall back to invoking OpenID4VP directly, as specified in CS-002.

A **verifier-side polyfill** (implemented as a JavaScript library or WebAssembly module) can bridge this gap by:

1. Detecting whether the DC API is available (via `typeof DigitalCredential !== "undefined"`) and whether the `"openid4vp-v1-signed"` protocol is allowed (via `DigitalCredential.userAgentAllowsProtocol("openid4vp-v1-signed")`).
2. If the DC API is available and the protocol is allowed, using it as the primary invocation path (this specification).
3. If the DC API is unavailable or the request fails with a `NotSupportedError`, falling back to:
   - **Same-device flow:** Redirecting to an `openid4vp://` custom URL scheme with the authorization request (CS-002 §6.1).
   - **Cross-device flow:** Displaying a QR code encoding the OpenID4VP request URI for scanning by a mobile wallet (CS-002 §6.2).

This approach is transparent to the wallet: it receives a standard OpenID4VP request regardless of whether the verifier used the DC API or a direct invocation. The trade-off is that the verifier takes on responsibility for wallet invocation, transport, and response handling that the DC API would otherwise mediate.

Verifier-side polyfill libraries SHOULD present a unified API to the verifier application, abstracting the detection and fallback logic so that application code does not need to manage multiple invocation paths directly.

# 9. Conformance

A **Verifier** conforms to this specification if it satisfies all requirements in §7.2.

An **Issuer** conforms to this specification if it satisfies all requirements in §7.3.

A **Wallet Unit** conforms to this specification if it satisfies all requirements in §7.1.

Conformance testing for this pre-flight specification will be defined as part of the feedback process described in the [Pre-flight CS ADR](../adr/pre-flight-CS.md). Implementers are encouraged to report their testing experience to inform the development of a full conformance specification.

# References

| # | Reference |
|---|-----------|
| [1] | W3C, "Digital Credentials API", W3C Working Draft, 15 July 2026, https://www.w3.org/TR/2026/WD-digital-credentials-20260715/ |
| [2] | WE BUILD, "Conformance Specification: Credential Presentation v1.1 (CS-002)", 2026 |
| [3] | W3C, "Credential Management Level 1", W3C Recommendation, https://www.w3.org/TR/credential-management-1/ |
| [4] | OpenID Foundation, "OpenID for Verifiable Presentations (OpenID4VP) 1.0", https://openid.net/specs/openid-4-verifiable-presentations-1_0.html (DC API profile: Appendix A) |
| [5] | W3C Web Identity & Credentials Adoption CG, "Digital Credentials API Ecosystem Support", https://digitalcredentials.dev/ecosystem-support |
| [6] | FIDO Alliance, "Client to Authenticator Protocol (CTAP) 2.2 — Hybrid Transport", https://fidoalliance.org/specs/fido-v2.2-rd-20230321/fido-client-to-authenticator-protocol-v2.2-rd-20230321.html#hybrid-transport |
| [7] | OpenID Foundation, "OpenID for Verifiable Credential Issuance (OID4VCI) 1.0", https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html |
