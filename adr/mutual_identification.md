# Mutual identification for European Business Wallet presentation requests

**Authors/Contributors:**

- Florin Coptil, Bosch, Germany
- Werner Folkendt, Bosch, Germany
- Lal Chandran, iGrant.io, Sweden
- George J Padayatti, iGrant.io, Sweden
- Eelco Klaver, Credenco, The Netherlands
- Leif Johansson, SIROS Foundation, Sweden
- Niels Klomp, Sphereon, The Netherlands
- <Please add more .. >

**Obsoletes:** N/A

## Context

An EBW in the Holder role stores attestations that its owner treats as confidential, such as ultimate beneficial ownership and control structure. In the BU use cases, requests arrive backend to backend with no person present. The Holder EBW must decide alone, so it needs three answers a machine can check:

1. Which legal entity is asking?
2. Is the requesting software a real wallet unit, and is it still valid?
3. Does the owner's policy allow this entity to receive this attestation?

The proposed Regulation on the establishment of European Business Wallets, COM(2025) 838 final of 19 November 2025, addresses this in its Annex. Point 14(2)(b) states that "where Business Wallet owners use their Business Wallets unit to interact with competent national authorities and providers of electronic attestations of attributes, Wallet units shall enable authentication and validation of the Wallet unit components by presenting the Wallet unit attestations to those competent national authorities and providers upon their request".

Point 14 covers the issuance direction, and CS-01 already implements it. The proposal places no equivalent obligation on a party that requests attestations from a Wallet unit. That gap is what this decision fills.

**We already solve this for issuance.** In CS-01, a Wallet Unit proves what it is before an Issuer releases anything: it authenticates with an attestation bound to the key used in the transaction, the attestation is checked against the Trusted List for Wallet Providers, and revocation is checked (CS-01 sections 7.3 to 7.5, CS-04 section 7.2).

**In presentation, the rule applies in one direction only.** CS-02 section 7.2, item 6 requires the Verifier to validate the Holder's Wallet Unit Attestation. Nothing requires the Verifier to identify the legal entity behind it, or to show that it is itself a valid wallet unit. The request carries no EBWOID and no BWUA.

The requester already holds both. An EBW is a single wallet unit that plays the Holder, Issuer and Verifier roles ([BWUA based on TS3](bwua-ts3-attestation.md), CS-02 chapter 4). Nothing new has to be issued to it. What is missing is an agreed way to present what it already holds.

### Where this material travels

Commission Implementing Regulation (EU) 2026/1731 of 15 July 2026 amends Implementing Regulations (EU) 2024/2977, 2024/2979, 2024/2980 and 2024/2982 as regards applicable standards. Its Annex XII, added as Annex II to 2024/2982, states that "the technical specifications in clauses 4.1, 4.2, 5, and 6 of ETSI TS 119 472-2 V1.2.1 (2026-03), shall apply with the following adaptations, including the insertion of a new clause 4.3".

Two requirements of that specification are relevant here:

> OIDFVP-HAIP-COMMON-REQ-01: The Authorization Request shall use the Client Identifier Prefix `x509_hash`.
> OIDFVP-HAIP-COMMON-REQ-RO-01: The RO JWT body shall contain the `verifier_info` parameter.

So for presentations to EUDI Wallets, `verifier_info` is the mandatory channel for Relying Party identity, and the Client Identifier Prefix is fixed. These obligations apply to EUDI Wallets and to relying parties requesting from them.

**Two things they do not settle.** First, the profile identifies the relying party but does not establish that the requester is a valid wallet unit, which is question 2 above. Second, EBW-to-EBW traffic is not within the scope of those acts. The Business Wallet Regulation is still in negotiation: the Council agreed its position on 9 June 2026, recital 4 of the Commission proposal states that the eIDAS specifications "should apply, with the specifications laid down in this Regulation taking precedence in the event of any inconsistency", and recitals 20 and 28 foresee Business-Wallet-specific technical specifications. Producing evidence for those specifications is a purpose of this pilot.

## Decision

This decision changes nothing in OpenID4VP, nothing in the CS-02 request and response flows, and nothing in the attestations defined in CS-04 and CS-05. It defines two WE BUILD `verifier_info` formats, states how they are bound to the request and validated, and separates that content from the choice of Client Identifier Prefix.

### 1. The requesting EBW identifies itself in `verifier_info`

An EBW acting as Verifier includes two elements in the `verifier_info` array of the Request Object, in addition to the elements ETSI TS 119 472-2 already requires:

