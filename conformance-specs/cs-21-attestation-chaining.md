# WE BUILD - Pre-flight Conformance Specification CS-019: Attestation Chaining

Version 0.9.2 / Pre-flight\
Date: 25 November 2026  

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
- [9. Conformance](#9-conformance)
- [Annex A (informative): Target Production State (Long-Term Validation and Timestamps)](#annex-a-informative-target-production-state-long-term-validation-and-timestamps)

---

## 1. Introduction

This document is a **pre-flight conformance specification** designed to enable the first pilot implementation of **Attestation Chaining** as approved in [**ADR#168**](https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/EAA-Chaining.md) and in line with the hybrid model proposed in [**ADR#371**](https://github.com/webuild-consortium/wp4-architecture/pull/371).

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
  - The detailed, production-grade protocol implementations for external Qualified and Batch Timestamping (such as RFC 3161 or Merkle tree batching) are deferred to a separate specification. The pilot's native Wallet-Internal Timestamping is specified directly within this document.
  - Hierarchical Key Delegation for Key Rotation (as described in ADR-168 Section 2.3) is designated as an advanced extension and is out of scope for the initial pilot implementation. The core processing rules defined herein are designed to be fully extendable to support multi-level delegation chains in future revisions.

---

## 3. Normative Language and Terminology

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, and **MAY** in this document are to be interpreted as described in [RFC 2119].

| Term | Meaning in this specification |
| :--- | :--- |
| **EBWOID** | European Business Wallet Owner Identity. The qualified identity credential used as the trust anchor link for the EAA Provider. |
| **`cnf`** | The standard confirmation claim inside the EBWOID, used strictly for hardware device-binding and interactive authentication. |
| **`cnf_signing`** | The newly introduced confirmation claim inside the EBWOID, used strictly for attesting the EAA signing public key. |
| **`atc`** | Attestation Chain. The newly defined JOSE header parameter used to carry the chained EBWOID within the EAA. |

---

## 4. Trust Model and Key Roles

This specification implements the **Delegated Chaining Trust Model**. Trust is not established directly from the TLoL to the EAA. Instead, trust is delegated cryptographically through the following path:

$$\text{TLoL} \rightarrow \text{EBWOID Provider} \rightarrow \text{EBWOID} \rightarrow \text{cnf\_signing} \rightarrow \text{EAA}$$

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

```mermaid
sequenceDiagram
    autonumber
    participant WU as EBW Wallet Unit
    participant EP as EBWOID Provider (QTSP)
    WU->>WU: Generate 'cnf' key (device authentication)
    WU->>WU: Generate 'cnf_signing' key (EAA signing)
    WU->>EP: Request EBWOID (with POP for both keys)
    EP->>EP: Validate legal identity (EUID)
    EP->>EP: Bind keys to EUID in EBWOID payload
    EP->>WU: Return EBWOID (carrying cnf and cnf_signing)
```

1.  The EBW Wallet Unit generates two distinct key pairs: one for device binding (`cnf`) and one for EAA signing (`cnf_signing`).
2.  The Wallet Unit requests the EBWOID from the EBWOID Provider using **OpenID4VCI**. The request includes both public keys, accompanied by Proof of Possession (PoP) signatures for each.
3.  The EBWOID Provider validates the organization's legal identity (EUID) and issues the EBWOID, sealing both public keys within the payload.

### 5.2 EAA Issuance and Holder-Side Validation

```mermaid
sequenceDiagram
    autonumber
    participant IP as "EAA Provider (Issuer)"
    participant HW as "Holder Wallet"
    participant Q as "EBWOID Status Provider (CS-010)"
    IP->>IP: Sign EAA with cnf_signing private key
    IP->>IP: Embed EBWOID in EAA 'atc' header
    IP->>HW: Send EAA via OpenID4VCI
    alt EBWOID valid
        HW->>Q: Query status list token (CS-010)
        Q-->>HW: Return 'Good' status list
        HW->>HW: Store EAA in wallet
    else revoked or invalid
        HW->>HW: Reject EAA
    end
```

1.  The EAA Provider (Issuer) signs the EAA using the private key corresponding to the `cnf_signing` key attested in their EBWOID.
2.  The EAA Provider embeds their full EBWOID credential in the `atc` header of the EAA and transmits it to the Holder's wallet via **OpenID4VCI**.
3.  Before storing the EAA, the **Holder's wallet MUST check the current status** of the issuer's EBWOID against the Status List Token referenced in its status claim (CS-010).
4.  If the EBWOID is valid, the Holder's wallet stores the EAA; otherwise, it is rejected.

### 5.3 EAA Presentation and Offline Verification

```mermaid
sequenceDiagram
    autonumber
    participant HW as "Holder Wallet"
    participant RP as "Relying Party (Verifier)"
    HW->>RP: Present EAA (carrying chained EBWOID in 'atc' header)
    RP->>RP: Extract EBWOID and cnf_signing key from 'atc' header
    RP->>RP: Verify EAA signature using cnf_signing key
    RP->>RP: Verify EBWOID signature against TLoL
    RP->>RP: RP checks the current status and expiry of the EBWOID (CS-010)
    alt EBWOID revoked, expired, or status unobtainable
        RP->>RP: Reject EAA
    else EBWOID valid
        RP->>RP: RP checks the current status of both the issuer's EBWOID and the EAA itself (CS-010)
        Note over RP: Offline verification is possible within<br/>the caching period of the Status List Tokens
        RP->>RP: Trust EAA
    end
```

1.  The Holder presents the EAA to the Relying Party (RP) via **OpenID4VP**.
2.  The RP extracts the EAA Provider's EBWOID from the `atc` header parameter.
3.  The RP extracts the `cnf_signing` public key from the EBWOID and validates the EAA's digital signature.
4.  The RP validates the EBWOID's signature and certificate chain (extracted from the EBWOID's `x5c` header) against the Trusted List (TLoL).
5.  The RP performs a **current** revocation check on the **EAA itself**, as well as the **chained EBWOID** using the Status List Token referenced in the EBWOID's status claim (CS-010).

---

## 6. Normative Requirements

### 6.1 EBWOID Provider Requirements

| ID | Requirement |
| :--- | :--- |
| **EBP-TV-01** | The EBWOID Provider **MUST** support the inclusion of the `cnf_signing` claim within the EBWOID payload alongside the standard `cnf` claim. |
| **EBP-TV-02** | The EBWOID Provider **MUST** require a Proof of Possession (PoP) signature for the `cnf_signing` public key during the OpenID4VCI issuance flow before including it in the credential. |
| **EBP-TV-03** | The EBWOID Provider **MUST** include its full X.509 certificate chain (excluding the TLoL root) in the `x5c` JOSE header of the issued EBWOID. |
| **EBP-TV-04** | *(Optional)* The EBWOID Provider **SHOULD** include a `cnf_signing` key only if it is listed in the `attested_keys` field of a valid Server Key Attestation (CS-005). |

### 6.2 EAA Provider Requirements (Issuance)

| ID | Requirement |
| :--- | :--- |
| **EAP-TV-01** | The EAA Provider **MUST** sign all issued EAAs using the private key corresponding to the `cnf_signing` public key attested in their active EBWOID. |
| **EAP-TV-02** | The EAA Provider **MUST** include their full, serialized EBWOID credential within the newly defined `atc` JOSE header parameter of each issued EAA. |

### 6.3 Holder Wallet Requirements (At Issuance)

| ID | Requirement |
| :--- | :--- |
| **HW-TV-01** | Before accepting and storing a newly issued EAA, the Holder's wallet **MUST** check the current status of the issuer's chained EBWOID using the Status List Token referenced in the EBWOID's status claim (CS-010). |
| **HW-TV-02** | If the issuer's EBWOID is revoked or invalid at the moment of issuance, the Holder's wallet **MUST** reject the EAA and MUST NOT store it. |

*Note: These checks protect the Holder and the Relying Party. A Relying Party relies on them, because the Relying Party need a confirmation during EAA verification that the EBWOID was not revoked at the point in time of issuance. This removes the obligation for a Relying party to perform a revocation check with a time parameter.*

### 6.4 Relying Party Requirements (At Presentation)

| ID | Requirement |
| :--- | :--- |
| **RP-TV-01** | Upon receiving a presented EAA, the Relying Party **MUST** check for the presence of the `atc` JOSE header parameter. If present, the RP **MUST** execute the attestation chaining verification flow. |
| **RP-TV-02** | The RP **MUST** extract the EAA Provider's EBWOID from the `atc` array and extract the `cnf_signing` public key from that EBWOID's payload. |
| **RP-TV-03** | The RP **MUST** validate the EAA's digital signature using the extracted `cnf_signing` public key. |
| **RP-TV-04** | The RP **MUST** validate the EBWOID's signature and certificate chain, using the certificates in its `x5c` header, up to the trust anchor of the EBWOID Provider in the WE BUILD LoTL. The EBWOID Provider can be a QTSP or a public body. |
| **RP-TV-05** | The RP **SHOULD** utilize a locally stored, cached copy of the TLoL (refreshed daily) as its default validation behavior. If a locally cached copy is unavailable, the RP **MAY** fall back to fetching the TLoL online in real-time. |
| **RP-TV-08** | The RP **MUST** perform a standard, current revocation check on the EAA itself. |
| **RP-TV-10** | The RP **MUST** check the current status of the chained EBWOID using the Status List Token referenced in the EBWOID's status claim (CS-010 RP-RV-02, RP-RV-03). The RP **MUST** reject the EAA if the status is INVALID or cannot be obtained, whatever the EAA's `iat`. (Note: rejecting when the status is unobtainable is intentionally stricter than CS-010 RP-RV-05 for pilot testability). |
| **RP-TV-11** | The RP **MUST** reject the EAA if the chained EBWOID has expired at the time of verification (`exp`, or `date_of_expiry`). |
| **RP-TV-12** | The RP **MUST** verify that the chained credential's `vct` identifies it as an EBWOID, and **MUST** take the identity of the EAA Provider strictly from that EBWOID to prevent identity spoofing attacks. |

---

## 7. Interface & Payload Definitions

### 7.1 Extended EBWOID Payload with `cnf_signing`

Below is the illustrative JSON payload of an EBWOID conforming strictly to the **We Build EBWOID Rulebook Schema**, extended with the dedicated `cnf_signing` key pair and using the CS-010 Status List schema.

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
    "status_list": {
      "idx": 42,
      "uri": "https://issuer.example.no/statuslists/1"
    }
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

## 8. Open Topics and Future Work

Implementers of this pre-flight specification are requested to gather and report experience on the following topics:

1.  **OpenID4VCI Support for Two PoP Signatures:** Does standard wallet software handle requesting a single credential (the EBWOID) while generating and sending two separate Proof of Possession (PoP) signatures (one for `cnf` and one for `cnf_signing`) in the same token request?
2.  **`atc` Header Parameter Overhead:** Measure the exact network and memory overhead introduced by carrying the compact EBWOID (typically 1.5–2 KB) in the EAA header, especially during wallet-to-wallet transfers over constrained channels.
3.  **Library Compatibility with `cnf_signing`:** Confirm if standard SD-JWT verification libraries can be easily configured to look for the public key in `cnf_signing` instead of the default `cnf` claim.
4.  **Future Path for Hierarchical Key Delegation:**
    *   The basic chaining model specified in this document requires the EAA to be signed directly by the `cnf_signing` key attested in the EBWOID. To support routine key rotation without requiring EBWOID re-issuance, future revisions will test the "Hierarchical Key Delegation" model.
    *   Under this model, the issuer self-signs an "Issuing Attestation" containing a subordinate key, signed by their primary `cnf_signing` key. Because the `atc` header parameter is defined as an array of JWTs, the system can seamlessly extend to carry both the Issuing Attestation and the EBWOID in the header `[atc_EAA -> Issuing_Attestation, EBWOID]` without modifying the underlying protocol schemas. We seek feedback on the legal and technical implications of this delegation model.
5.  **Known Pilot Limitations (Temporary departure from the LTV baseline):**
    *   A genuine EAA is rejected once its issuer's EBWOID is revoked for any reason, including routine events such as relocation or merger (see [Critical Verification Failures for Valid EAAs Due to Lack of Historical Key-Binding Interface #358](https://github.com/webuild-consortium/wp4-architecture/issues/358)), or expires. This is a temporary departure from the LTV baseline of ADR [ADR #168](https://github.com/webuild-consortium/wp4-architecture/pull/168) §3. The pilots test the identity link established by chaining, not its long-term validity. A forged EAA signed with a compromised `cnf_signing` key is accepted until the revocation is published (CS-010 `ISS-RV-05`) and the RP's cached Status List Token expires.

---

## 9. Conformance

An **EBW Wallet Unit (Holder/Issuer)** conforms to this specification if it satisfies the requirements in **Section 6.2** (for EAA issuance) and **Section 6.3** (for Holder-side validation).

An **EBW Relying Party (Verifier)** conforms to this specification if it satisfies the requirements in **Section 6.4** and correctly parses the interface payloads defined in **Section 7**.

---

## Annex A (informative): Target Production State (Long-Term Validation and Timestamps)

To move from the pilot's simplified verification model back to the full target eIDAS-compliance architecture, the following design guidelines for **Long-Term Validation (LTV) and Trusted Timestamps** are preserved for future standardization:

1.  **The Token Status List Limitations:**
    *   A standard 1-bit or 2-bit Token Status List carries no cryptographic revocation time or historical logs. 
2.  **Required Cryptographic Signature Bindings:**
    *   One design that works without changing CS-010 needs both an independent, trusted timestamp and a status proof embedded at the moment of signing. This is the "trusted timestamps and embedded revocation proofs" of [ADR #168](https://github.com/webuild-consortium/wp4-architecture/pull/168) §3.
3.  **Standard Representation in SD-JWT VC:**
    *   A secure signature timestamp requires a formally defined, standardized place inside the JOSE/COSE headers of the SD-JWT VC format.
4.  **Securing the Time Source:**
    *   A wallet-internal timestamp (Option C in the ADR #403 point-in-time-validity (https://github.com/webuild-consortium/wp4-architecture/pull/403) requires a certified, tamper-proof internal hardware clock and cryptographic key that the EAA issuer cannot unilaterally alter or backdate, preventing insider forgery.

In a future version of this CS the following normative requirements will be added to enable log term verification and protect against key compromise + backdating attacks.
**6.1 EBWOID Provider Requirements**

| ID | Requirement |
| :--- | :--- |
| **EBP-TV-0x** | The EBWOID Provider **MUST** include its full X.509 certificate chain (excluding the TLoL root) in the `x5c` JOSE header of the issued EBWOID. |

** 6.2 EAA Provider Requirements (Issuance)**

| ID | Requirement |
| :--- | :--- |
| **EAP-TV-0x** | To secure the signing time and prevent key-compromise backdating fraud, the EAA Provider **MUST** obtain a **Trusted Timestamp (TSA)** over the EAA signature from an independent, trusted Time-Stamping Authority, and embed this timestamp token directly within the EAA signature block. |

**6.3 Holder Wallet Requirements (At Issuance)**

| ID | Requirement |
| :--- | :--- |
| **HW-TV-0x** | If the issuer's EBWOID is revoked or invalid at the moment of issuance, the Holder's wallet **MUST** reject the EAA and MUST NOT store it. |

**6.4 Relying Party Requirements (At Presentation)**

| ID | Requirement |
| :--- | :--- |
| **RP-TV-0x** | The RP **MUST** extract the embedded **Trusted Timestamp** from the EAA signature block and verify its cryptographic signature. |
| **RP-TV-0x+1** | If the issuer's EBWOID is currently revoked, the RP **MUST** check the QTSP's revocation list (CRL or OAuth Status List) to retrieve the **revocation time** and **revocation reason**. If the revocation reason is `keyCompromise` and the EAA's Trusted Timestamp is **after** the revocation time, the RP **MUST** reject the EAA. If the timestamp is before the revocation time, the EAA is accepted. |
| **RP-TV-0x+2** | The RP **MUST** perform a standard, current revocation check on the EAA itself. |

---




