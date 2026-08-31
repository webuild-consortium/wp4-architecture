# WE BUILD - Pre-flight Conformance Specification: SCA Attestations for payment transactions (TS12 Profile)

Version 0.7 (Draft) Date: 31 August 2026

**Revision history**
- Version 0.7 (31 August 2026): Initial draft, profiling TS12 [1] for use within WE BUILD.

**Authors / Contributors**:
- Stefan Kauhaus, Visa, Germany

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [Normative Language](#3-normative-language)
4. [Roles and Components](#4-roles-and-components)
5. [Protocol Overview](#5-protocol-overview)
6. [High-level Flows](#6-high-level-flows)
   - 6.1 [Issuer-requested Flow](#61-issuer-requested-flow)
   - 6.2 [Third-party-requested Flow](#62-third-party-requested-flow)
7. [Normative Requirements](#7-normative-requirements)
   - 7.1 [Common Requirements (Attestation Provider, WU and RP)](#71-common-requirements-attestation-provider-wu-and-rp)
   - 7.2 [Attestation Provider Requirements](#72-attestation-provider-requirements)
   - 7.3 [Wallet Unit Requirements](#73-wallet-unit-requirements)
   - 7.4 [Relying Party Requirements](#74-relying-party-requirements)
8. [Interface Definitions](#8-interface-definitions)
   - 8.1 [SCA Authorization Request](#81-sca-authorization-request)
   - 8.2 [SCA Authorization Response](#82-sca-authorization-response)
9. [Conformance](#9-conformance)
10. [References](#references)

## 1. Introduction

This document is a **pre-flight conformance specification** as per ADR-21 [12], defining the WE BUILD Conformance Specification for SCA Attestations used in payment transactions. It profiles TS12 [1], the European Commission's technical specification for implementing Strong Customer Authentication (SCA) under PSD2 [8] with the EU Digital Identity Wallet, for use between WE BUILD consortium partners in the WP3 (Wallet for Payments) use cases.

TS12 [1] is itself a profile of SD-JWT-VC [9] and OpenID4VP [10], consistent with the baseline protocols adopted by the consortium in ADR-2 [3] and the credential-format decisions in ADR-3 [4]. This CS narrows TS12 [1] further, for WE BUILD purposes only, as follows:

1. **Attestation types**: only the three SCA Attestation types defined in the WE BUILD Attestation Rulebooks Catalog [2] — `sca-card-dpc`, `sca-iban`, and `sca-user` — are in scope. No other SCA Attestation type is profiled by this CS.
2. **Transaction type**: only the `payment` transaction type (`urn:eudi:sca:payment:1`) is used. The `login_risk_transaction`, `account_access`, and `emandate` transaction types defined in TS12 [1] §4.3 are out of scope for WE BUILD.
3. **Single-attestation presentation**: only one SCA Attestation — `sca-card-dpc`, `sca-iban`, or `sca-user` — is presented to the RP per Authorization Request. Combined presentations across these three types are not used in WE BUILD.
4. **Embedded Disclosure Policy**: WE BUILD does **not** make use of the Embedded Disclosure Policy feature described in TS12 [1] §3.1.

Separately, this CS relaxes one TS12 [1] requirement from a mandatory to an optional level:

1. **Transaction Log Inclusion**: TS12 [1] §5.3 requires Wallet Units to log defined transaction data for every SCA presentation; this CS treats it as an optional Wallet Unit capability (§2, §7.3.11).

This CS is intended to be read together with CS-01 [5] (Credential Issuance) and CS-02 [6] (Credential Presentation), which define the general issuance and presentation mechanics that this document specialises for SCA. It also relies on CS-04 [7] for Wallet Unit Attestation (WUA) validity and revocation, which gates the issuance of SCA Attestations.

This document is intended to support the Interoperability Test Bed (ITB) and does not itself define the SCA Attestation types, their claims, or their trust/revocation mechanisms — these are defined in the respective Rulebooks (`rb-sca-card-dpc`, `rb-sca-iban`, `rb-sca-user`) in the Rulebooks Catalog [2].

## 2. Scope

This CS defines conformance requirements for **Attestation Providers**, **Wallet Units (WU)**, and **Relying Parties (RP)** when an SCA Attestation of type `sca-card-dpc`, `sca-iban`, or `sca-user` is presented to authenticate a payment transaction within WE BUILD.

**In scope:**
- Detection and processing of SCA Attestations belonging to one of the three named types, including their `extends` chain to the base SCA VCT.
- Construction, transmission, and validation of a `payment` (`urn:eudi:sca:payment:1`) transaction data object, including Dynamic Linking and consent-screen rendering.
- Signed Request Verification (authenticity and integrity of the Authorization Request) for all in-scope SCA presentations, mandatory.
- The `aud` claim as the only attestation-level RP-permission control available, applicable solely to `sca-user` presentations in the Issuer-requested flow (§6.1).
- Key Binding JWT (KB-JWT) requirements (`jti`, `amr`, `response_mode`, `transaction_data_hashes`) for SCA presentations.

**Out of scope (deviations from TS12 [1]):**
- Presentation of more than one of the three in-scope SCA Attestation types (e.g. `sca-user` alongside `sca-iban` or `sca-card-dpc`) in a single Authorization Request. Only one of the three in-scope attestation types is presented to the RP at a time. This is a WE BUILD-specific restriction and is distinct from the Combined Presentation pattern of TS12 [1] §3.4, which concerns combining a single SCA Attestation with a different, non-SCA attestation (e.g. payment plus age verification, driver's licence, or loyalty cards); that pattern is not addressed by this CS.
- The `login_risk_transaction`, `account_access`, and `emandate` transaction types. TS12 [1] §4.3 requires Wallet Units to support processing and rendering of all four built-in transaction types; under this profile, WU conformance is assessed only against the `payment` type, and implementers are not required to implement the other three to conform to this CS.
- The Embedded Disclosure Policy feature and the associated Disclosure Policy Verification step of TS12 [1] §3.1.1. WE BUILD Attestation Providers issuing `sca-card-dpc`, `sca-iban`, or `sca-user` attestations do not embed a disclosure policy (§7.2), and Wallet Units are not required to implement disclosure-policy evaluation logic for these attestation types.
- Mandatory Transaction Log Inclusion. TS12 [1] §5.3 requires, at a "SHALL" level, Wallet Units to log defined transaction data for every SCA presentation; under this profile, this is relaxed to an optional capability (§7.3.11), and Wallet Providers are not required to implement it to conform to this CS.
- Attestation-level RP-permission control for `sca-card-dpc`, and for `sca-iban` in the Third-party-requested flow (§6.2). Because Embedded Disclosure Policy is excluded (above) and no `aud` restriction applies in these cases, this profile has no mechanism restricting which Relying Parties may request these attestations beyond Signed Request Verification's authenticity check; a conforming Wallet Unit will present to any Relying Party whose request passes Signed Request Verification, whether by valid signature or, for an unsigned request, the Holder's explicit confirmation (§7.3.3).
- Any SCA Attestation type other than `sca-card-dpc`, `sca-iban`, and `sca-user`.
- ISO/IEC 18013-5 (mdoc) encodings of `sca-iban` and `sca-user`. Although the respective Rulebooks define mdoc namespaces, TS12 [1] itself is scoped to SD-JWT-VC [9].
- SCA Attestation registration / issuance binding, Open Banking / PSD2 interbank messaging between TPPs and ASPSPs, and account information services generally — all out of scope of TS12 [1] itself and unchanged here.
- WUA issuance and revocation mechanics, which are defined in CS-04 [7] and only referenced here as an issuance precondition.

## 3. Normative Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119 and RFC 8174, only when they appear in all capitals.

## 4. Roles and Components

- **Wallet Unit (WU)** — the EUDI Wallet software/hardware combination holding and presenting SCA Attestations on behalf of the Holder.
- **Holder / Payment Service User (PSU)** — the natural person controlling the Wallet Unit and completing SCA for a payment.
- **Attestation Provider (ASPSP / Issuer)** — the payment service provider issuing an `sca-card-dpc`, `sca-iban`, or `sca-user` attestation into a Wallet Unit, per the relevant Rulebook.
- **Relying Party (RP)** — the party requesting the SCA presentation for a payment transaction. Depending on the flow (§6), the RP is either the Attestation Provider itself (Issuer-requested flow) or a third party such as a Payee, Merchant, PISP, or TPP (Third-party-requested flow).
- **Payee** — the intended recipient of the payment funds, represented in the `payment` transaction data payload.

> **Note (terminology mapping)**: In OpenID4VP [10] terminology, the RP plays the **Verifier** role and the WU plays the **Wallet** role, consistent with the mapping used in CS-02 [6] §4.

## 5. Protocol Overview

An SCA presentation for a payment proceeds as follows:

1. The RP constructs an OpenID4VP [10] Authorization Request carrying a `transaction_data` object of `type` `urn:eudi:sca:payment:1` and a DCQL query matching one or more of the three in-scope VCTs.
2. The RP is expected to sign the Authorization Request (§7.4.1).
3. The request is delivered to the WU (same-device or cross-device, per CS-02 [6] §6).
4. The WU performs Signed Request Verification (§7.3.3); Disclosure Policy Verification does not apply (§2).
5. The WU validates the `transaction_data.payload` against the `urn:eudi:sca:payment:1` schema referenced in the attestation's `transaction_data_types` metadata.
6. The WU renders the payment confirmation screen, composing the requested attributes, the transactional data, and any UI labels, per the visualisation levels declared in the attestation metadata.
7. The Holder authenticates locally to the WU (contributing to the `amr` categories, §7.3.8) and confirms or denies the transaction.
8. On confirmation, the WU generates a Key Binding JWT per attestation presented (`jti`, `amr`, `response_mode`, `transaction_data_hashes`) and submits the presentation response.
9. The RP validates the response and treats the `jti` accordingly (§7.4.3). The WU can additionally log the transaction locally, per §7.3.11.

## 6. High-level Flows

### 6.1 Issuer-requested Flow

Applicable when the RP is the Attestation Provider itself (the Holder's own ASPSP), using either `sca-user` or `sca-iban`.

> **Note**: `sca-card-dpc` is not used in this flow. Its Rulebook (`rb-sca-card-dpc`) states that "SCA-Card (DPC) is designed for the 3-party model in remote commerce: the credential issuer and the verifier are in different organisations.", which excludes the Issuer-requested case addressed here, where the Attestation Provider and RP are the same organisation.

1. **Request creation**: The ASPSP, acting as RP, creates an Authorization Request for `urn:eudi:sca:payment:1`, targeting a single attestation: either an `sca-iban` attestation (identifying the account being debited) or an `sca-user` attestation, used where the account context for the payment is already established out-of-band — e.g. within the ASPSP's own online/mobile banking session — and the SCA Attestation serves solely as the second authentication factor.
2. **Invocation**: Same as CS-02 [6] §6.1.1–6.1.2 (same-device) or §6.2.1–6.2.2 (cross-device).
3. **Request authenticity and RP permission**: The WU performs Signed Request Verification on the Authorization Request in all cases (§7.3). Where an `sca-user` attestation is requested, the WU additionally checks the `aud` claim, which the Attestation Provider sets to the ASPSP's own RP identifier (§7.2.3), to confirm the request originates from the issuing ASPSP; this is the only attestation-level RP-permission check available in this flow. Where an `sca-iban` attestation is requested instead, no equivalent permission check is available, since `aud` restriction is not evaluated for `sca-iban` in payment use (per the `rb-sca-iban` Rulebook; see also §2).
4. **Validation**: WU validates the `payment` payload as described in §5, steps 5–6.
5. **Consent**: Holder reviews the consent screen for the single presented attestation (account details where `sca-iban` is used, or a User-level confirmation only where `sca-user` is used) and confirms.
6. **Generation**: WU generates a single KB-JWT for the presented attestation.
7. **Submission and outcome**: Same as CS-02 [6] §6.1.6–6.1.7. The ASPSP validates the KB-JWT and proceeds with payment execution.

> **Note**: Because combined presentation is out of scope (§2) and the `login_risk_transaction` type is out of scope, an `sca-user` attestation presented alone for a `payment` transaction relies on the account/card context being established outside the wallet exchange, e.g. within the ASPSP's own online/mobile banking session, consistent with TS12 [1]'s description of the Issuer-requested flow as resembling "banks' existing authenticator solutions".

### 6.2 Third-party-requested Flow

Applicable when the RP is not the Attestation Provider (e.g. a Merchant, or a TPP performing an embedded SCA flow), typically using `sca-card-dpc` or `sca-iban`.

1. **Request creation**: The third-party RP creates a signed Authorization Request for `urn:eudi:sca:payment:1`, targeting an `sca-card-dpc` or `sca-iban` attestation.
2. **Invocation**: Same as §6.1.2.
3. **Request authenticity**: No Embedded Disclosure Policy applies to either attestation type (§2). No `aud` claim is defined for `sca-card-dpc`; for `sca-iban`, an `aud` claim exists but is not evaluated for payment use regardless of flow (§6.1.3). The WU performs Signed Request Verification (§7.3) as the only check on the request (§7.1.3). Encrypted requests are "RECOMMENDED" per TS12 [1] §3.5 given the sensitivity of payment payloads.
4. **Validation, consent, generation, submission**: Same as §6.1.4–§6.1.7.
5. **Outcome**: The RP validates the response and proceeds with any further messaging required to complete the payment, e.g. Open Banking messaging between the RP (as TPP) and the ASPSP, or card scheme messaging between Merchant, PSP/Acquirer, and card Issuer (`sca-card-dpc`), out of scope (§2).

## 7. Normative Requirements

### 7.1 Common Requirements (Attestation Provider, WU and RP)

1. Implementations **SHALL** restrict `transaction_data.type` to `urn:eudi:sca:payment:1` for all SCA presentations; RPs **SHALL NOT** request, and WUs **MAY** reject, presentations declaring `urn:eudi:sca:login_risk_transaction:1`, `urn:eudi:sca:account_access:1`, or `urn:eudi:sca:emandate:1`.
2. Implementations **SHALL** restrict SCA Attestation processing to the `sca-card-dpc`, `sca-iban`, and `sca-user` types (identified via their `vct` `extends` chain to the base SCA VCT).
3. Implementations **SHALL NOT** treat Signed Request Verification (§7.3.3) as providing RP-permission control; it establishes request authenticity and integrity only.

### 7.2 Attestation Provider Requirements

1. The Attestation Provider **SHALL NOT** embed a disclosure policy in `sca-card-dpc`, `sca-iban`, or `sca-user` attestations.
2. The Attestation Provider **SHALL** validate the Wallet Unit's WUA per CS-04 [7] before issuance, and **SHALL** ensure the SCA Attestation's validity does not exceed the WUA's validity period.
3. For `sca-user` attestations, the Attestation Provider **SHALL** set the `aud` claim to its own RP identifier(s), consistent with the two-party-only model defined in the `rb-sca-user` Rulebook.
4. For `sca-card-dpc` and `sca-iban` attestations intended for use in a Third-party-requested flow (§6.2), the Attestation Provider **SHALL NOT** rely on `aud` restriction; no attestation-level RP-permission control applies to these cases (§2).
5. The Attestation Provider **SHALL** declare `transaction_data_types` metadata covering, at minimum, `urn:eudi:sca:payment:1`, and **MAY** omit the other three TS12 [1] §4.3 transaction types.

### 7.3 Wallet Unit Requirements

1. The WU **SHALL** evaluate the SD-JWT VC Type Metadata `category` claim per TS12 [1] §3 to detect SCA Attestations, restricted to the three in-scope types (§7.1.2).
2. The WU **SHALL NOT** perform Disclosure Policy Verification (TS12 [1] §3.1.1) for attestations in scope of this CS.
3. The WU **SHALL** perform Signed Request Verification (TS12 [1] §3.1.2) for every SCA Authorization Request in scope of this CS, regardless of flow. Where the request is signed, the WU **SHALL** verify the signature and certificate, and **SHALL** cease processing and inform the Holder if verification fails. Where the request is not signed, the WU **SHALL** warn the Holder and require explicit confirmation before continuing to process the request.
4. The WU **SHALL** validate `transaction_data.payload` against the `urn:eudi:sca:payment:1` schema declared in the attestation's `transaction_data_types` metadata, per TS12 [1] §3.2, and **SHALL** cease processing on validation failure.
5. The WU **SHALL** render the payment confirmation screen per the visualisation levels declared in the attestation's Claim Metadata, defaulting to level `3` where unset (TS12 [1] §3.3.1–3.3.2).
6. The WU **SHALL** display the `affirmative_action_label` and, if present, `denial_action_label`, `transaction_title`, and `security_hint` UI elements per TS12 [1] §3.3.3.
7. The WU **SHALL NOT** present more than one SCA Attestation, across `sca-card-dpc`, `sca-iban`, and `sca-user`, in response to a single Authorization Request; combined presentation of these types is out of scope (§2).
8. For every KB-JWT generated in an SCA presentation, the WU **SHALL** include a fresh, cryptographically random `jti`, a `response_mode` claim echoing the request's `response_mode`, and an `amr` array containing **at least two** entries from different categories (`knowledge`, `possession`, `inherence`) per TS12 [1] §3.6.
9. The WU **SHALL** support processing of encrypted Authorization Requests per TS12 [1] §3.5 and JAR [11].
10. The WU **MAY** reject any request declaring a transaction type other than `urn:eudi:sca:payment:1` (§7.1.1).
11. The WU **MAY**, for every SCA presentation (successful or not), log at least the `transaction_data.payload.transaction_id`, the `payee.name`, and, where available, the `pisp.legal_name`, consistent with the Transaction Log Inclusion requirement of TS12 [1] §5.3. WE BUILD relaxes this from a mandatory to an optional requirement: Wallet Providers are not required to implement this logging capability to conform to this CS.

### 7.4 Relying Party Requirements

1. The RP **SHOULD** send signed Authorization Requests (JAR [11], OpenID4VP [10] §5) for SCA presentations, consistent with TS12 [1] §3.1.
2. Where the RP is the Attestation Provider (Issuer-requested flow, §6.1) and requests an `sca-user` attestation, the RP **SHALL** ensure its identifier is present in the attestation's `aud` claim, per the `rb-sca-user` Rulebook.
3. The RP **SHALL** treat the `jti` of a validated KB-JWT as the PSD2 Authentication Code for the corresponding transaction.
4. The RP **SHALL** verify that the `amr` array of each validated KB-JWT contains at least two entries from different categories before treating SCA as satisfied.
5. The RP **SHALL** verify presentation and attestation validity (signature, `cnf` key binding, and revocation status where a `status_list` claim is present) before accepting an SCA presentation, and **SHALL** cease the payment process on a negative result.
6. The RP **SHALL NOT** construct an Authorization Request querying for more than one of `sca-card-dpc`, `sca-iban`, or `sca-user` (§2).

## 8. Interface Definitions

### 8.1 SCA Authorization Request

**Direction**: RP (Verifier) to WU (Wallet)
**Method**: OpenID4VP [10] Authorization Request, delivered per CS-02 [6] §8.3/8.4 (same-device / cross-device), **profiled as follows**:

- **Transport**: typically a signed Request Object (JAR [11]) (§7.4.1); an unsigned request is permitted but triggers the Holder confirmation described in §7.3.3. For Third-party-requested flows, encryption is used, which TS12 [1] §3.5 states as "RECOMMENDED" given the sensitivity of payment payloads.
- **DCQL query**: matches exactly one of the following `vct` values (or its issuer-specific `extends` chain) per Authorization Request, consistent with the single-attestation constraint (§2, §7.4.6):
  - `https://webuildconsortium.eu/sca/sca-card-dpc/1.0`
  - `https://webuildconsortium.eu/sca/sca-iban/1.0`
  - `https://webuildconsortium.eu/sca-user/1.0`
- **`transaction_data`** (array, present in every Authorization Request): exactly one entry with:
  - `type`: `urn:eudi:sca:payment:1`
  - `credential_ids`: references exactly one credential ID, corresponding to the single SCA Attestation matched by the DCQL query (§2)
  - `transaction_data_hashes_alg`: as per OpenID4VP [10]
  - `payload`: object per TS12 [1] §4.3.1, restricted in this profile to the fields below

**Example (illustrative, non-normative) `payload`:**

```json
{
  "transaction_id": "9c3b1e2a-6f21-4e2a-9a71-2b7e6a5d1234",
  "payee": {
    "name": "Example Merchant B.V.",
    "id": "NL-KVK-12345678"
  },
  "currency": "EUR",
  "amount": 129.95
}
```

**Error handling**: If the request is unsigned, the WU warns the Holder and requires explicit confirmation before continuing (§7.3.3). If the request is incorrectly signed, or if the requested `transaction_data.type` is not supported by the presented attestation's `transaction_data_types` metadata (the expected outcome where an Attestation Provider has omitted an out-of-scope type per §7.2.5), the WU ceases processing and informs the Holder with an appropriate error message (§7.3.3–7.3.4). Independently, the WU may reject a request declaring a `transaction_data.type` other than `urn:eudi:sca:payment:1` even where the presented attestation's metadata still supports it (§7.1.1, §7.3.10).

### 8.2 SCA Authorization Response

**Direction**: WU (Wallet) to RP (Verifier)
**Method**: OpenID4VP [10] Authorization Response, per CS-02 [6] §8.3/8.4, carrying exactly one Key Binding JWT, for the single SCA Attestation presented (§2).

**Response (KB-JWT claims)**:
- `aud`, `nonce`, `sd_hash` — per OpenID4VP [10] / SD-JWT-VC [9]
- `iat` — issuance time of the KB-JWT
- `jti` — fresh, unique per presentation (§7.3.8); RP treatment per §7.4.3
- `response_mode` — echoes the request's `response_mode`
- `amr` — per §7.3.8
- `transaction_data_hashes`, `transaction_data_hashes_alg` — binding to the presented `payment` payload

**Example (illustrative, non-normative) decoded KB-JWT:**

```json
{
  "iat": 1798540123,
  "aud": "x509_san_dns:merchant.example.com",
  "nonce": "3f8c1e2a-9b4d-4e7a-8c1a-2d5e7f9a0b3c",
  "sd_hash": "s0me_base64url_hash_of_the_disclosed_sd_jwt",
  "jti": "7a1e4c2b-5f6d-4a3b-9c8e-1d2f3a4b5c6d",
  "response_mode": "direct_post.jwt",
  "amr": ["pin", "face"],
  "transaction_data_hashes": ["b3JpZ2luYWxfcGF5bG9hZF9oYXNo"],
  "transaction_data_hashes_alg": "sha-256"
}
```

**Error handling**: RPs reject responses where the `amr` array fails the §7.4.4 check, where `transaction_data_hashes` does not match the originally sent payload, or where attestation/status-list validation (§7.4.5) fails.

## 9. Conformance

An implementation **conforms to this specification as an Attestation Provider** if it:

1. Issues `sca-card-dpc`, `sca-iban`, and/or `sca-user` attestations for SCA purposes without an embedded disclosure policy (§7.2).
2. Validates the Wallet Unit's WUA prior to issuance, per CS-04 [7] (§7.2).
3. Applies the `aud`-restriction rules of §7.2 appropriate to each attestation type.

An implementation **conforms to this specification as a Wallet Unit** if it:

1. Restricts SCA processing to the `sca-card-dpc`, `sca-iban`, and `sca-user` attestation types and the `urn:eudi:sca:payment:1` transaction type (§2, §7.1).
2. Implements Signed Request Verification for all in-scope SCA presentations and does not implement or require Disclosure Policy Verification for these attestation types (§7.3).
3. Implements transaction data discovery, validation, and rendering per §5–6 and §7.3.
4. Generates Key Binding JWTs meeting the `jti`, `amr`, `response_mode`, and `transaction_data_hashes` requirements of §7.3.
5. Never presents more than one SCA Attestation, across `sca-card-dpc`, `sca-iban`, and `sca-user`, in response to a single Authorization Request (§7.3.7).

An implementation **conforms to this specification as a Relying Party** if it:

1. Issues only `urn:eudi:sca:payment:1` transaction data requests for SCA presentations (§7.1).
2. Sends signed Authorization Requests for SCA presentations wherever practicable, consistent with §7.4.
3. Treats the KB-JWT `jti` per the requirements of §7.4.
4. Constructs Authorization Requests querying for at most one of `sca-card-dpc`, `sca-iban`, or `sca-user` per request (§7.4).

This CS does not itself constitute conformance to TS12 [1]; an implementation conforming to this CS conforms to the subset of TS12 [1] described in §2, and may additionally implement the out-of-scope features of TS12 [1] without ceasing to conform to this CS, provided the requirements above are met for the in-scope subset.

## References

[1] TS12: European Commission (2026) *TS12 – Electronic Payments SCA Implementation with the Wallet*. eudi-doc-standards-and-technical-specifications. Available at: https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/blob/main/docs/technical-specifications/ts12-electronic-payments-SCA-implementation-with-wallet.md (Accessed: 26 August 2026).

[2] Rulebooks Catalog: WE BUILD Consortium (2026) *Attestation Rulebooks Catalog – rb-sca-card-dpc, rb-sca-iban, rb-sca-user*. Available at: https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks (Accessed: 26 August 2026).

[3] ADR-2: WE BUILD Consortium (2026) *ADR-2: Baseline Protocols*. wp4-architecture. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/base-protocols.md (Accessed: 26 August 2026).

[4] ADR-3: WE BUILD Consortium (2026) *ADR-3: Specify PID and eAA Formats*. wp4-architecture. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/document-formats.md (Accessed: 26 August 2026).

[5] CS-01: WE BUILD Consortium (2026) *CS-01: Credential Issuance*. wp4-architecture. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/cs-01-credential-issuance.md (Accessed: 26 August 2026).

[6] CS-02: WE BUILD Consortium (2026) *CS-02: Credential Presentation*. wp4-architecture. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/cs-02-credential-presentation.md (Accessed: 26 August 2026).

[7] CS-04: WE BUILD Consortium (2026) *CS-04: Individual Wallet Unit Attestation (WUA) Lifecycle*. wp4-architecture. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/cs-04-wua-lifecycle.md (Accessed: 26 August 2026).

[8] PSD2: European Parliament and Council (2015) *Directive (EU) 2015/2366 on payment services in the internal market (PSD2)*. Available at: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32015L2366 (Accessed: 26 August 2026).

[9] SD-JWT-VC: IETF OAuth Working Group (2026) *SD-JWT-based Verifiable Digital Credentials (SD-JWT VC), draft-ietf-oauth-sd-jwt-vc*. Available at: https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/ (Accessed: 26 August 2026).

[10] OpenID4VP: OpenID Foundation (2025) *OpenID for Verifiable Presentations 1.0*. Available at: https://openid.net/specs/openid-4-verifiable-presentations-1_0.html (Accessed: 26 August 2026).

[11] JAR: IETF (2021) *RFC 9101: The OAuth 2.0 Authorization Framework: JWT-Secured Authorization Request (JAR)*. Available at: https://datatracker.ietf.org/doc/html/rfc9101 (Accessed: 26 August 2026).

[12] ADR-21: WE BUILD Consortium (2026) *ADR-21: Pre-flight CS*. wp4-architecture. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/pre-flight-CS.md (Accessed: 28 August 2026).