| `format` | Content | Answers |
| --- | --- | --- |
| `ebwoid` | An EBWOID presentation, as defined in rb-ebwoid, with its Key Binding JWT | Which legal entity is asking |
| `ebw_wallet_unit` | A BWUA presentation, as defined in CS-05, with its Key Binding JWT, carrying the wallet unit identifier and its status reference | Whether the requester is a valid, unrevoked wallet unit |

Neither element contains the `credential_ids` member, following OIDFVP-HAIP-COMMON-REQ-RO-03 and RO-14. Both are key-bound presentations, so the Holder can tell them apart by `format` without inspecting the payload.

Example (illustrative values):

```json
"verifier_info": [
  { "format": "registrar_dataset",  "data": "…" },
  { "format": "ebwoid",             "data": "<EBWOID~disclosures~KB-JWT(nonce, aud)>" },
  { "format": "ebw_wallet_unit",    "data": "<BWUA~KB-JWT(nonce, aud)>" }
]
```

**2. Binding.** The Key Binding JWT of each presentation shall contain:

- `nonce`: the `nonce` of the Presentation Request, which gives freshness;
- `aud`: the `client_id` of the Presentation Request, which ties the presentation to the requesting party and prevents it being copied into another party's request.

A Holder EBW that uses these elements shall verify both values, as OpenID4VP section 5.11 requires the Wallet to "validate the signature and ensure binding".

**3. Validation.** For each element the Holder EBW shall verify the issuer's signature and the validity of the presentation, then check revocation:

- the EBWOID presentation according to rb-ebwoid, with the issuer validated against the eIDAS Trusted List;
- the BWUA presentation according to CS-05, with the Wallet Provider validated against the Trusted List for Wallet Providers, as CS-01 section 7.4 already does for issuance.

If either check fails, the request is refused. Unknown or unsupported `verifier_info` elements are ignored, as OpenID4VP already provides.

### 2. The formats are independent of the Client Identifier Prefix

The content defined above is carried in the Request Object body and remains valid under any Client Identifier Prefix. This decision therefore separates the two questions:

- **Towards EUDI Wallets**, an EBW acting as Verifier uses the `x509_hash` prefix, as ETSI TS 119 472-2 clause 6 requires through Annex II of Implementing Regulation (EU) 2024/2982. Nothing in this decision changes that direction, and no EUDI Wallet is required to recognise the WE BUILD formats.
- **Business Wallet-Native Model (Certificate-Free)**: The requester authenticates by proving possession of its core identity credential. In this model, the Request Object MUST be signed by the private key corresponding to the signing_key attested within the EBWOID itself. This path eliminates the need for any external Access Certificate.

**No certificate obligation is created for EBW-to-EBW traffic by this decision.** Only `x509_hash` requires the requester to hold an X.509 wallet-relying party access certificate, issued under Implementing Regulation (EU) 2025/848, together with registration in an RP registrar. Nothing in the acts currently in force applies that requirement to requests between two Business Wallets. The pilot shall implement and measure at least one certificate-based and one certificate-free option, and report the operational cost of each, so that the choice for the Business Wallet specifications rests on evidence.

### 3. When the elements are required

An EBW acting as Verifier shall include both elements in every Presentation Request addressed to another EBW, or requesting an attestation type governed by an EBW rulebook. An EBW always holds an EBWOID and a BWUA, so it can always comply. An attestation rulebook MAY declare that a given attestation type shall not be released unless the request carries both valid elements, and an owner MAY apply stricter rules for its own wallet. Valid elements do not by themselves give a right to a response.

**This obligation does not apply to interactions with EUDI Wallets.** In that direction the EBW sends the `verifier_info` elements ETSI TS 119 472-2 requires and nothing further.

Verifiers that are not EBWs are not excluded in the other direction either. Their requests carry neither element, and the Holder decides what to release under Decision 4.

### 4. One place where policy is decided

The validated elements are inputs to the automatic approval list from [EBW EAA exchange automation](EBW-EAA-exchange-automation.md), not a second gate in front of it. The list is keyed on the EBWOID and the attestation type. Where the owner approved a requester and attestation combination in advance, that approval is the Holder's consent for CS-02 section 7.1, and the wallet unit shall record the release and show it to the owner. Otherwise it shall ask the owner or reject. The choice of Client Identifier Prefix does not affect this list.

### Processing summary for the receiving EBW

| Step | Check | Depends on the prefix? |
| --- | --- | --- |
| 1 | Client authentication, as the chosen prefix defines | Yes |
| 2 | `ebwoid` element: issuer signature, validity, revocation, eIDAS Trusted List | No |
| 3 | `ebw_wallet_unit` element: issuer signature, validity, status, Trusted List for Wallet Providers | No |
| 4 | Key Binding JWT of each element: `nonce` and `aud` match the request | No |
| 5 | Owner's approval list, keyed on the EBWOID, then release and log, or ask the owner | No |

