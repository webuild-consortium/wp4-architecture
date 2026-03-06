# WE BUILD - Conformance Specification: Remote Qualified Signing with Wallet Units

Version 1.0-draft
Date: 05 March 2026

**Table of Contents**
- [WE BUILD - Conformance Specification: Remote Qualified Signing with Wallet Units](#we-build---conformance-specification-remote-qualified-signing-with-wallet-units)
- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language](#3-normative-language)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
- [6. High-level Flows](#6-high-level-flows)
  - [6.1 Same-device Signing Flow](#61-same-device-signing-flow)
    - [6.1.1 Signature Request Creation](#611-signature-request-creation)
    - [6.1.2 WU Invocation](#612-wu-invocation)
    - [6.1.3 WU Validation](#613-wu-validation)
    - [6.1.4 Signer Consent](#614-signer-consent)
    - [6.1.5 Signature Generation](#615-signature-generation)
    - [6.1.6 Presentation Submission](#616-presentation-submission)
    - [6.1.7 Result Handling](#617-result-handling)
  - [6.2 Cross-device Signing Flow](#62-cross-device-signing-flow)
- [7. Normative Requirements](#7-normative-requirements)
  - [7.1 Wallet Unit Requirements](#71-wallet-unit-requirements)
  - [7.2 Relying Party Requirements](#72-relying-party-requirements)
- [8. Interface Definitions](#8-interface-definitions)
  - [8.1 Signing Request Object Interface](#81-signing-request-object-interface)
  - [8.2 Presentation Endpoint](#82-presentation-endpoint)
  - [8.3 Relying Party Metadata Interface](#83-relying-party-metadata-interface)
- [9. Conformance](#9-conformance)
- [References](#references)

# 1. Introduction

This document defines the **WE BUILD Conformance Specification: Remote Qualified Signing with Wallet Units**, describing how Wallet Units (WU) and Relying Parties interoperate to create qualified electronic signatures using OpenID for Verifiable Presentations (OpenID4VP) 1.0 [1] and the CSC Data Model Bindings [3].

This specification extends the WE BUILD Conformance Specification: Credential Presentation [5] (hereafter CS-02). All requirements defined in CS-02 apply unless explicitly superseded here. This document defines only the signing-specific additions.

It covers:

- Signing request and response flows using the CSC `qesRequest` transaction data type
- Support for the CSC X.509 credential format
- Signer consent requirements specific to qualified electronic signatures
- Inline and out-of-band signed document delivery

> **NOTE_CSRS_01** The `qesApproval` flow (provider-centric model using mdoc or SD-JWT VC approval credentials) is out of scope for this version and will be addressed in a subsequent version. For provider-centric remote signing with long-term certificates, see EWC RFC-010 [6].

# 2. Scope

This specification defines the conformance profile for remote qualified electronic signature creation. It applies in addition to CS-02 [5].

Requirements are defined for:

- Wallet Units that respond to signing requests
- Relying Parties that initiate signing requests

Mandatory features beyond CS-02:

- CSC `qesRequest` transaction data type [3]
- CSC X.509 credential format (`https://cloudsignatureconsortium.org/2025/x509`)
- Signer consent rendering requirements
- AdES signature generation
- Inline and out-of-band (`responseURI`) response delivery

Out of scope:

- All requirements already covered by CS-02 [5]
- CSC API endpoints (`signatures/signDoc`, `signatures/signHash`)
- The qesApproval flow (see NOTE_CSRS_01)

# 3. Normative Language

As defined in CS-02 [5] Section 3.

# 4. Roles and Components

This specification uses the roles defined in CS-02 [5] Section 4, with the following substitutions and additions:

- **Holder** is referred to as **Signer** in this specification.
- **Verifier** is referred to as **Relying Party (RP)** in this specification.
- The Wallet Unit acts as both credential holder and signing application in the wallet-centric model covered by this specification.

# 5. Protocol Overview

This specification applies the protocol baseline defined in CS-02 [5] Section 5 without modification, with the following signing-specific additions:

- The DCQL query MUST use the CSC X.509 credential format: `https://cloudsignatureconsortium.org/2025/x509`
- The Authorisation Request MUST include `transaction_data` containing a base64url-encoded `qesRequest` object as defined in CSC-DMB [3] Section 6.2.1
- `signatureQualifier` MUST always be present in the `qesRequest`
- Document integrity MUST be verified by the WU when both `href` and `checksum` are present

High-level steps:

1. Relying Party creates a Signing Request containing `qesRequest` transaction data
2. WU is invoked via `openid4vp://` (same-device) or QR code (cross-device)
3. WU validates the Signing Request
4. Signer reviews documents and consents
5. WU generates AdES signature(s)
6. WU submits the Presentation Response containing the signed document(s)
7. Relying Party validates and returns the outcome

> **NOTE_CSRS_02** ISO18013-5 and ISO18013-7 credential formats will be considered in subsequent versions based on use case requirements.

# 6. High-level Flows

## 6.1 Same-device Signing Flow

### 6.1.1 Signature Request Creation

The Relying Party prepares a signed Presentation Request Object as defined in CS-02 [5] Section 6.1.1, with the following additional requirements:

- The DCQL query MUST contain a credential entry with `format: "https://cloudsignatureconsortium.org/2025/x509"` and optionally `certificatePolicies` or `certificateFingerprints` in the `meta` field
- `transaction_data` MUST contain a base64url-encoded `qesRequest` specifying `type`, `credential_ids`, `signatureQualifier`, and at least one `signatureRequests` entry

### 6.1.2 WU Invocation

As defined in CS-02 [5] Section 6.1.2.

### 6.1.3 WU Validation

As defined in CS-02 [5] Section 6.1.3, with the following additional checks:

- `transaction_data` MUST decode to a valid `qesRequest`
- `signatureQualifier` MUST be present and recognised
- The available credential MUST be capable of producing a QES with the specified `signatureQualifier`; if not, the WU MUST abort
- If both `href` and `checksum` are present in a `signatureRequest`, the WU MUST verify document integrity; if verification fails, the WU MUST abort

### 6.1.4 Signer Consent

In addition to the consent requirements of CS-02 [5] Section 6.1.4, the WU MUST display:

- A clear indication that the transaction creates a qualified electronic signature or seal
- The trust framework identified by `signatureQualifier`
- The label of each document, or a clear indication that no label is provided
- Whether document integrity has been automatically verified
- The URI to which the signed response will be sent, if `responseURI` is specified

### 6.1.5 Signature Generation

Upon consent, the WU MUST generate AdES signature(s) per the `signature_format` and `conformance_level` specified in each `signatureRequest`.

### 6.1.6 Presentation Submission

As defined in CS-02 [5] Section 6.1.6, with the following additions:

The `vp_token` MUST include a `qes` object containing either:

- `documentWithSignature`: base64-encoded signed document(s), for enveloped formats (e.g. PAdES)
- `signatureObject`: base64-encoded detached signature(s)

If `responseURI` is specified in the `qesRequest`, the WU MUST HTTP POST the `qesResponse` to that URI as defined in Section 8.2, and MUST return an empty credential response in the `vp_token`.

### 6.1.7 Result Handling

As defined in CS-02 [5] Section 6.1.7.

## 6.2 Cross-device Signing Flow

The cross-device signing flow follows CS-02 [5] Section 6.2 in its entirety, applying the signing-specific additions defined in Sections 6.1.1 through 6.1.7 of this specification at each corresponding step.

# 7. Normative Requirements

## 7.1 Wallet Unit Requirements

In addition to all requirements in CS-02 [5] Section 7.1, Wallet Units MUST:

1. Support the CSC X.509 credential format (`https://cloudsignatureconsortium.org/2025/x509`).
2. Process `qesRequest` transaction data as defined in CSC-DMB [3] Section 6.2.1.
3. Verify document integrity against `checksum` when both `href` and `checksum` are present.
4. Support `data:` URIs with base64 encoding in `href`.
5. Display the signing-specific consent information defined in Section 6.1.4.
6. Generate AdES signatures per the specified `signature_format` and `conformance_level`.
7. Support inline response delivery via `documentWithSignature` or `signatureObject`.
8. Support out-of-band response delivery via `responseURI`.

Wallet Units MUST NOT:

- Proceed if document integrity verification fails.
- Proceed if the credential cannot satisfy the specified `signatureQualifier`.

## 7.2 Relying Party Requirements

In addition to all requirements in CS-02 [5] Section 7.2, Relying Parties MUST:

1. Include `transaction_data` with a valid `qesRequest` in every signing request.
2. Include `signatureQualifier` in every `qesRequest`.
3. Use the CSC X.509 credential format in the DCQL query.
4. Provide a valid access method (`public` or `OTP`) for all `href` document references.
5. If using `responseURI`: implement an HTTPS endpoint accepting HTTP POST as defined in Section 8.2.

Relying Parties MUST NOT:

- Omit `signatureQualifier` from `qesRequest` objects.

# 8. Interface Definitions

Interfaces in this specification follow the structure defined in CS-02 [5] Section 8. The Wallet Invocation Interface defined in CS-02 [5] Section 8.1 applies without modification.

## 8.1 Signing Request Object Interface

The Presentation Request Object MUST satisfy CS-02 [5] Section 8.2, with the following additions.

The DCQL query MUST include a credential entry of the following form:

```json
{
  "id": "signing-cert-01",
  "format": "https://cloudsignatureconsortium.org/2025/x509",
  "meta": {
    "certificatePolicies": ["0.4.0.2042.1"]
  }
}
```

The `transaction_data` array MUST contain the following object, base64url-encoded:

```json
{
  "type": "https://cloudsignatureconsortium.org/2025/qes",
  "credential_ids": ["signing-cert-01"],
  "signatureQualifier": "eu_eidas_qes",
  "signatureRequests": [
    {
      "label": "Example Contract",
      "access": { "type": "public" },
      "href": "https://rp.example.org/documents/contract.pdf",
      "checksum": "sha256-HZQzZmMAIWekfGH0/ZKW1nsdt0xg3H6bZYztgsMTLw0=",
      "signature_format": "P",
      "conformance_level": "AdES-B-B",
      "signed_envelope_property": "Certification"
    }
  ]
}
```
> **NOTE_CSRS_03** In this profile, the base64url-decoded `transaction_data` value is the CSC `qesRequest` object with `type` `https://cloudsignatureconsortium.org/2025/qes`.
> The `credential_ids` values refer to the `id` of the associated DCQL credential query, and not to CSC API `credentialID` values.
> For interoperability with Wallet Units that validate `transaction_data` strictly, Relying Parties should not include additional profile-specific members unless this specification defines them.

## 8.2 Presentation Endpoint

The Presentation Endpoint defined in CS-02 [5] Section 8.3 applies. The request body MUST use the following structure for inline signing responses:

```json
{
  "signing-cert-01": {
    "qes": {
      "documentWithSignature": ["<base64-encoded signed document>"]
    }
  }
}
```

When `responseURI` is specified, the WU MUST HTTP POST the `qesResponse` to that URI. The following requirements apply:

- `responseURI` MUST use the `https` scheme.
- The WU MUST verify that the `responseURI` host matches the Relying Party's `client_id` or a domain listed in the RP's verified metadata.
- If the HTTP POST to `responseURI` fails (network error or non-2xx response), the WU MUST abort the signing flow and report an error to the Signer.

```
POST <responseURI path> HTTP/1.1
Host: <responseURI host>
Content-Type: application/json

{ "documentWithSignature": ["<base64-encoded signed document>"] }
```

The `responseURI` endpoint MUST return `HTTP 200 OK` on successful receipt. The `vp_token` returned to the Presentation Endpoint MUST be empty:

```json
{ "signing-cert-01": {} }
```

## 8.3 Relying Party Metadata Interface

The Verifier Metadata Interface defined in CS-02 [5] Section 8.4 applies. Relying Parties MUST additionally declare support for the CSC X.509 credential format in `vp_formats`.

# 9. Conformance

An implementation conforms to this specification as a **Wallet Unit** if it:

1. Conforms to CS-02 [5] Section 9 as a Wallet Provider
2. Implements all Wallet Unit requirements in Section 7.1 of this specification
3. Supports the signing flows defined in Section 6 of this specification

An implementation conforms to this specification as a **Relying Party** if it:

1. Conforms to CS-02 [5] Section 9 as a Verifier (referred to as "Issuer" in CS-02 Section 9)
2. Implements all Relying Party requirements in Section 7.2 of this specification
3. Supports both same-device and cross-device signing flows

# References

[1] OpenID Foundation (2025). OpenID for Verifiable Presentations 1.0. Available at: https://openid.net/specs/openid-4-verifiable-presentations-1_0.html (Accessed: 5 March 2026).

[2] OpenID Foundation (2025). OpenID4VC High Assurance Interoperability Profile - Implementer's Draft 1. Available at: https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-ID1.html (Accessed: 5 March 2026).

[3] Cloud Signature Consortium (2025). CSC Data Model Bindings, version 1.0.0. Published 14 October 2025.

[4] Cloud Signature Consortium (2025). Data Model for Remote Signature Applications, version 1.0.0. Published 16 October 2025.

[5] WE BUILD (2025). Conformance Specification: Credential Presentation, version 1.0. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/cs-02-credential-presentation.md (Accessed: 5 March 2026).

[6] EWC Consortium (2025). RFC-010: Document Signing on a Remote Signing Service Provider using Long-Term Certificates, version 1.1. Available at: https://github.com/EWC-consortium/eudi-wallet-rfcs/blob/main/ewc-rfc010-long-term-certifice-qes-creation.md (Accessed: 5 March 2026).

[7] ETSI EN 319 102-1. Electronic Signatures and Trust Infrastructures (ESI); Procedures for Creation and Validation of AdES Digital Signatures; Part 1: Creation and Validation.
