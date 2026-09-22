# Verify EAA issuer key binding via an AuthZEN API call

**Authors:**

- Leif Johansson, SIROS, Sweden
- Malin Norlander, Bolagsverket, Sweden

## Context

[#168](https://github.com/webuild-consortium/wp4-architecture/pull/168) asks how a validator can confirm that the key which signed an EAA is bound to the legal person identified by the issuer's EBWOID, without requiring every EAA Provider to be registered in a national Trusted List (TLoL). Both options it proposes solve this by making the binding statically verifiable offline:

- Option 1 puts the EBW owner's public key inside the EBWOID itself and chains the EBWOID into every EAA header.
- Option 2 has the EBWOID provider issue a parallel x.509 "issuing/sealing" certificate, chained into every EAA header instead.

Both options require changes to the EBWOID's ETSI-based format, to SD-JWT VC and to HAIP (or an equivalent business-wallet document) so that every attestation format can carry the chained data, and both re-raise the TLoL scaling threat #168 itself names: a copy of the TLoL, or the header data it protects, may be too large to hold reliably on constrained wallets in embedded devices. Revocation is also harder this way: #168 asks EBWOID providers to support revocation requests carrying a past timestamp, precisely because the binding is asserted once, statically, and consumed long after.

A validator is not always offline when it checks this binding. [flo0x/wp4-architecture#1](https://github.com/flo0x/wp4-architecture/pull/1) proposes that two EBWs identify each other by reciprocally presenting their own EBWOIDs during a request. A validator built this way already holds the counterparty's EBWOID and already has a live network path open to it at the moment it needs to check a signing key. The EBWOID itself is issued by each Member State's company registration office (e.g. Bolagsverket in Sweden), which is the authority best placed to answer, in real time, "is this key currently bound to this legal person?" — because it is the same authority that would otherwise be asked to chain that fact statically into the EBWOID.

[AuthZEN](https://openid.net/wg/authzen/) is an OpenID Foundation working group standard for exactly this shape of question: a validator (the AuthZEN Policy Enforcement Point) sends a `{subject, resource, action, context}` access evaluation request over HTTPS to a Policy Decision Point, and gets back a decision. Using it here avoids inventing a bespoke chaining protocol per attestation format.

## Decision

An EAA issuer's key binding to its EBWOID MAY be verified by the validator calling an AuthZEN access evaluation endpoint operated by (or on behalf of) the registration office that issued that EBWOID, instead of by chaining a public key or certificate into the EAA header.

1. From the presented EAA, the validator extracts the issuer's EBWOID unique identifier (EUID) and the identifier of the key that signed the EAA (its JWK thumbprint per RFC 7638).
2. The validator resolves the AuthZEN Policy Decision Point endpoint for the issuing registration office through an EU directory service. This is a distinct lookup from the [Digital Directory Lookup Service](ebw-endpoint-lookup-service.md), which resolves a Wallet Unit's credential offer endpoint; here the directory is keyed by issuing authority (e.g. by EUID country prefix), not by Wallet Unit. Whether this reuses the existing EU Business Registers Interconnection System (BRIS), extends the Digital Directory, or is a new registry is an open item for the PID/EBWOID group to decide.
3. The validator sends an AuthZEN access evaluation request to that endpoint:
   - `subject`: the signing key, identified by its JWK thumbprint.
   - `resource`: the legal person, identified by the EBWOID's EUID.
   - `action`: `bind_key`, or an equivalently named action scoped to this question.
   - `context`: MAY carry the EAA's issuer-identifying claims for audit, but the decision MUST NOT depend on anything the validator cannot itself already assert.
4. A `true` decision from the EBWOID's own issuing authority is sufficient evidence that the signing key is bound to the legal person; no public key or certificate needs to be chained into the EAA, the EBWOID or its provider's header, and no change to the EBWOID's ETSI format, to SD-JWT VC or to HAIP is required for this purpose.
5. Validators MAY cache a `true` decision for a bounded time-to-live to avoid a live call per EAA. A `false` decision or an unreachable endpoint MUST be handled per the validator's own trust policy; fail-closed is RECOMMENDED wherever the EAA is being relied on at the same assurance level as a QEAA.
6. This is independent of, and does not replace, Wallet Unit Attestation validation under CS-02 §7.2 item 6; it answers a different question — whether the *signing key* is bound to the *legal person* — that #168 raises and this ADR proposes to answer live rather than by chaining.

## Consequences

What becomes easier?

- No changes are needed to the EBWOID's ETSI format, to SD-JWT VC or to HAIP to carry chained key or certificate data — the entire multi-standard change surface #168 requires for both of its options is avoided.
- No new x.509 "issuing/sealing" certificate type is introduced, and no trust anchor is needed beyond the registration office that already issues the EBWOID.
- Constrained wallets no longer need to fetch, store or verify a TLoL, or a chain rooted in it, to check this one binding — removing the "TLoL too big for embedded/mobile devices" threat #168 names.
- Key rotation and revocation are answered live, from the registration office's current record, at the moment of verification — removing the need to design a retroactive-timestamp revocation mechanism, or to re-issue the EBWOID on every key rotation.
- The mechanism is a direct application of AuthZEN, an existing OpenID standard for access/binding decisions, rather than a bespoke chaining scheme invented per attestation format.

What becomes more difficult?

- This breaks pure offline, holder-to-holder verification: the validator needs live reachability to the issuing registration office (or its delegate) at the moment it verifies. #168's own example — a long-lived, non-revocable EAA (e.g. a diploma) verified after the issuing EAA Provider, or even its EBWOID provider's endpoint, no longer exists — is not solved by this ADR, and this ADR does not claim to solve it.
- The EU directory mapping a registration office (or EUID prefix) to its AuthZEN endpoint does not exist yet in this form. It is a different lookup from the Wallet Unit-keyed Digital Directory Lookup Service, and needs its own design or an explicit extension of that one.
- Every Member State's company registration office would need to expose and operate an AuthZEN Policy Decision Point. Rolling this out consistently across roughly thirty registration offices of varying technical maturity is its own scaling problem, not obviously smaller than the standards changes #168 requires.
- The `subject`/`resource`/`action` vocabulary for this check must mean the same thing everywhere it is deployed; if registration offices diverge in how they interpret it, validators cannot rely on a `true` decision meaning the same thing across Member States.

How do we address the risks introduced by this change?

- Scope this ADR to the live-verification case only. The archival case — verifying a long-lived EAA after its issuing chain is no longer reachable — remains #168's problem to solve (by chaining or otherwise) and should stay a separate, explicit decision rather than be folded into this one.
- Bound the cache TTL for `true` decisions to the issuing registration office's stated revocation SLA, to reduce round-trip cost on repeat or warm relationships.
- Treat the AuthZEN endpoint directory as an extension of the Digital Directory Lookup Service concept, keyed by issuing authority instead of Wallet Unit, rather than inventing a second, unrelated directory.
- Pilot with a small number of registration offices (starting with Bolagsverket) and a fixed `bind_key` action definition before asking all Member States to adopt it.

## Advice

Once merged, this is our consortium's decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