### What this decision does not change

| Area | Already decided in |
| --- | --- |
| Client Identifier Prefix, Request Object structure and mandatory `verifier_info` content towards EUDI Wallets | ETSI TS 119 472-2 V1.2.1 clause 6, applied by CIR (EU) 2026/1731 Annex XII |
| Protocols | [Baseline protocols](base-protocols.md) |
| OpenID4VP request and response processing | OpenID4VP 1.0, used as published |
| EBWOID claims, encoding, trust model, revocation | rb-ebwoid, authoritative |
| Attestation structure, validity, revocation, binding | CS-04 for the WUA, CS-05 for the BWUA, both authoritative |
| Trust lists | [Trusted lists](trusted-lists.md), applied in CS-01 section 7.4 |
| What a Verifier checks in a response | CS-02 section 7.2, item 6 |

## Consequences

### What becomes easier?

A Holder EBW can identify the requesting legal entity and check that its wallet unit is sound and not revoked, using credentials the requester already holds and verification paths its implementation already runs. Owners can accept requests they refuse today.

Requests can be answered without a person present, which is a precondition for using the EBW inside internal systems. Consent is given once, by the owner, in a list the owner controls.

The material travels in the parameter the EUDI profile already mandates, so an implementation that meets ETSI TS 119 472-2 adds two array elements on the sending side and two validation routines on the receiving side. Nothing new has to be issued, and no verifier-side attestation has to be kept in step with the BWUA.

Because the formats are independent of the Client Identifier Prefix, the pilot can test more than one prefix without changing the payload, and the decision survives whatever the Business Wallet specifications settle on.

### What becomes more difficult?

Wallet Providers and EBWOID issuers must support presentation of these credentials by an EBW acting in the Verifier role, including key binding to a request the EBW itself creates.

Owners must decide which attestations are confidential. Classification will vary until common practice develops.

Requesters without an EBWOID and a BWUA will not receive confidential attestations. For KYC and PA3 this must be explained before participants design their integration.

Running two prefixes during the pilot costs implementation effort on the Holder side. This is deliberate, so that the cost of each option is measured rather than assumed.

### Open items this decision depends on

1. **EBWOID revocation** is not yet fully specified in rb-ebwoid. Decision 1 depends on a revocation check.
2. **Status checking for the BWUA presentation** in the Verifier direction must be confirmed against CS-05, including what a Holder does when the status cannot be checked.
3. **Registrar data in EBW-to-EBW traffic.** OIDFVP-HAIP-COMMON-REQ-RO-02 requires `verifier_info` to carry RP Registrar-provided data. Whether an EBW acting as Verifier towards another EBW registers with an RP Registrar, or whether the two WE BUILD elements stand in its place for that traffic, must be decided explicitly.
4. **Backend-to-backend transport for a Presentation Request** is not defined in CS-02, whose invocation flows assume a person. This blocks the BU use cases independently of this decision.
5. **CS-02 section 7.1 forbids auto-consent**, while [EBW EAA exchange automation](EBW-EAA-exchange-automation.md) requires sharing without human approval for M2M scenarios. Decision 4 treats a prior owner approval as consent; the conflict between those documents predates this decision.
6. **Format identifier registration.** The values `ebwoid` and `ebw_wallet_unit` should be recorded wherever WE BUILD registers Verifier Info format identifiers, so that they do not collide with a future ETSI or OpenID Foundation registration.

### How do we address the risks introduced by this change?

The pre-flight specification should publish a default classification for the BU1 attestation types, so owners start from a common baseline.

WE BUILD should report to ETSI and to the Commission that the current presentation profile conveys relying party identity but not wallet unit validity, and that EBW-to-EBW traffic needs an explicit answer on the Client Identifier Prefix and on relying party registration. The pilot's measurements from Decision 2 are the evidence for that report.

## References

- Commission Implementing Regulation (EU) 2026/1731 of 15 July 2026, Annex XII, added as Annex II to Implementing Regulation (EU) 2024/2982
- ETSI TS 119 472-2 V1.2.1 (2026-03), clause 6
- Commission Implementing Regulation (EU) 2025/848 on registration of wallet-relying parties
- [OpenID for Verifiable Presentations 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html), sections 5.9.3 and 5.11
- COM(2025) 838 final, proposal for a Regulation on European Business Wallets, recitals 4, 20 and 28

## Advice

Once merged, this is our consortium's decision. This does not mean all participants agree it is the best possible decision. In the decision-making process, we have heard the following advice.

- All authors / Contributors
- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
