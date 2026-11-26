# WE BUILD - Pre-flight Conformance Specification CS-019: W3C VCDM Credentials for Data Spaces

Version 0.1 / Pre-flight Draft
Date: 2026-11-25

**Revision history**

* Version 0.1 (2026-11-25): First draft for review by SC2, Spherity, WP4 Wallet Providers and WP4 Testing.

**Authors / Contributors**: WP4 Architecture

* Sarah Amandusson, Digg
* <Reviewers from SC2 / Spherity / Wallet Providers / Testing>

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [Normative Language](#3-normative-language)
4. [Roles and Components](#4-roles-and-components)
5. [Protocol Overview](#5-protocol-overview)
6. [High-level Flows](#6-high-level-flows)
7. [Normative Requirements](#7-normative-requirements)
8. [Interface Definitions](#8-interface-definitions)
9. [Open Topics for Testing Feedback](#9-open-topics-for-testing-feedback)
10. [Conformance](#10-conformance)
* [References](#references)

# 1. Introduction

Use case SC2 (Trusted Data Sharing for Data Spaces) issues a Dataspace Membership Credential that one Data Sharing Initiative (DSI) issues and another DSI accepts, so that a company does not have to register again. Data spaces build on ontologies and JSON-LD for semantic interoperability, so SC2 uses the W3C Verifiable Credentials Data Model (VCDM) 2.0 for this credential ([#334](https://github.com/webuild-consortium/wp4-architecture/issues/334), D2.1).

The [Dataspace Membership Credential Rulebook](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-ds-membership) defines the attributes and the JSON-LD encoding, but leaves the securing mechanism open. This specification fixes what is needed to issue, present and test such credentials in the ITB.

W3C VCDM is not a baseline format for the European Business Wallet. It is used only where a use case needs it, as decided in [Baseline protocols, formats and versions](../adr/baseline-protocols-and-versions.md).

# 2. Scope

**In scope**

* Non-qualified EAAs encoded as W3C VCDM 2.0 (JSON-LD), exchanged between European Business Wallets and DSIs in SC2. In the MVP: the Dataspace Membership Credential.
* Issuance with OpenID4VCI and presentation with OpenID4VP, as profiled in CS-01 and CS-02, with the differences set out here.
* Securing mechanism, context handling, revocation and holder binding for these credentials.
* ITB validation of these credentials.

**Out of scope**

* EUDI Wallets. W3C VCDM credentials are never issued to or requested from EUDI Wallets.
* PID, EBWOID, VAT ID and other QEAAs or PuB-EAAs. These remain SD-JWT VC as in CS-01 and CS-02.
* Business wallets not taking part in SC2. They are not required to support this specification.
* Data space trust frameworks (e.g. DSSC, iSHARE, Gaia-X). SC2 MVP relies on the WE BUILD trust infrastructure; a data space trust layer is an MVP+ topic.
* Data usage licences (MVP+).

# 3. Normative Language

The key words "MUST", "MUST NOT", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT" and "MAY" are to be interpreted as described in RFC 2119 and RFC 8174.

# 4. Roles and Components

| Role | Description |
|---|---|
| **Issuer (DSI)** | Data Sharing Initiative that onboards a company and issues the Dataspace Membership Credential. Listed as a non-qualified EAA Provider. |
| **Holder (Business Wallet)** | European Business Wallet of the company. Holds EBWOID and VAT ID as SD-JWT VC, and the membership credential as W3C VCDM. |
| **Verifier (DSI)** | Another DSI that accepts the membership credential to onboard the company without full re-registration. |

# 5. Protocol Overview

| Aspect | CS-01 / CS-02 baseline | This specification |
|---|---|---|
| Credential format | SD-JWT VC | W3C VCDM 2.0, JSON-LD 1.1 |
| Securing | SD-JWT (JOSE) | Data Integrity proof (see 8.4 and 9.1) |
| Selective disclosure | SD-JWT disclosures | Data Integrity selective disclosure cryptosuite (see 8.4 and 9.1) |
| Revocation | Token Status List (CS-10) | See 8.5 and 9.2 |
| Issuance / presentation protocol | OpenID4VCI 1.0 / OpenID4VP 1.0 | Same, with the W3C VC format identifiers (Section 8) |
| Issuer trust | WE BUILD trusted lists | Same: non-qualified EAA Provider list (see 9.3 for key resolution) |

# 6. High-level Flows

## 6.1 Onboarding and issuance (SC2 user story 1)

1. The company starts onboarding at DSI A and accepts the data space governance rulebook.
2. DSI A requests EBWOID and VAT ID from the company's business wallet with OpenID4VP, as in CS-02 (SD-JWT VC).
3. DSI A verifies them and issues the Dataspace Membership Credential to the business wallet with OpenID4VCI, as in CS-01, in the W3C VCDM format defined here.

Steps 2 and 3 can be run as separate protocol runs within OpenID4VCI 1.0. The DSI is then responsible for linking the two runs to the same wallet (e.g. through its session). D2.1 also describes running the presentation inside the issuance flow, using the interactive authorization endpoint of a later OpenID4VCI version, which binds the two cryptographically but goes beyond the WE BUILD baseline (OpenID4VCI 1.0). See 9.6.

## 6.2 Re-use at another DSI (SC2 user stories 2 and 3)

1. The company starts onboarding at DSI B.
2. DSI B requests the Dataspace Membership Credential with OpenID4VP, as in CS-02, in the W3C VCDM format defined here.
3. DSI B verifies the credential (Section 7.3) and onboards the company if its governance rulebook is compatible.

# 7. Normative Requirements

## 7.1 Credential

| ID | Requirement |
|---|---|
| VCDM-01 | The credential MUST conform to W3C VCDM 2.0 [W3C VCDM 2.0] and to the encoding in the applicable rulebook (for the MVP: [RB-DSM], section 5.3). |
| VCDM-02 | The `@context` MUST contain only the pinned contexts listed in Section 8.3, in the stated order. |
| VCDM-03 | The credential MUST declare the types required by the rulebook so that all attributes survive JSON-LD expansion (rulebook section 5.3.1). |
| VCDM-04 | The credential MUST be secured with a Data Integrity proof using the cryptosuite in Section 8.4. |
| VCDM-05 | The credential MUST carry `credentialStatus` as defined in Section 8.5. |
| VCDM-06 | The credential MUST carry `validFrom` and `validUntil`. |

## 7.2 Issuer

| ID | Requirement |
|---|---|
| ISS-01 | The Issuer MUST advertise the credential configuration in its Credential Issuer metadata with the format identifier in Section 8.1. |
| ISS-02 | Before issuance, the Issuer MUST verify the company's EBWOID (and VAT ID where the rulebook requires it) as in CS-02. |
| ISS-03 | The Issuer MUST bind the credential to the holder as defined in Section 8.6. |
| ISS-04 | The Issuer MUST be listed in the applicable WE BUILD trusted list for non-qualified EAA Providers. |

## 7.3 Holder (Business Wallet)

| ID | Requirement |
|---|---|
| HLD-01 | A business wallet taking part in SC2 MUST support both SD-JWT VC (CS-01/CS-02) and the W3C VCDM format defined here. |
| HLD-02 | The wallet MUST store and present the credential without modifying it. |
| HLD-03 | The wallet MUST create the presentation with the proof required in Section 8.2, using the key bound in Section 8.6. |

## 7.4 Verifier

| ID | Requirement |
|---|---|
| VER-01 | The Verifier MUST verify the Data Integrity proof of the credential and of the presentation. |
| VER-02 | The Verifier MUST use the locally pinned contexts in Section 8.3 and MUST NOT fetch contexts at runtime. |
| VER-03 | The Verifier MUST expand the credential and reject it if a required attribute does not survive expansion. |
| VER-04 | The Verifier MUST check revocation status (Section 8.5) and the validity period. |
| VER-05 | The Verifier MUST check that the issuer is listed in the applicable trusted list. |

## 7.5 Unhappy paths

| Case | Result |
|---|---|
| Unknown or modified `@context` | Reject |
| Required attribute dropped on expansion | Reject |
| Proof invalid, issuer not listed, or credential revoked or expired | Reject |
| Revocation status cannot be obtained | Verifier's documented risk decision |

# 8. Interface Definitions

## 8.1 Issuance format identifier

The Credential Issuer metadata and the credential request MUST use the format identifier `ldp_vc` (OpenID4VCI 1.0, Appendix A.1.2: VC secured using Data Integrity, using JSON-LD).

## 8.2 Presentation

The DCQL query MUST use the format `ldp_vc`. The presentation MUST be a W3C Verifiable Presentation secured with a Data Integrity proof that includes the `challenge` (nonce) and `domain` (client identifier) from the request.

*Note to reviewers: please confirm that this matches the W3C VC format profile in OpenID4VP 1.0.*

## 8.3 Pinned contexts

Issuers MUST use, and Verifiers MUST accept, only the JSON-LD contexts listed below, in the exact version given. Verifiers MUST use local copies and MUST NOT fetch contexts at runtime, so that the meaning of a credential cannot change after issuance and verification does not depend on, or reveal anything to, the context host.

| Order | Context | Version / hash |
|---|---|---|
| 1 | `https://www.w3.org/ns/credentials/v2` | <pin> |
| 2 | European Business Wallet Vocabulary context | <URL, pin> |

*Note to reviewers (SC2 / Spherity): please provide the URL and version (or hash) of the European Business Wallet Vocabulary context to pin.*

## 8.4 Securing mechanism

Proposal for review (see 9.1): for the MVP, Data Integrity with `ecdsa-rdfc-2019` (P-256) for full disclosure, and `ecdsa-sd-2023` where selective disclosure is required. `bbs-2023` is a candidate for MVP+.

## 8.5 Revocation

The Dataspace Membership Credential is revocable, so CS-10 applies. CS-10 specifies the IETF Token Status List for SD-JWT VC; for W3C VCDM, the `credentialStatus` mechanism is open (see 9.2):

* **Proposal:** W3C Bitstring Status List, the native mechanism for VCDM.
* **Alternative:** the Token Status List from CS-10, so that one status infrastructure serves both formats. This requires WE BUILD to define how a VCDM credential references it.

Whichever is chosen, the principles of CS-10 apply: 1-bit status entries, herd-privacy-preserving index allocation, caching by Verifiers, and a documented risk decision when status cannot be obtained.

## 8.6 Holder binding

Proposal for review (see 9.4): `credentialSubject.id` is a DID controlled by the business wallet (`did:jwk`), proven with the `di_vp` proof type in the credential request (OpenID4VCI 1.0, Appendix F.2) and in the presentation proof.

# 9. Open Topics for Testing Feedback

## 9.1 Securing mechanism

Proposal: **ECDSA for the MVP; BBS as a candidate for MVP+**, if wallets and DSIs support it.

* **MVP: ECDSA** (`ecdsa-rdfc-2019`, `ecdsa-sd-2023`). Uses the same curve (P-256) as the rest of WE BUILD and the EUDI ecosystem, so existing keys and hardware can be reused, and supports selective disclosure.
* **MVP+: BBS** (`bbs-2023`). Adds zero-knowledge selective disclosure, so that presentations cannot be linked across verifiers. Its standardisation status and the support for its curve (BLS12-381) in wallets and hardware need to be confirmed before it is required.
* **Alternative: VC-JOSE-COSE**, if SC2 wallets cannot support Data Integrity in the MVP timeframe.

Questions to SC2: which of these do the SC2 wallets and DSIs support today? Is ECDSA sufficient for the MVP, with BBS tested in MVP+?

## 9.2 Revocation

Bitstring Status List (W3C), or the Token Status List used in CS-10, to reuse existing infrastructure?

## 9.3 Issuer key resolution and trust

How does a Verifier get from the proof's `verificationMethod` to the issuer's entry in the trusted list (e.g. `did:web` with an X.509 chain, or a certificate reference)?

## 9.4 Holder binding

`did:jwk`, `did:web`, or another mechanism?

## 9.5 ITB validation

Syntax and `@context`, JSON Schema, expansion without dropped claims (SHACL, see the rulebook), proof and key binding. What can the ITB support in the MVP timeframe?

## 9.6 Linking presentation and issuance

Are separate OpenID4VP and OpenID4VCI 1.0 runs, linked by the DSI's session, sufficient for SC2? Or is the interactive authorization endpoint needed? If so, this would be a justified exception to the baseline under the change rules in the ADR "Baseline protocols, formats and versions".

# 10. Conformance

An implementation conforms to this specification for a role if it meets all requirements in Section 7 for that role and the interface definitions in Section 8, as resolved after the open topics in Section 9.

# References

* [W3C VCDM 2.0] W3C Verifiable Credentials Data Model v2.0. https://www.w3.org/TR/vc-data-model-2.0/
* [VC-DI] W3C Verifiable Credential Data Integrity 1.0. https://www.w3.org/TR/vc-data-integrity/
* [VC-DI-ECDSA] W3C Data Integrity ECDSA Cryptosuites v1.0. https://www.w3.org/TR/vc-di-ecdsa/
* [BSL] W3C Bitstring Status List v1.0. https://www.w3.org/TR/vc-bitstring-status-list/
* [JSON-LD 1.1] W3C JSON-LD 1.1. https://www.w3.org/TR/json-ld11/
* [OpenID4VCI] OpenID for Verifiable Credential Issuance 1.0. https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html
* [OpenID4VP] OpenID for Verifiable Presentations 1.0. https://openid.net/specs/openid-4-verifiable-presentations-1_0.html
* [CS-01] WE BUILD WBCS Credential Issuance. [cs-01-credential-issuance.md](cs-01-credential-issuance.md)
* [CS-02] WE BUILD WBCS Credential Presentation. [cs-02-credential-presentation.md](cs-02-credential-presentation.md)
* [RB-DSM] WE BUILD Dataspace Membership Credential Rulebook. https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-ds-membership
* [CS-10] WE BUILD WBCS Attestation Revocation Mechanism. [cs-10-revocation-mechanism.md](cs-10-revocation-mechanism.md)
* [ADR] WE BUILD ADR Baseline protocols, formats and versions. [baseline-protocols-and-versions.md](../adr/baseline-protocols-and-versions.md)
