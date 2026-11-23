# WE BUILD - Pre-flight Conformance Specification CS-021: Attestation Chaining

Version 0.9 / Pre-flight\
Date: 12 November 2026

**Authors / Contributors**: WP4 Architecture / Trust Infrastructure Group

- Werner Folkendt, Robert Bosch GmbH, Germany
- Florin Coptil, Robert Bosch GmbH
- Leif Johansson, SIROS

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language and Terminology](#3-normative-language-and-terminology)
- [4. Trust Model and Key Roles](#4-trust-model-and-key-roles)
- [5. High-level Flows](#5-high-level-flows)
  - [5.1 EBWOID Issuance with EAA Signing Key](#51-ebwoid-issuance-with-eaa-signing-key)
  - [5.2 EAA Issuance and Holder-Side Validation](#52-eaa-issuance-and-holder-side-validation)
  - [5.3 EAA Presentation and Offline Verification](#53-eaa-presentation-and-offline-verification)
- [6. Normative Requirements](#6-normative-requirements)
  - [6.1 EBWOID Provider Requirements](#61-ebwoid-provider-requirements)
  - [6.2 EAA Provider Requirements (Issuance)](#62-eaa-provider-requirements-issuance)
  - [6.3 Holder Wallet Requirements (At Issuance)](#63-holder-wallet-requirements-at-issuance)
  - [6.4 Relying Party Requirements (At Presentation)](#64-relying-party-requirements-at-presentation)
- [7. Interface & Payload Definitions](#7-interface--payload-definitions)
  - [7.1 Extended EBWOID Payload with `cnf_signing`](#71-extended-ebwoid-payload-with-cnf_signing)
  - [7.2 Chained EAA Header with `atc`](#72-chained-eaa-header-with-atc)
- [8. Open Topics and Future Work](#8-open-topics-and-future-work)

---

## 1. Introduction

This document is a **pre-flight conformance specification** designed to enable the first pilot implementation of **Attestation Chaining** as approved in [**ADR#168**](https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/EAA-Chaining.md) and **ADR#371**.

By implementing these specifications, wallet providers and trust infrastructure operators can validate the feasibility of decentralized EAA Provider identity verification, paving the way for formal change requests to **ETSI TS 119 472** and the European Commission's **HAIP** profile.

This specification bridges the trust gap for EAA Providers who cannot be listed directly in national Trusted Lists (TLoLs) due to scalability constraints. It establishes a delegated trust model where an EAA Provider’s signing key is cryptographically bound to their legal identity (EUID) via a QTSP-signed EBWOID, which is then chained directly within the EAA header.

---

## 2. Scope

This specification defines the technical and cryptographic requirements for implementing attestation chaining using **SD-JWT VC** formats.

- **In scope:**
  - The schema extension of the EBWOID to include the dedicated EAA signing key (`cnf_signing`).
  - The definition and processing of the `atc` (Attestation Chain) JOSE header parameter.
  - The cryptographic processing rules for Holder wallets to validate the issuer's EBWOID status at the moment of EAA issuance.
  - The offline verification processing rules for Relying Parties to validate the EAA signature chain back to the Trusted List (TLoL).
- **Out of scope:**
  - EAA issuer key binding verification via an AuthZEN API call [https://github.com/webuild-consortium/wp4-architecture/blob/a40b3d13c5b87bda00aa36283229c73e17d40732/adr/eaa-key-binding-authzen.md](https://github.com/webuild-consortium/wp4-architecture/blob/a40b3d13c5b87bda00aa36283229c73e17d40732/adr/eaa-key-binding-authzen.md)
  - Formats other than SD-JWT VC (e.g., mdoc is out of scope for this pilot).
  - The detailed implementation of Long-Term Validation (LTV) timestamps, which is deferred to a separate specification.
  - Hierarchical Key Delegation for Key Rotation (as described in ADR-168 Section 2.3) is designated as an advanced extension and is out of scope for the initial pilot implementation. The core processing rules defined herein are designed to be fully extendable to support multi-level delegation chains in future revisions.

---

## 3. Normative Language and Terminology

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, and **MAY** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

| **Term**          | **Meaning in this specification**                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **EBWOID**        | European Business Wallet Owner Identity. The qualified identity credential used as the trust anchor link for the EAA Provider. |
| **`cnf`**         | The standard confirmation claim inside the EBWOID, used strictly for hardware device-binding and interactive authentication.   |
| **`cnf_signing`** | The newly introduced confirmation claim inside the EBWOID, used strictly for attesting the EAA signing public key.             |
| **`atc`**         | Attestation Chain. The newly defined JOSE header parameter used to carry the chained EBWOID within the EAA.                    |

---

## 4. Trust Model and Key Roles

This specification implements the **Delegated Chaining Trust Model**. Trust is not established directly from the TLoL to the EAA. Instead, trust is delegated cryptographically through the following path:



```
   [ eIDAS Trusted List (TLoL) ]
                 │
                 ▼
     [ EBWOID Provider (QTSP) ] (Signs EBWOID)
                 │
                 ▼
         [ EBWOID payload ] ──(attests)──► [ cnf_signing public key ]
                 │                                        │
                 ▼                                        ▼
      [ Chained EAA Header ] ◄──(signed by)── [ EAA Provider Private Key ]

```

---

## 5. High-level Flows

### 5.1 EBWOID Issuance with EAA Signing Key

Remark: The table was added because github's preview does not display the following code: 
```mermaid
sequenceDiagram
    participant WU as EBW Wallet Unit
    participant EP as EBWOID Provider (QTSP)
    autonumber
    WU->>WU: Generate cnf key pair for device authentication
    WU->>WU: Generate cnf_signing key pair for EAA signing
    WU->>EP: Request EBWOID via OpenID4VCI with proof of possession for both public keys
    EP->>EP: Validate legal identity (EUID)
    EP->>EP: Bind both public keys to EUID in the EBWOID payload
    EP->>WU: Return EBWOID carrying cnf and cnf_signing
```

| Step | From | To | Interaction |
| --- | --- | --- | --- |
| 1 | EBW Wallet Unit | EBW Wallet Unit | Generate `cnf` key pair for device authentication |
| 2 | EBW Wallet Unit | EBW Wallet Unit | Generate `cnf_signing` key pair for EAA signing |
| 3 | EBW Wallet Unit | EBWOID Provider (QTSP) | Request EBWOID via OpenID4VCI with proof of possession for both public keys |
| 4 | EBWOID Provider (QTSP) | EBWOID Provider (QTSP) | Validate legal identity (EUID) |
| 5 | EBWOID Provider (QTSP) | EBWOID Provider (QTSP) | Bind both public keys to EUID in the EBWOID payload |
| 6 | EBWOID Provider (QTSP) | EBW Wallet Unit | Return EBWOID carrying `cnf` and `cnf_signing` |

1. The EBW Wallet Unit generates two distinct key pairs: one for device binding (`cnf`) and one for EAA signing (`cnf_signing`).
2. The Wallet Unit requests the EBWOID from the EBWOID Provider using **OpenID4VCI**. The request includes both public keys, accompanied by Proof of Possession (PoP) signatures for each.
3. The EBWOID Provider validates the organization's legal identity (EUID) and issues the EBWOID, sealing both public keys within the payload.

### 5.2 EAA Issuance and Holder-Side Validation

Remark: The table was added because github's preview does not display the following code: 
```mermaid
sequenceDiagram
    participant EAP as EAA Provider (Issuer)
    participant HW as Holder Wallet
    participant EP as EBWOID Provider (QTSP)
    autonumber
    EAP->>EAP: Embed the issuer EBWOID in the EAA atc header
    EAP->>EAP: Sign the EAA with the private key corresponding to cnf_signing
    EAP->>HW: Issue the chained EAA via OpenID4VCI
    HW->>EP: Check current EBWOID revocation status
    EP-->>HW: Return EBWOID revocation status
    alt EBWOID is valid
        HW->>HW: Store the EAA
    else EBWOID is revoked or invalid
        HW->>HW: Reject the EAA
    end
```

| Step | From | To | Interaction |
| --- | --- | --- | --- |
| 1 | EAA Provider (Issuer) | EAA Provider (Issuer) | Embed the issuer EBWOID in the EAA `atc` header |
| 2 | EAA Provider (Issuer) | EAA Provider (Issuer) | Sign the EAA with the private key corresponding to `cnf_signing` |
| 3 | EAA Provider (Issuer) | Holder Wallet | Issue the chained EAA via OpenID4VCI |
| 4 | Holder Wallet | EBWOID Provider (QTSP) | Check current EBWOID revocation status |
| 5 | EBWOID Provider (QTSP) | Holder Wallet | Return EBWOID revocation status |
| 6 | Holder Wallet | Holder Wallet | **If EBWOID is valid:** Store the EAA |
| 7 | Holder Wallet | Holder Wallet | **If EBWOID is revoked or invalid:** Reject the EAA |

1. The EAA Provider (Issuer) signs the EAA using the private key corresponding to the `cnf_signing` key attested in their EBWOID.
2. The EAA Provider embeds their full EBWOID credential in the `atc` header of the EAA and transmits it to the Holder's wallet via **OpenID4VCI**.
3. Before storing the EAA, the **Holder's wallet MUST perform a live revocation check** of the issuer's EBWOID against the issuing EBWOID Provider's revocation endpoint (e.g., OCSP).
4. If the EBWOID is valid, the Holder's wallet stores the EAA. **This step locks the validity of the issuer's identity to the moment of issuance.**

### 5.3 EAA Presentation and Offline Verification

Remark: The table was added because github's preview does not display the following code: 
```mermaid
sequenceDiagram
    participant HW as Holder Wallet
    participant RP as Relying Party (Verifier)
    autonumber
    HW->>RP: Present EAA via OpenID4VP
    RP->>RP: Extract the chained EBWOID from the atc header
    RP->>RP: Extract the cnf_signing public key from the EBWOID payload
    RP->>RP: Verify the EAA signature using cnf_signing
    RP->>RP: Validate the EBWOID signature and x5c certificate chain against the TLoL
    RP->>RP: Check current EAA revocation status
```

| Step | From | To | Interaction |
| --- | --- | --- | --- |
| 1 | Holder Wallet | Relying Party (Verifier) | Present EAA via OpenID4VP |
| 2 | Relying Party (Verifier) | Relying Party (Verifier) | Extract the chained EBWOID from the `atc` header |
| 3 | Relying Party (Verifier) | Relying Party (Verifier) | Extract the `cnf_signing` public key from the EBWOID payload |
| 4 | Relying Party (Verifier) | Relying Party (Verifier) | Verify the EAA signature using `cnf_signing` |
| 5 | Relying Party (Verifier) | Relying Party (Verifier) | Validate the EBWOID signature and `x5c` certificate chain against the TLoL |
| 6 | Relying Party (Verifier) | Relying Party (Verifier) | Check current EAA revocation status |

1. The Holder presents the EAA to the Relying Party (RP) via **OpenID4VP**.
2. The RP extracts the EAA Provider's EBWOID from the `atc` header parameter.
3. The RP extracts the `cnf_signing` public key from the EBWOID and validates the EAA's digital signature.
4. The RP validates the EBWOID's signature and certificate chain (extracted from the EBWOID's `x5c` header) against the Trusted List (TLoL).
5. The RP performs a **current** revocation check on the **EAA itself**. It does not need to perform a retroactive revocation check on the EBWOID, trusting the Holder's wallet's validation at issuance.

---

## 6. Normative Requirements

### 6.1 EBWOID Provider Requirements

| **ID**        | **Requirement**                                                                                                                                                                        |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EBP-TV-01** | The EBWOID Provider **MUST** support the inclusion of the `cnf_signing` claim within the EBWOID payload alongside the standard `cnf` claim.                                            |
| **EBP-TV-02** | The EBWOID Provider **MUST** require a Proof of Possession (PoP) signature for the `cnf_signing` public key during the OpenID4VCI issuance flow before including it in the credential. |
| **EBP-TV-03** | The EBWOID Provider **MUST** include its full X.509 certificate chain (excluding the TLoL root) in the `x5c` JOSE header of the issued EBWOID.                                         |

### 6.2 EAA Provider Requirements (Issuance)

| **ID**        | **Requirement**                                                                                                                                     |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EAP-TV-01** | The EAA Provider **MUST** sign all issued EAAs using the private key corresponding to the `cnf_signing` public key attested in their active EBWOID. |
| **EAP-TV-02** | The EAA Provider **MUST** include their full, serialized EBWOID credential within the newly defined `atc` JOSE header parameter of each issued EAA. |

### 6.3 Holder Wallet Requirements (At Issuance)

| **ID**       | **Requirement**                                                                                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **HW-TV-01** | Before accepting and storing a newly issued EAA, the Holder's wallet **MUST** perform a live revocation check (via OCSP or CRL) of the EAA issuer's chained EBWOID. |
| **HW-TV-02** | If the issuer's EBWOID is revoked or invalid at the moment of issuance, the Holder's wallet **MUST** reject the EAA and MUST NOT store it.                          |

### 6.4 Relying Party Requirements (At Presentation)

| **ID**       | **Requirement**                                                                                                                                                                                                                       |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RP-TV-01** | Upon receiving a presented EAA, the Relying Party **MUST** check for the presence of the `atc` JOSE header parameter. If present, the RP **MUST** execute the attestation chaining verification flow.                                 |
| **RP-TV-02** | The RP **MUST** extract the EAA Provider's EBWOID from the `atc` array and extract the `cnf_signing` public key from that EBWOID's payload.                                                                                           |
| **RP-TV-03** | The RP **MUST** validate the EAA's digital signature using the extracted `cnf_signing` public key.                                                                                                                                    |
| **RP-TV-04** | The RP **MUST** validate the EBWOID's signature and certificate chain (extracted from the EBWOID's `x5c` header) against the Trusted List (TLoL).                                                                                     |
| **RP-TV-05** | The RP **SHOULD** utilize a locally stored, cached copy of the TLoL (refreshed daily) as its default validation behavior. If a locally cached copy is unavailable, the RP **MAY** fall back to fetching the TLoL online in real-time. |
| **RP-TV-06** | The RP **MUST NOT** perform a historical or retroactive revocation check on the chained EBWOID, but **MUST** perform a standard, current revocation check on the EAA itself.                                                          |

---

## 7. Interface & Payload Definitions

### 7.1 Extended EBWOID Payload with `cnf_signing`

Below is the illustrative JSON payload of an EBWOID conforming strictly to the **We Build EBWOID Rulebook Schema**, extended with the dedicated `cnf_signing` key pair.

```json
{
  "vct": "uri:eu.ebw.oid.1",
  "id": "NOFOR.123456789",
  "name": "Example AS",
  "attestation_legal_category": "PUB-EAA",
  "issuing_authority": "Brønnøysundregistrene",
  "issuing_country": "NO",
  "date_of_expiry": "2026-12-31",
  "trust_anchor": "https://tl.eidas.europa.eu/tl-browser/#/",
  "status": {
    "type": "status-list",
    "status_list_credential": "https://issuer.example.no/status/1",
    "status_list_index": 42,
    "status_purpose": "revocation"
  },
  "cnf": {
    "jwk": {
        "kty": "EC",
        "crv": "P-256",
        "x": "52aDI_ur05n1f_p3jiYGUU82oKZr3m4LsAErM536crQ",
        "y": "ckhZ-KQ5aXNL91R8Eufg1aOf8Z5pZJnIvuCzNGfdnzo"
    }
  },
  "cnf_signing": {
    "jwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "h73JD82ksD_s9_DedicatedSigningKeyForEAAIssuance",
      "y": "k92JDm38ds_d8_DedicatedSigningKeyForEAAIssuance"
    }
  }
}
```

### 7.2 Chained EAA Header with `atc`

Below is the illustrative JOSE header of an EAA signed by the EAA Provider. The `atc` parameter carries the complete, compact serialized EBWOID shown above (including the EBWOID Provider's intermediate certificates in its own `x5c` header).

```json
{
  "alg": "ES256",
  "typ": "dc+sd-jwt",
  "atc": [
    "eyJhbGciOiJFUzI1NiIsIng1YyI6WyJNSUlDLi4uUVRTUC1zZWFsLWNlcnQiLCJNSUlDLi4uUVRTUC1pbnRlcm1lZGlhdGUiXX0.eyJ2Y3QiOiJ1cmk6ZXUuZWJ3Lm9pZC4xIiwiaWQiOiJOT0ZPUi4xMjM0NTY3ODkiLCJjbmZfc2lnbmluZyI6eyJqd2siOnsia3R5IjoiRUMiLCJjcnYiOiJQLTI1NiIsIngiOiJoNzNKRDgyayJ9fX0.signature-of-qtsp"
  ]
}
```

---

## 8. Open Topics and Future Work

Implementers of this pre-flight specification are requested to gather and report experience on the following topics:

1. **OpenID4VCI Support for Two PoP Signatures:** Does standard wallet software handle requesting a single credential (the EBWOID) while generating and sending two separate Proof of Possession (PoP) signatures (one for `cnf` and one for `cnf_signing`) in the same token request?
2. **`atc` Header Parameter Overhead:** Measure the exact network and memory overhead introduced by carrying the compact EBWOID (typically 1.5–2 KB) in the EAA header, especially during wallet-to-wallet transfers over constrained channels.
3. **Library Compatibility with `cnf_signing`:** Confirm if standard SD-JWT verification libraries can be easily configured to look for the public key in `cnf_signing` instead of the default `cnf` claim.
4. **Future Path for Hierarchical Key Delegation:**
   - The basic chaining model specified in this document requires the EAA to be signed directly by the `cnf_signing` key attested in the EBWOID. To support routine key rotation without requiring EBWOID re-issuance, future revisions will test the "Hierarchical Key Delegation" model.
   - Under this model, the issuer self-signs an "Issuing Attestation" containing a subordinate key, signed by their primary `cnf_signing` key. Because the `atc` header parameter is defined as an array of JWTs, the system can seamlessly extend to carry both the Issuing Attestation and the EBWOID in the header `[atc_EAA -> Issuing_Attestation, EBWOID]` without modifying the underlying protocol schemas. We seek feedback on the legal and technical implications of this delegation model.

## 9. Conformance

An **EBW Wallet Unit (Holder/Issuer)** conforms to this specification if it satisfies the requirements in **Section 6.2** (for EAA issuance) and **Section 6.3** (for Holder-side validation).

An **EBW Relying Party (Verifier)** conforms to this specification if it satisfies the requirements in **Section 6.4** and correctly parses the interface payloads defined in **Section 7**.

