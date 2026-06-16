# Minimum Viable Taxonomy for PoA/PoR

**Authors:**

- Consortium Architecture Working Group AMS Track 4
- Boris Lingl (boris.lingl@datev.de)
- Alexander Manecke (a.manecke@telekom.de)
- Ignacio Ripoll (ignacio.ripoll@corpme.es)
- Iris Speiser (iris.speiser@datev.de)
- Marlene Urbschat (marlene.urbschat@datev.de)

## Context

The consortium requires a shared taxonomy for Powers of Attorney (PoA) and Powers of Representation (PoR).

The current list of faculties that may be granted through a PoA is broad and not exhaustive. Different use cases require different faculties, and there is currently no consortium-wide agreement on the minimum set that must be supported.

The core trade-off is between a minimal taxonomy that can be implemented quickly and a comprehensive taxonomy that covers all real-world scenarios.

## Decision

The consortium will create a **Minimum Viable Taxonomy (MVT)** for PoA/PoR based on the requirements of the 13 identified consortium use cases.

The taxonomy will include all faculties required by the identified use cases, add missing faculties where needed, remove faculties not expected to be used by those use cases, and be refined through feedback from use-case owners until a consortium-complete list is achieved.

## Consequences

### What becomes easier?

This decision enables faster alignment across consortium participants, reduces implementation complexity, provides clearer mapping between use-case requirements and authorization capabilities, and supports earlier interoperability testing.

### What becomes more difficult?

At the same time, the taxonomy may not sufficiently cover all real-world scenarios, future use cases may require additional faculties, and governance processes will be needed to evolve the taxonomy over time.

### How do we address the risks introduced by this change?

To address these risks, the consortium will establish a feedback process with all use-case owners, review the taxonomy periodically, and allow future extensions without breaking existing implementations.

## Advice

On 2026-06-11, the Consortium Working Group recommended adopting a minimal taxonomy first and evolving it based on implementation experience. On the same date, the Use Case Representatives recommended reviewing all 13 use cases before declaring the taxonomy complete.
