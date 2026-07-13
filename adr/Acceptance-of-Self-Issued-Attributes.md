# Acceptance of Self-Issued / User-Asserted Attributes

**Authors:**

- Consortium Architecture Working Group AMS Track 4

- Boris Lingl, boris.lingl@datev.de
- Alexander Manecke, a.manecke@telekom.de
- Ignacio Ripoll, ignacio.ripoll@corpme.es
- Iris Speiser, iris.speiser@datev.de
- Marlene Urbschat, marlene.urbschat@datev.de

## Context

The consortium needed to determine whether self-issued/user-asserted attributes are acceptable within the ecosystem.

The acceptability and legal fit of self-issued attestations were unclear. While self-issued attestations offer flexibility and ease of issuance, they do not provide the same level of assurance as electronic attestations of attributes (EAA) or qualified electronic attestations of attributes (QEAA) issued by trusted parties.

The core trade-off is between enabling broad adoption and maintaining a consistently high level of trust across jurisdictions.

## Decision

The consortium will allow the use of self-issued/user-asserted attributes.

However, self-issued attributes shall not be treated as qualified attestations and shall not imply the same level of legal or regulatory assurance.

Relying parties remain responsible for determining whether self-issued attestations are sufficient for their use case and risk profile.

## Consequences

### What becomes easier?

- Faster ecosystem adoption.
- Reduced issuance complexity.
- Lower barriers to participation.
- Increased flexibility for use cases where qualified attestations are not required.

### What becomes more difficult?

- Trust evaluation becomes the responsibility of relying parties.
- Acceptance may vary across jurisdictions.
- Additional policy decisions may be required by service providers.

### How do we address the risks introduced by this change?

- Clearly distinguish self-issued and qualified attestations.
- Define metadata and trust indicators that allow relying parties to assess assurance levels.
- Allow relying parties to reject self-issued attestations where regulatory requirements demand stronger evidence.

## Advice

- 2026-06-11: Consortium Working Group: Self-issued/user-asserted attributes should be supported to maximize ecosystem adoption.
- 2026-06-11: Legal and Compliance Representatives: Self-issued attestations must not be confused with qualified attestations.
- 2026-06-11: Service Providers: Acceptance policies should be based on jurisdictional and risk requirements.
