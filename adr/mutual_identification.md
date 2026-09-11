# Mutual identification for European Business Wallet presentation requests

**Authors/Contributors:**

- Florin Coptil, Bosch, Germany
- Werner Folkendt, Bosch, Germany
- Lal Chandran, iGrant.io, Sweden
- George J Padayatti, iGrant.io, Sweden
- Eelco Klaver, Credenco, The Netherlands
- <Please add more .. >

**Obsoletes:** N/A

## Context

An EBW in the Holder role stores attestations that its owner treats as confidential, such as ultimate beneficial ownership and control structure. In the BU use cases, requests arrive backend to backend with no person present. The Holder EBW must decide alone, so it needs three answers a machine can check:

1. Which legal entity is asking?
2. Is the requesting software a real wallet unit, and is it still valid?
3. Does the owner's policy allow this entity to receive this attestation?

The proposed Regulation on the establishment of European Business Wallets, COM(2025) 838 final of 19 November 2025, addresses this in its Annex. Point 14(2)(b) states that "where Business Wallet owners use their Business Wallets unit to interact with competent national authorities and providers of electronic attestations of attributes, Wallet units shall enable authentication and validation of the Wallet unit components by presenting the Wallet unit attestations to those competent national authorities and providers upon their request".

Point 14 covers the issuance direction, and CS-01 already implements it. The proposal places no equivalent obligation on a party that requests attestations from a Wallet unit. That gap is what this decision fills.

**We already solve this for issuance.** In CS-01, a Wallet Unit proves what it is before an Issuer releases anything:

- it authenticates with an attestation, the WIA, per OpenID4VCI Appendix E, sent with its Proof-of-Possession (CS-01 section 7.4)
- the attestation is bound to the key used in the transaction, through `cnf` (CS-01 section 7.4)
- `client_id` equals the `sub` claim of the attestation (CS-01 sections 7.3 and 7.4)
- the attestation is checked against the Trusted List for Wallet Providers (CS-01 section 7.4)
- revocation is checked, and re-checked later (CS-01 section 7.5, CS-04 section 7.2)

**In presentation, this rule applies in one direction only.** CS-02 section 7.2, item 6 requires the Verifier to validate the Holder's Wallet Unit Attestation. Nothing requires the Verifier to prove the same about itself. Today it is identified only as the party that signed the request (CS-02 sections 5 and 8.2). The request carries no EBWOID and no BWUA.

The requester already holds both. An EBW is a single wallet unit that plays the Holder, Issuer, and Verifier roles ([BWUA based on TS3](bwua-ts3-attestation.md), CS-02 chapter 4). Nothing new has to be issued to it. What is missing is an agreed way to present what it already holds.

**Two places can carry this material.**

| | `verifier_attestation` Prefix, OpenID4VP 5.9.3 and 12 | `verifier_info`, OpenID4VP 5.11 |
| --- | --- | --- |
| Link to the request | The attestation contains the Verifier's public key (`cnf`). The request signature proves the sender holds the matching private key, so the attestation cannot be copied into another party's request. This is the method CS-01 section 7.4 already uses | We must define this link ourselves. Without it, an entry can be copied into another party's request |
| Relation to CS-02 | Already an allowed scheme, section 5 | Not used today |
| Identity carriers per request | One | Two, checked alongside `client_id` |

Legal entities that run an EUDI Relying Party component hold neither an EBWOID nor a BWUA. Making a parameter mandatory for all requests would exclude them from all traffic, including data that the KYC and PA3 use cases depend on and that is not confidential. The reverse also holds: an EBW may itself request attestations from an EUDI Wallet, and in that direction the EUDI ecosystem's own relying party rules apply.

## Decision

This decision changes nothing in OpenID4VP, nothing in the CS-02 request and response flows, and nothing in the attestations defined in CS-04 and CS-05. It prescribes, for EBW-to-EBW traffic, which already-standard Client Identifier Prefix an EBW uses, and it introduces one new artefact, the EBW Verifier Attestation, which reuses the wallet unit identifier and status mechanism defined in CS-05 and is expected to be specified alongside it. A wallet that implements OpenID4VP section 5.9.3 today processes these requests without modification.

**1. Apply the same rule in both directions, using the issuance method.** WE BUILD defines the EBW Verifier Attestation, a profile of the OpenID4VP Verifier Attestation JWT (section 12), presented with the `verifier_attestation` Client Identifier Prefix (section 5.9.3), which CS-02 section 5 already allows. It is a single JWT, placed in the `jwt` JOSE header of the request object as section 5.9.3 requires. It MUST contain:

- the EBWOID of the legal entity operating the requesting wallet unit
- the wallet unit identifier and the status reference of the requesting wallet unit, as defined for the BWUA in CS-05, so that the Holder can check validity and revocation without resolving a second artefact
- a `cnf` claim whose key signs the Presentation Request Object, so that the signature proves the sender holds that key
- `sub` equal to the `client_id` in the request object

