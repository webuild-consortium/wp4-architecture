# Pseudonyms for user accounts

**Authors:**

- Peter Altmann, Digg, SWE

## Context

Pseudonyms are a mandatory wallet function (Article 5a.4(b)) and support various use cases. 
However, CIR 2024/2979 Article 14 only permits WebAuthn-based pseudonyms, which lack key 
properties for some scenarios. While passkeys suffice for standard account recovery, 
some services need to recover accounts while enforcing bans on known offenders.

This requires pseudonyms that are deterministic per identity subject and site-specific, 
allowing services to detect returning banned users without revealing their identity. 
The current WebAuthn-based approach cannot generate stable, site-specific pseudonyms tied to 
the identity subject. Therefore, alternative solutions must be explored.

Prior work proposed a pseudonym seed managed by the PID Provider. Two approaches building on 
this concept were explored for account recovery, each with significant drawbacks. One requires 
introducing a third party to act as the pseudonym generator, which adds complexity and necessitates 
combining attributes from two separate attestations in each presentation. The other derives a fixed 
set of pseudonyms for selective disclosure, which limits how many pseudonyms a user can hold.

A third approach involves equipping the user's EUDIW device with ZKP capabilities. With this, the 
user can prove statements like: "This pseudonym is derived from a seed value in a valid PID and a 
site-specific public input." There are multiple ways to construct such proofs. This ADR is limited to
options that support hardware bound attestations and assumes that the seed resides in a PID.

## Decision

The following changes were agreed upon:

- Investigate methods for deriving stable pseudonyms that are both site-specific and identity-subject-specific.
- Leverage zero-knowledge proofs (ZKPs) to address limitations of approaches based solely on conventional cryptography.
- Focus on account recovery in cases where known offender matching is important.

## Consequences

What becomes easier?

- Enabling enforcement actions such as preventing re-registration by banned users.
- Deriving stable, identity-bound and site-specific pseudonyms without revealing underlying identifiers.
- Avoids new ecosystem actors.

What becomes more difficult?

- Implementing and verifying ZKP-based proofs.
- Updating verifier capabilities within the existing EUDIW ecosystem.
- Requiring PID Providers to include a pseudonym seed.

How do we address the risks introduced by this change?

- Rely on established ZKP tooling to reduce implementation risk.
- Offset added complexity by simplifying other aspects and focusing efforts on the ZKP integration. For instance:
  - Use a simple derivation function like `seed = HMAC(key=secret, msg=personal_number)`
  - Compute the pseudonym as `SHA256(seed || service_id)` 

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
