# EBWOID Carrier Independence

**Authors:**

- Leif Johansson, SIROS, Sweden

## Context

[rb-ebwoid v1.0.0](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/blob/main/rulebooks/rb-ebwoid/README.md) defines EBWOID's claims (§2), its SD-JWT VC / W3C VCDM encoding (§3), its eIDAS Trust List trust model (§5), and its Token Status List revocation mechanism (§6). All of it is written for one direction of use: a Wallet User presenting their own EBWOID to an Issuer or Relying Party, e.g. during onboarding or wallet activation (rb-ebwoid v1.0.0 §4.1).

It does not address the direction [PR #205](https://github.com/webuild-consortium/wp4-architecture/pull/205) needs: an EBW acting as Relying Party presenting its own EBWOID to another EBW's Wallet User, as part of a mutual-identification handshake for non-interactive, backend-to-backend requests for non-public data. That PR proposes a new `verifierInfo`-carried attestation for this purpose. This introduces a second, undefined attestation-carrying mechanism for something the EU has already standardised: [ETSI TS 119 475](https://www.etsi.org/deliver/etsi_ts/119400_119499/119475/01.01.01_60/ts_119475v010101p.pdf) defines Wallet-Relying-Party Registration and Access Certificates (WRPRC/WRPAC) specifically for a Relying Party to prove its authorisations, entitlements, and intended purposes to a wallet.

Separately, [bwua-ts3-attestation.md](bwua-ts3-attestation.md) records that Business Wallet Unit Attestation (BWUA)'s organisational identity dimension has "EBWOID carried as a claim." Read next to rb-ebwoid v1.0.0 §4.1, which documents EBWOID as presented atomically and standalone, and referenced by `id` from other attestations rather than duplicated into them, it is unclear whether EBWOID's claims are meant to be embedded inside BWUA or only referenced by it. If both readings are implemented, `legal_name` (which can change) risks holding two independent, potentially diverging copies.

## Decision

Treat EBWOID as the claim set rb-ebwoid v1.0.0 §2 already defines, with one or more named, registered carriers, rather than as a single fixed credential type:

1. Name the SD-JWT VC encoding rb-ebwoid v1.0.0 §3.2 already defines as carrier `ebwoid+sdjwtvc`, and the W3C VCDM encoding it already permits as `ebwoid+w3cvcdm`. Neither changes.
2. Register a new carrier, `ebwoid+wrprc`, for the Relying-Party-side direction: the EBWOID `id` and `legal_name` carried or referenced within an ETSI TS 119 475 WRPRC/WRPAC, issued and revoked through that certificate's existing lifecycle rather than a new one. This gives PR #205's mutual-identification requirement a concrete mechanism without a new attestation type, and without depending on OID4VP's `verifier_info` parameter, which the base specification defines as optional and ignorable by the Wallet.
3. Ask WP4 to explicitly resolve the composition question raised above: either EBWOID remains standalone and BWUA references it by `id` only, or BWUA embeds EBWOID's current claims and rb-ebwoid v1.0.0 §4.1 is amended to document BWUA as a valid carrier. This ADR does not choose between them — only that one should be chosen and stated, rather than left to differ by which document an implementer reads.
4. Reserve, but do not require, a carrier identifier `ebwoid+federation` for a possible future OpenID Federation-based carrier, should EBW trust infrastructure adopt Federation separately. No such infrastructure exists today, and this ADR does not propose building it.

## Consequences

What becomes easier?

1. PR #205's mutual-identification requirement gets a concrete mechanism, reusing an ETSI standard already designed for a Relying Party proving itself to a wallet, instead of an underspecified new attestation object.
2. rb-ebwoid v1.0.0's claims, encoding, trust model, and revocation mechanism require no changes to support this.
3. Additional carriers can be registered later, if the ecosystem's trust infrastructure changes, without revisiting this decision or rb-ebwoid v1.0.0.

What becomes more difficult?

1. Implementers need to know which carrier(s) a given interaction expects, rather than assuming EBWOID always arrives as an SD-JWT VC.
2. WP4 must explicitly resolve the EBWOID/BWUA composition question rather than leaving it to differ between rb-ebwoid v1.0.0 and bwua-ts3-attestation.md.
3. EBW owners may not be able to hide whether they internally use an EBW or another WRP component.
4. In this approach, the WRPRAC/WRPRC becomes an EAA, so a single provider becomes responsible for meeting EAA Provider requirements as well as WRPRAC/WRPRC Provider requirements.

How do we address the risks introduced by this change?

- Each carrier is required to convey the same mandatory EBWOID attributes unchanged, bind them to a verifiable issuer, and support a revocation/status check — so accepting a new carrier does not weaken what a Relying Party or Wallet User can rely on, only how it is delivered.
- Until WP4 resolves the BWUA composition question, implementations SHOULD treat rb-ebwoid v1.0.0 §4.1 as authoritative (EBWOID standalone, referenced by `id`) to avoid two independently-editable copies of the same legal-identity claim.

## Advice

Once merged, this is our consortium's decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.