The EBW Verifier Attestation is issued and signed by the Wallet Provider of the requesting wallet unit and is validated against the Trusted List for Wallet Providers, as CS-01 section 7.4 does for the WIA. The Wallet Provider verifies the EBWOID binding at onboarding and asserts it in the attestation; the EBWOID provider is not the trust anchor. The BWUA artefact itself is neither embedded nor fetched: the Wallet Provider signs both the BWUA and the EBW Verifier Attestation, so the attestation restates the same facts under the same signature and the same trust path.

**2. An EBW acting as Verifier MUST include its EBW Verifier Attestation in every Presentation Request addressed to another EBW, or requesting an attestation type governed by an EBW rulebook.** An EBW always holds an EBWOID and a BWUA, so it can always comply. An attestation rulebook MAY declare that a given attestation type MUST NOT be released unless the request carries a valid EBW Verifier Attestation, and an owner MAY apply stricter rules for its own wallet. A valid attestation does not by itself give a right to a response.

**This obligation does not apply to interactions with EUDI Wallets.** An EBW can also act as Verifier towards an EUDI Wallet, for example to request a PID or an attestation from a natural person. In that direction the EBW follows the rules of the EUDI ecosystem, using the Client Identifier Prefix it mandates, in practice `x509_san_dns` with a Relying Party access certificate. Nothing in this decision requires an EUDI Wallet to support the `verifier_attestation` prefix or to trust EBW attestation providers.

Verifiers that are not EBWs are not excluded in the other direction either. Their requests carry no EBW Verifier Attestation, and the Holder decides what to release under Decision 3, using the Client Identifier Schemes CS-02 section 5 already allows.

**3. One place where policy is decided.** The validated attestation is an input to the automatic approval list from [EBW EAA exchange automation](EBW-EAA-exchange-automation.md), not a second gate in front of it. Where the owner approved a requester and attestation combination in advance, that approval is the Holder's consent for CS-02 section 7.1, and the wallet unit MUST record the release and show it to the owner. Otherwise it MUST ask the owner or reject.


### What this decision does not change

| Area | Already decided in |
| --- | --- |
| Protocols | [Baseline protocols](base-protocols.md) |
| OpenID4VP request and response processing | OpenID4VP 1.0, used as published; only the choice of Client Identifier Prefix and the content of the attestation JWT are profiled |
| Signed requests, `client_id`, allowed schemes, nonce, audience, expiry | CS-02 sections 5, 6.1.1, 6.1.3, 8.2 |
| Attestation structure, validity, revocation, binding | CS-04 for the WUA, CS-05 for the BWUA, both authoritative |
| Trust lists | [Trusted lists](trusted-lists.md), applied in CS-01 section 7.4 |
| What a Verifier checks in a response | CS-02 section 7.2, item 6 |

## Consequences

### What becomes easier?

A Holder EBW can identify the requesting entity and check that its wallet unit is sound and not revoked, using material the requester already holds and a verification path its implementation already runs for issuance. Owners can accept requests they refuse today.

Requests can be answered without a person present, which is a precondition for using the EBW inside internal systems. Consent is given once, by the owner, in a list the owner controls.

There is one identity carrier, one binding rule, one trust path and one revocation path, in both directions. Testing extends what exists instead of adding a second surface.

### What becomes more difficult?

Wallet Providers must issue an EBW Verifier Attestation for each wallet unit and keep its revocation status in step with the BWUA: the provider MUST revoke the EBW Verifier Attestation whenever it revokes the corresponding BWUA, or issue it short lived so that alignment happens by expiry. Where a customer runs only a Relying Party component, the provider must decide whether to give it EBW-bound material.

Owners must decide which attestations are confidential. Classification will vary until common practice develops.

Requesters without EBW-bound material will not receive confidential attestations. For KYC and PA3 this must be explained before participants design their integration.

### How do we address the risks introduced by this change?

Wallet Providers can enable a Relying Party component to hold and present an EBW Verifier Attestation, for example by supplying the holder component with the verifier service.

The pre-flight specification should publish a default classification for the BU1 attestation types, so owners start from a common baseline.

If the Architecture Group decides that the Client Identifier layer cannot carry this material, the same requirements can be written in the `verifier_info` format: authentication stays at the Client Identifier layer, using the prefix the target ecosystem supports, and the EBWOID and wallet unit claims travel in `verifier_info` under a WE BUILD profile that defines the binding to the request signature. Decision 1 then changes, Decisions 2 and 3 stand, and the profile must additionally define the link between the entry and the request that section 12 provides by default.

## Advice

Once merged, this is our consortium's decision. This does not mean all participants agree it is the best possible decision. In the decision-making process, we have heard the following advice.

- All authors / Contributors
- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
