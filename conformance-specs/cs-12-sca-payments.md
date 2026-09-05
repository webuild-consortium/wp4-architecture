# WE BUILD - Pre-flight Conformance Specification: SCA Attestations for Payment Transactions (TS12 Profile)

Version 0.8 (Draft)
Date: 31 August 2026

**Revision history**

* Version 0.8 (31 August 2026): Made the document an explicit profile of CS-01 and CS-02, aligned the signed-request rule with CS-02, made encrypted request delivery mandatory outside the Digital Credentials API, corrected TS12 and CS-02 section references and the `sca-user` VCT, labelled the requirement sections by lifecycle phase (issuance vs presentation), verified and expanded the examples against TS12, and applied editorial cleanup.
* Version 0.7 (31 August 2026): Initial draft, profiling TS12 [1] for use within WE BUILD.

**Authors / Contributors**:

* Stefan Kauhaus, Visa, Germany
* Nikolaos Triantafyllou, University of Aegean, Greece
* Filip Hladky, BankID, Czech Republic
* Lal Chandran, iGrant.io, Sweden
* George J Padayatti, iGrant.io, Sweden

Table of Contents

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
   - 7.2 [Attestation Provider Requirements (Issuance)](#72-attestation-provider-requirements-issuance)
   - 7.3 [Wallet Unit Requirements (Presentation)](#73-wallet-unit-requirements-presentation)
   - 7.4 [Relying Party Requirements (Presentation)](#74-relying-party-requirements-presentation)
8. [Interface Definitions](#8-interface-definitions)
   - 8.1 [SCA Authorization Request](#81-sca-authorization-request)
   - 8.2 [SCA Authorization Response](#82-sca-authorization-response)
9. [Conformance](#9-conformance)
10. [References](#references)

# 1. Introduction

This document is a **pre-flight conformance specification** as per ADR-21 [12]. It defines the WE BUILD Conformance Specification for SCA Attestations used in payment transactions. It profiles TS12 [1], the European Commission's technical specification for Strong Customer Authentication (SCA) under PSD2 [8] with the EU Digital Identity Wallet, for use between WE BUILD consortium partners in the WP3 (Wallet for Payments) use cases.

**This CS is a profile of CS-01 [5] (Credential Issuance) and CS-02 [6] (Credential Presentation).** SCA Attestations are issued with the OpenID4VCI profile of CS-01 and presented with the OpenID4VP profile of CS-02. This document does not restate the requirements of those specifications. It defines only the SCA-specific additions, and conformance to this CS presupposes conformance to CS-01 and CS-02 (section 9). It also relies on CS-04 [7] for Wallet Unit Attestation (WUA) validity and revocation, which gates the issuance of SCA Attestations.

TS12 [1] is itself a profile of SD-JWT-VC [9] and OpenID4VP [10], consistent with the baseline protocols adopted in ADR-2 [3] and the credential-format decisions in ADR-3 [4]. This CS narrows TS12 [1] further, for WE BUILD purposes only, as follows:

1. **Attestation types**: only the three SCA Attestation types defined in the WE BUILD Attestation Rulebooks Catalog [2] are in scope: `sca-card-dpc`, `sca-iban` and `sca-user`. No other SCA Attestation type is profiled by this CS.
2. **Transaction type**: only the `payment` transaction type (`urn:eudi:sca:payment:1`) is used. The `login_risk_transaction`, `account_access` and `emandate` transaction types of TS12 [1] section 4.3 are out of scope for WE BUILD.
3. **Single-attestation presentation**: only one SCA Attestation is presented to the RP per Authorization Request. Combined presentations across the three in-scope types are not used in WE BUILD.
4. **Embedded Disclosure Policy**: WE BUILD does **not** use the Embedded Disclosure Policy feature of TS12 [1] section 3.1.
5. **Signed requests**: TS12 [1] section 3.1 recommends signed Authorization Requests and permits unsigned requests after a Holder warning. CS-02 [6] requires all Authorization Requests to be signed and requires WUs to reject unsigned requests. This CS follows CS-02: the unsigned-request path of TS12 [1] is not available in WE BUILD (section 7.3, item 3 and section 7.4, item 1).
6. **Encrypted requests**: TS12 [1] section 3.5 only recommends encrypted presentation requests. This CS requires them for every request delivered outside the Digital Credentials API: the RP delivers the Request Object by reference with the POST method, the WU provides its encryption keys in that POST exchange, and the RP sends the Request Object encrypted (section 7.3, item 9 and section 7.4, item 2).

Separately, this CS relaxes one TS12 [1] requirement from a mandatory to an optional level:

1. **Transaction Log Inclusion**: TS12 [1] section 5.3 requires Wallet Units to log defined transaction data for every SCA presentation. This CS treats it as an optional Wallet Unit capability (section 2 and section 7.3, item 11).

This document supports the Interoperability Test Bed (ITB). It does not define the SCA Attestation types, their claims, or their trust and revocation mechanisms. These are defined in the respective Rulebooks (`rb-sca-card-dpc`, `rb-sca-iban`, `rb-sca-user`) in the Rulebooks Catalog [2].

# 2. Scope

This CS defines conformance requirements for **Attestation Providers**, **Wallet Units (WU)** and **Relying Parties (RP)** when an SCA Attestation of type `sca-card-dpc`, `sca-iban` or `sca-user` is presented to authenticate a payment transaction within WE BUILD.

**In scope:**

* Detection and processing of SCA Attestations of the three named types, including their `extends` chain to the base SCA VCT.
* Construction, transmission and validation of a `payment` (`urn:eudi:sca:payment:1`) transaction data object, including Dynamic Linking and consent-screen rendering.
* Signed Request Verification (authenticity and integrity of the Authorization Request) for all in-scope SCA presentations. All requests are signed (section 1, item 5).
* Encrypted delivery of the Authorization Request outside the Digital Credentials API, with POST delivery of the Request Object and WU-provided encryption keys (section 1, item 6).
* The `aud` claim as the only attestation-level RP-permission control available. It applies solely to `sca-user` presentations in the Issuer-requested flow (section 6.1).
* Key Binding JWT (KB-JWT) requirements (`jti`, `amr`, `response_mode`, `transaction_data_hashes`) for SCA presentations.

**Out of scope (deviations from TS12 [1]):**

* **Combined SCA presentations.** Presentation of more than one of the three in-scope SCA Attestation types in a single Authorization Request. Only one of the three in-scope types is presented to the RP at a time. This is a WE BUILD-specific restriction. It is distinct from the Combined Presentation pattern of TS12 [1] section 3.4, which combines one SCA Attestation with non-SCA attestations (for example payment plus age verification, driving licence or loyalty cards). That pattern is not addressed by this CS.
* **Other transaction types.** TS12 [1] section 4.3 defines four built-in transaction types and requires Wallet Units to process and render all of them. Under this profile, WU conformance is assessed only against the `payment` type. Implementers are not required to implement `login_risk_transaction`, `account_access` or `emandate` to conform to this CS.
* **Embedded Disclosure Policy.** WE BUILD Attestation Providers do not embed a disclosure policy in the three in-scope attestation types (section 7.2). Wallet Units are not required to implement the Disclosure Policy Verification step of TS12 [1] section 3.1 for these attestation types.
* **Mandatory Transaction Log Inclusion.** TS12 [1] section 5.3 requires transaction logging at a SHALL level. This profile relaxes it to an optional capability (section 7.3, item 11). Wallet Providers are not required to implement it to conform to this CS.
* **Attestation-level RP-permission control** for `sca-card-dpc`, and for `sca-iban` in the Third-party-requested flow (section 6.2). Because Embedded Disclosure Policy is excluded and no `aud` restriction applies in these cases, this profile has no mechanism that restricts which Relying Parties may request these attestations beyond the authenticity check of Signed Request Verification. A conforming Wallet Unit presents to any Relying Party whose signed request passes Signed Request Verification (section 7.3, item 3).
* **Other SCA Attestation types** than `sca-card-dpc`, `sca-iban` and `sca-user`.
* **mdoc encodings.** ISO/IEC 18013-5 (mdoc) encodings of `sca-iban` and `sca-user`. The respective Rulebooks define mdoc namespaces, but TS12 [1] itself is scoped to SD-JWT-VC [9].
* **Payment rails.** SCA Attestation registration binding, Open Banking and PSD2 interbank messaging between TPPs and ASPSPs, and account information services generally. These are out of scope of TS12 [1] itself and remain out of scope here.
* **WUA issuance and revocation mechanics.** These are defined in CS-04 [7] and are referenced here only as an issuance precondition.
* **Delivery over the Digital Credentials API.** Presentation via the Digital Credentials API is specified in CS-07 [13]. The transport requirements of this CS (section 7.3, item 9 and section 7.4, items 1 and 2) apply to the `openid4vp://` delivery of CS-02 [6].

# 3. Normative Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY** and **OPTIONAL** in this document are to be interpreted as described in RFC 2119 and RFC 8174, only when they appear in all capitals.

# 4. Roles and Components

* **Wallet Unit (WU):** the EUDI Wallet software and hardware combination that holds and presents SCA Attestations on behalf of the Holder.
* **Holder / Payment Service User (PSU):** the natural person who controls the Wallet Unit and completes SCA for a payment.
* **Attestation Provider (ASPSP / Issuer):** the payment service provider that issues an `sca-card-dpc`, `sca-iban` or `sca-user` attestation into a Wallet Unit, per the relevant Rulebook.
* **Relying Party (RP):** the party that requests the SCA presentation for a payment transaction. Depending on the flow (section 6), the RP is either the Attestation Provider itself (Issuer-requested flow) or a third party such as a Payee, Merchant, PISP or TPP (Third-party-requested flow).
* **Payee:** the intended recipient of the payment funds, represented in the `payment` transaction data payload.

> **Note (terminology mapping)**: In OpenID4VP [10] terminology, the RP plays the **Verifier** role and the WU plays the **Wallet** role, consistent with the mapping used in CS-02 [6] section 4.

# 5. Protocol Overview

An SCA presentation is a CS-02 [6] presentation with SCA-specific additions from TS12 [1]. The base flow (request creation, invocation, validation, consent, generation, submission, result handling) is defined in CS-02 [6] sections 5 and 6 and is not restated here. This CS adds the following on top of it:

1. The Authorization Request carries a `transaction_data` object of type `urn:eudi:sca:payment:1`, and its DCQL query matches exactly one of the three in-scope VCTs (section 8.1).
2. During validation, the WU performs Signed Request Verification (section 7.3, item 3) and validates the `transaction_data.payload` against the `urn:eudi:sca:payment:1` schema referenced in the attestation's `transaction_data_types` metadata (section 7.3, item 4). Disclosure Policy Verification does not apply (section 2).
3. The consent screen becomes a payment confirmation screen. The WU composes the requested attributes, the transactional data and the UI labels, per the visualisation levels declared in the attestation metadata (section 7.3, items 5 and 6).
4. The Holder authenticates locally to the WU with at least two factors from different categories, which the WU records in the `amr` claim (section 7.3, item 8).
5. The KB-JWT carries the additional claims `jti`, `amr`, `response_mode` and `transaction_data_hashes` (section 7.3, item 8 and section 8.2). The RP treats the `jti` as the PSD2 Authentication Code (section 7.4, item 4).
6. The WU can log the transaction locally (section 7.3, item 11).

# 6. High-level Flows

Both flows in this chapter are **presentation** flows; they differ only in who acts as the RP. There is no SCA-specific issuance flow: an Attestation Provider issues `sca-card-dpc`, `sca-iban` and `sca-user` attestations with the standard issuance flows of CS-01 [5], subject to the issuance-time requirements of section 7.2, with the claims and formats defined in the Rulebooks [2].

## 6.1 Issuer-requested Flow

Applicable when the RP is the Attestation Provider itself (the Holder's own ASPSP), using either `sca-user` or `sca-iban` (for `sca-card-dpc`, see the note below).

> **Note**: Despite its name, this is a presentation flow, not an issuance flow. The name follows TS12 [1]: the issuing ASPSP acts as the RP and requests a presentation of an attestation that it issued earlier.

> **Note**: The Rulebooks [2] govern which attestation types are available in each flow. The `rb-sca-card-dpc` Rulebook currently describes SCA-Card (DPC) for the 3-party model in remote commerce, where the credential issuer and the verifier are different organisations, which excludes the Issuer-requested case. Where a revision of that Rulebook permits use with the Attestation Provider and the RP in the same organisation, `sca-card-dpc` can also be used in this flow; the Rulebook is authoritative.

1. **Request creation**: The ASPSP, acting as RP, creates a signed Authorization Request for `urn:eudi:sca:payment:1` that targets a single attestation. It targets an `sca-iban` attestation to identify the account being debited, or an `sca-user` attestation where the account context is already established out of band (for example within the ASPSP's own online or mobile banking session) and the SCA Attestation serves only as the second authentication factor.
2. **Invocation**: Same as CS-02 [6] sections 6.1.1 to 6.1.2 (same-device) or 6.2.1 to 6.2.2 (cross-device).
3. **Request authenticity and RP permission**: The WU performs Signed Request Verification on the Authorization Request in all cases (section 7.3, item 3). Where an `sca-user` attestation is requested, the WU additionally checks the `aud` claim, which the Attestation Provider sets to the ASPSP's own RP identifier (section 7.2, item 3), to confirm that the request originates from the issuing ASPSP. This is the only attestation-level RP-permission check available in this flow. Where an `sca-iban` attestation is requested, no equivalent permission check is available, because `aud` restriction is not evaluated for `sca-iban` in payment use (per the `rb-sca-iban` Rulebook; see also section 2).
4. **Validation**: The WU validates the `payment` payload (section 7.3, items 4 to 6).
5. **Consent**: The Holder reviews the consent screen for the single presented attestation (account details for `sca-iban`, or a User-level confirmation only for `sca-user`) and confirms.
6. **Generation**: The WU generates a single KB-JWT for the presented attestation (section 7.3, item 8).
7. **Submission and outcome**: Same as CS-02 [6] sections 6.1.6 to 6.1.7. The ASPSP validates the KB-JWT and proceeds with payment execution.

> **Note**: Combined presentation is out of scope (section 2) and the `login_risk_transaction` type is out of scope. An `sca-user` attestation presented alone for a `payment` transaction therefore relies on the account or card context being established outside the wallet exchange, for example within the ASPSP's own online or mobile banking session. This is consistent with the description in TS12 [1] of the Issuer-requested flow as resembling banks' existing authenticator solutions.

## 6.2 Third-party-requested Flow

Applicable when the RP is not the Attestation Provider (for example a Merchant, or a TPP performing an embedded SCA flow), typically using `sca-card-dpc` or `sca-iban`.

1. **Request creation**: The third-party RP creates a signed and encrypted Authorization Request for `urn:eudi:sca:payment:1` that targets an `sca-card-dpc` or `sca-iban` attestation (section 7.4, items 1 and 2).
2. **Invocation**: Same as section 6.1, step 2.
3. **Request authenticity**: The WU performs Signed Request Verification (section 7.3, item 3) as the only check on the request (section 7.1, item 3). No Embedded Disclosure Policy applies to either attestation type (section 2). No `aud` claim is defined for `sca-card-dpc`. For `sca-iban`, an `aud` claim exists but is not evaluated for payment use, regardless of flow (section 6.1, step 3).
4. **Validation, consent, generation, submission**: Same as section 6.1, steps 4 to 7.
5. **Outcome**: The RP validates the response and proceeds with any further messaging required to complete the payment, for example Open Banking messaging between the RP (as TPP) and the ASPSP, or card scheme messaging between Merchant, PSP or Acquirer and card Issuer (`sca-card-dpc`). This messaging is out of scope (section 2).

# 7. Normative Requirements

The requirements below are additions on top of CS-01 [5] (issuance) and CS-02 [6] (presentation). The base requirements of those specifications continue to apply and are not restated.

## 7.1 Common Requirements (Attestation Provider, WU and RP)

1. Implementations **SHALL** restrict `transaction_data.type` to `urn:eudi:sca:payment:1` for all SCA presentations. RPs **SHALL NOT** request, and WUs **MAY** reject, presentations declaring `urn:eudi:sca:login_risk_transaction:1`, `urn:eudi:sca:account_access:1` or `urn:eudi:sca:emandate:1`.
2. Implementations **SHALL** restrict SCA Attestation processing to the `sca-card-dpc`, `sca-iban` and `sca-user` types, identified via their `vct` `extends` chain to the base SCA VCT.
3. Implementations **SHALL NOT** treat Signed Request Verification (section 7.3, item 3) as providing RP-permission control. It establishes request authenticity and integrity only.

## 7.2 Attestation Provider Requirements (Issuance)

All requirements in this section apply at issuance time. The Attestation Provider issues SCA Attestations as an Issuer under CS-01 [5]. In addition, the Attestation Provider:

1. **SHALL NOT** embed a disclosure policy in `sca-card-dpc`, `sca-iban` or `sca-user` attestations.
2. **SHALL** validate the Wallet Unit's WUA per CS-04 [7] before issuance, and **SHALL** ensure that the SCA Attestation's validity period does not exceed the WUA's validity period (TS12 [1] section 5.1).
3. **SHALL**, for `sca-user` attestations, set the `aud` claim to its own RP identifier(s), consistent with the two-party-only model defined in the `rb-sca-user` Rulebook.
4. **SHALL NOT** rely on `aud` restriction for `sca-card-dpc` and `sca-iban` attestations intended for use in a Third-party-requested flow (section 6.2). No attestation-level RP-permission control applies to these cases (section 2).
5. **SHALL** declare `transaction_data_types` metadata covering, at minimum, `urn:eudi:sca:payment:1`, and **MAY** omit the other three transaction types of TS12 [1] section 4.3.

**Example (illustrative, non-normative) VC Type Metadata** for an `sca-iban` attestation, showing the SCA-specific parameters of TS12 [1] sections 2.3, 3.3.3 and 4.1 and the VCT hierarchy of the `rb-sca-iban` Rulebook [2]:

```json
{
  "vct": "https://issuer.bank.example/credentials/sca/iban/1.0",
  "name": "Example Bank SCA-IBAN Attestation",
  "extends": "https://webuildconsortium.eu/sca/sca-iban/1.0",
  "category": "urn:eu:europa:ec:eudi:sua:sca",
  "transaction_data_types": {
    "urn:eudi:sca:payment:1": {
      "schema": "urn:eudi:sca:payment:1",
      "claims": [
        {
          "path": ["payload", "amount"],
          "visualisation": 1,
          "display": [
            {
              "lang": "en-GB",
              "label": "Amount",
              "description": "Amount of the payment"
            }
          ]
        },
        {
          "path": ["payload", "payee", "name"],
          "visualisation": 1,
          "display": [
            {
              "lang": "en-GB",
              "label": "Payee",
              "description": "Recipient of the payment"
            }
          ]
        }
      ],
      "ui_labels": {
        "affirmative_action_label": [
          { "lang": "en", "value": "Confirm Payment" }
        ],
        "denial_action_label": [
          { "lang": "en", "value": "Cancel Payment" }
        ]
      }
    }
  }
}
```

In this profile, the key of each `transaction_data_types` entry is the transaction type itself (`urn:eudi:sca:payment:1`), so the value that the RP sends as `transaction_data.type` is also the key that the WU looks up (TS12 [1] section 3.2).

## 7.3 Wallet Unit Requirements (Presentation)

All requirements in this section apply at presentation time. The WU obtains SCA Attestations under CS-01 [5] and presents them under CS-02 [6]. In addition, the WU:

1. **SHALL** evaluate the SD-JWT VC Type Metadata `category` claim per TS12 [1] section 3 to detect SCA Attestations, restricted to the three in-scope types (section 7.1, item 2).
2. **SHALL NOT** perform Disclosure Policy Verification (TS12 [1] section 3.1) for attestations in scope of this CS.
3. **SHALL** perform Signed Request Verification (TS12 [1] section 3.1) for every SCA Authorization Request, regardless of flow: verify the signature and certificate, and cease processing and inform the Holder if the verification fails. The WU **SHALL** reject unsigned requests, as required by CS-02 [6] section 7.1. The unsigned-request path of TS12 [1] section 3.1 (warn the User and continue on confirmation) **SHALL NOT** be used.
4. **SHALL** validate `transaction_data.payload` against the `urn:eudi:sca:payment:1` schema declared in the attestation's `transaction_data_types` metadata, per TS12 [1] section 3.2, and **SHALL** cease processing on validation failure.
5. **SHALL** render the payment confirmation screen per the visualisation levels declared in the attestation's Claim Metadata, defaulting to level `3` where unset (TS12 [1] sections 3.3.1 to 3.3.2).
6. **SHALL** display the `affirmative_action_label` and, if present, the `denial_action_label`, `transaction_title` and `security_hint` UI elements per TS12 [1] section 3.3.3.
7. **SHALL NOT** present more than one SCA Attestation, across `sca-card-dpc`, `sca-iban` and `sca-user`, in response to a single Authorization Request. Combined presentation of these types is out of scope (section 2).
8. **SHALL** include the following in every KB-JWT generated in an SCA presentation, per TS12 [1] section 3.6 and OpenID4VP [10]:
   * a fresh, cryptographically random `jti`, unique per presentation;
   * a `response_mode` claim that echoes the request's `response_mode`;
   * an `amr` array with **at least two** entries from different categories (`knowledge`, `possession`, `inherence`), where each entry is an object that pairs the category with the specific method used, for example `{"knowledge": "pin_6_or_more_digits"}`;
   * `transaction_data_hashes`, calculated over the presented `transaction_data`, together with the `transaction_data_hashes_alg` that identifies the algorithm used.
9. **SHALL** support processing of encrypted Authorization Requests per TS12 [1] section 3.5 and JAR [11]. For requests delivered outside the Digital Credentials API, the WU **SHALL** support POST delivery of the Request Object (`request_uri_method` `post`, OpenID4VP [10] section 5.10), **SHALL** provide its encryption keys to the RP in the `wallet_metadata` of that POST exchange, and **SHALL** reject unencrypted requests.
10. **MAY** reject any request declaring a transaction type other than `urn:eudi:sca:payment:1` (section 7.1, item 1).
11. **MAY**, for every SCA presentation (successful or not), log at least the `transaction_data.payload.transaction_id`, the `payee.name` and, where available, the `pisp.legal_name`, consistent with the Transaction Log Inclusion requirement of TS12 [1] section 5.3. WE BUILD relaxes this from a mandatory to an optional requirement: Wallet Providers are not required to implement this logging capability to conform to this CS.

## 7.4 Relying Party Requirements (Presentation)

All requirements in this section apply at presentation time. The RP acts as a Verifier under CS-02 [6]. In addition, the RP:

1. **SHALL** send signed Authorization Requests (JAR [11], OpenID4VP [10] section 5) for SCA presentations, as required by CS-02 [6] sections 5 and 7.2. This CS tightens TS12 [1] section 3.1, which recommends signing (section 1, item 5).
2. **SHALL**, for requests delivered outside the Digital Credentials API (the `openid4vp://` flows of CS-02 [6] section 6), deliver the Authorization Request by reference with `request_uri_method` `post` (OpenID4VP [10] section 5.10), obtain the WU's encryption keys from the `wallet_metadata` that the WU sends in that POST exchange, and send the Request Object encrypted (JAR [11]). This CS tightens TS12 [1] section 3.5, which recommends encryption (section 1, item 6).
3. **SHALL**, where the RP is the Attestation Provider (Issuer-requested flow, section 6.1) and requests an `sca-user` attestation, ensure that its identifier is present in the attestation's `aud` claim, per the `rb-sca-user` Rulebook.
4. **SHALL** treat the `jti` of a validated KB-JWT as the PSD2 Authentication Code for the corresponding transaction.
5. **SHALL** verify that the `amr` array of each validated KB-JWT contains at least two entries from different categories before treating SCA as satisfied.
6. **SHALL** validate the presentation and the attestation per CS-02 [6] section 7.2, including revocation status where a `status_list` claim is present, **SHALL** recompute and verify `transaction_data_hashes` against the exact `transaction_data` sent in the Authorization Request, and **SHALL** cease the payment process on a negative result (TS12 [1] section 5.2).
7. **SHALL NOT** construct an Authorization Request querying for more than one of `sca-card-dpc`, `sca-iban` or `sca-user` (section 2).

# 8. Interface Definitions

## 8.1 SCA Authorization Request

**Direction**: RP (Verifier) to WU (Wallet)
**Method**: OpenID4VP [10] Authorization Request, delivered per CS-02 [6] sections 8.1 (Wallet invocation) and 8.2 (Presentation Request Object), in the same-device or cross-device flow of CS-02 [6] section 6, **profiled as follows**:

* **Transport**: a signed Request Object (JAR [11]) is REQUIRED (section 7.4, item 1). Outside the Digital Credentials API, the Request Object is delivered by reference with `request_uri_method` `post` and is encrypted with the keys that the WU provides in the `wallet_metadata` of the POST exchange (section 7.4, item 2). This tightens TS12 [1] section 3.5, which recommends encryption.
* **DCQL query**: matches exactly one of the following `vct` values (or its issuer-specific `extends` chain) per Authorization Request, consistent with the single-attestation constraint (section 2 and section 7.4, item 7):
  - `https://webuildconsortium.eu/sca/sca-card-dpc/1.0`
  - `https://webuildconsortium.eu/sca/sca-iban/1.0`
  - `https://webuildconsortium.eu/sca/sca-user/1.0`
* **`transaction_data`** (array, present in every Authorization Request): exactly one entry with:
  - `type`: `urn:eudi:sca:payment:1`
  - `credential_ids`: references exactly one credential ID, corresponding to the single SCA Attestation matched by the DCQL query (section 2)
  - `transaction_data_hashes_alg`: REQUIRED, consistent with TS12 [1] section 4.2; values and processing as defined by OpenID4VP [10]
  - `payload`: REQUIRED, object per TS12 [1] section 4.3.1. All payload fields of TS12 [1] section 4.3.1 remain available, including the OPTIONAL `pisp`, `execution_date` and `recurrence` elements. The example below shows the REQUIRED fields only.

**Example (illustrative, non-normative) DCQL query** for an `sca-iban` presentation:

```json
{
  "credentials": [
    {
      "id": "sca_iban",
      "format": "dc+sd-jwt",
      "meta": {
        "vct_values": ["https://webuildconsortium.eu/sca/sca-iban/1.0"]
      }
    }
  ]
}
```

**Example (illustrative, non-normative) `transaction_data` entry**, shown decoded. Per OpenID4VP [10], each entry is base64url-encoded in the request, and the `credential_ids` value references the `id` of the DCQL query above:

```json
{
  "type": "urn:eudi:sca:payment:1",
  "credential_ids": ["sca_iban"],
  "transaction_data_hashes_alg": "sha-256",
  "payload": {
    "transaction_id": "9c3b1e2a-6f21-4e2a-9a71-2b7e6a5d1234",
    "payee": {
      "name": "Example Merchant B.V.",
      "id": "NL-KVK-12345678"
    },
    "currency": "EUR",
    "amount": 129.95
  }
}
```

**Error handling**: If the request is unsigned or incorrectly signed, the WU rejects it (section 7.3, item 3). If the requested `transaction_data.type` is not supported by the presented attestation's `transaction_data_types` metadata (the expected outcome where an Attestation Provider has omitted an out-of-scope type per section 7.2, item 5), the WU ceases processing and informs the Holder with an appropriate error message (section 7.3, items 3 and 4). Independently, the WU may reject a request declaring a `transaction_data.type` other than `urn:eudi:sca:payment:1` even where the presented attestation's metadata still supports it (section 7.1, item 1; section 7.3, item 10).

## 8.2 SCA Authorization Response

**Direction**: WU (Wallet) to RP (Verifier)
**Method**: OpenID4VP [10] Authorization Response, submitted to the Presentation Response Endpoint per CS-02 [6] section 8.3, carrying exactly one Key Binding JWT for the single SCA Attestation presented (section 2).

**Response (KB-JWT claims)**:

* `aud`, `nonce`, `sd_hash`: per OpenID4VP [10] and SD-JWT-VC [9]
* `iat`: issuance time of the KB-JWT
* `jti`: fresh, unique per presentation (section 7.3, item 8); RP treatment per section 7.4, item 4
* `response_mode`: echoes the request's `response_mode`
* `amr`: per section 7.3, item 8
* `transaction_data_hashes`, `transaction_data_hashes_alg`: binding to the presented `payment` payload

**Example (illustrative, non-normative) decoded KB-JWT**, answering the request of section 8.1. The `transaction_data_hashes` value is the SHA-256 hash of the base64url-encoded `transaction_data` entry of that request:

```json
{
  "aud": "x509_san_dns:merchant.example.com",
  "iat": 1798540123,
  "jti": "7a1e4c2b-5f6d-4a3b-9c8e-1d2f3a4b5c6d",
  "nonce": "wyFUNx18SPErrRrh8nmSdQ",
  "sd_hash": "jhFWI7fYUfiZ1FXTvRf5nCXTPj5cP2m3GHpg6FqFH1E",
  "response_mode": "direct_post.jwt",
  "amr": [
    { "knowledge": "pin_6_or_more_digits" },
    { "inherence": "face_device" }
  ],
  "transaction_data_hashes": [
    "8_u-RlUj2xBzhmjl8ZfLxP1B_eUkqhAGvx7GIPQMCQY"
  ],
  "transaction_data_hashes_alg": "sha-256"
}
```

> **Note**: TS12 [1] section 3.6 defines `response_mode` as REQUIRED in the KB-JWT; the non-normative example in TS12 [1] omits it. This CS follows the normative text and includes it.

**Error handling**: RPs reject responses where the `amr` array fails the check in section 7.4, item 5, where `transaction_data_hashes` does not match the originally sent payload, or where attestation or status-list validation (section 7.4, item 6) fails.

# 9. Conformance

Conformance to this CS presupposes conformance to the base specifications: CS-01 [5] as an Issuer or Wallet Provider, and CS-02 [6] as a Verifier or Wallet Provider, for the respective role.

An implementation **conforms to this specification as an Attestation Provider** if it:

1. Conforms to CS-01 [5] as an Issuer.
2. Issues `sca-card-dpc`, `sca-iban` and/or `sca-user` attestations for SCA purposes without an embedded disclosure policy (section 7.2).
3. Validates the Wallet Unit's WUA prior to issuance, per CS-04 [7], and caps the attestation validity at the WUA validity (section 7.2).
4. Applies the `aud`-restriction rules of section 7.2 appropriate to each attestation type.

An implementation **conforms to this specification as a Wallet Unit** if it:

1. Conforms to CS-01 [5] and CS-02 [6] as a Wallet Provider.
2. Restricts SCA processing to the `sca-card-dpc`, `sca-iban` and `sca-user` attestation types and the `urn:eudi:sca:payment:1` transaction type (sections 2 and 7.1).
3. Implements Signed Request Verification for all in-scope SCA presentations, rejects unsigned requests and, outside the Digital Credentials API, unencrypted requests, and does not implement or require Disclosure Policy Verification for these attestation types (section 7.3).
4. Implements transaction data discovery, validation and rendering per sections 5, 6 and 7.3.
5. Generates Key Binding JWTs meeting the `jti`, `amr`, `response_mode` and `transaction_data_hashes` requirements of section 7.3.
6. Never presents more than one SCA Attestation, across `sca-card-dpc`, `sca-iban` and `sca-user`, in response to a single Authorization Request (section 7.3, item 7).

An implementation **conforms to this specification as a Relying Party** if it:

1. Conforms to CS-02 [6] as a Verifier.
2. Issues only `urn:eudi:sca:payment:1` transaction data requests for SCA presentations (section 7.1).
3. Sends signed Authorization Requests for all SCA presentations and, outside the Digital Credentials API, delivers them encrypted with POST delivery of the Request Object (section 7.4).
4. Treats the KB-JWT `jti` per the requirements of section 7.4.
5. Constructs Authorization Requests querying for at most one of `sca-card-dpc`, `sca-iban` or `sca-user` per request (section 7.4).

This CS does not itself constitute conformance to TS12 [1]. An implementation conforming to this CS conforms to the subset of TS12 [1] described in section 2, and may additionally implement the out-of-scope features of TS12 [1] without ceasing to conform to this CS, provided the requirements above are met for the in-scope subset.

# References

[1] TS12: European Commission (2026) *TS12 - Electronic Payments SCA Implementation with the Wallet*. eudi-doc-standards-and-technical-specifications. Available at: https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/blob/main/docs/technical-specifications/ts12-electronic-payments-SCA-implementation-with-wallet.md (Accessed: 26 August 2026).

[2] Rulebooks Catalog: WE BUILD Consortium (2026) *Attestation Rulebooks Catalog - rb-sca-card-dpc, rb-sca-iban, rb-sca-user*. Available at: https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks (Accessed: 26 August 2026).

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

[13] CS-07: WE BUILD Consortium (2026) *CS-07: Credential Presentation and Issuance via the Digital Credentials API*. wp4-architecture. Available at: https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/cs-07-credential-presentation-dc-api.md (Accessed: 31 August 2026).
