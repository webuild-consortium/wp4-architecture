# Atomic Granularity for Mandate-Related Attestations

**Authors:**

- Consortium Architecture Working Group AMS Track 4

- Boris Lingl, boris.lingl@datev.de
- Alexander Manecke, a.manecke@telekom.de
- Ignacio Ripoll, ignacio.ripoll@corpme.es
- Iris Speiser, iris.speiser@datev.de
- Marlene Urbschat, marlene.urbschat@datev.de

## Context

Individuals may hold multiple powers, mandates, or authorizations on behalf of an organization.

The consortium needed to determine whether mandate-related attestations should contain multiple faculties or be limited to a single authorization scope.

The core trade-off is between expressiveness and implementation simplicity.

## Decision

Mandate-related attestations shall be atomic.

Each attestation shall contain exactly one faculty or one service authorization.

Multiple powers shall be represented by multiple attestations rather than by composite authorization structures.

## Consequences

### What becomes easier?

- Simpler issuance and validation processes.
- Clear and unambiguous authorization semantics.
- Improved interoperability across participants.
- Easier lifecycle management of individual permissions.

### What becomes more difficult?

- Multiple attestations may be required for a single representative.
- Presentation and management of large authorization sets may become more complex.
- Real-world mandate structures may require aggregation mechanisms.

### How do we address the risks introduced by this change?

- Allow wallets and verifiers to present and process multiple attestations together.
- Define guidance for bundling and presenting related attestations.
- Reassess granularity requirements as additional use cases emerge.

## Advice

- 2026-06-11: Consortium Working Group: Prefer simple, composable attestations over complex multi-purpose credentials.
- 2026-06-11: Technical Participants: Atomic credentials simplify interoperability and validation logic.
