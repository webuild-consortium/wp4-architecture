# Support for Sole Trader Representation

**Authors:**

- Consortium Architecture Working Group AMS Track 4

- Boris Lingl, boris.lingl@datev.de
- Alexander Manecke, a.manecke@telekom.de
- Ignacio Ripoll, ignacio.ripoll@corpme.es
- Iris Speiser, iris.speiser@datev.de
- Marlene Urbschat, marlene.urbschat@datev.de

## Context

The current PoA/PoR rulebooks focus primarily on legal persons and do not adequately represent sole traders and similar economic actors.

As a result, certain business structures cannot be represented consistently within the current model.

The core trade-off is between maintaining a legal-person-centric model and expanding the scope to support a broader set of economic actors.

## Decision

The consortium will extend the rulebook terminology from "legal person" to the broader concept of an "economic operator."

The consortium will leverage the EBWOID initiative and use an EUID-like identifier approach to support identity representation for sole traders and similar actors.

Where necessary, existing implementations may continue to process legacy terminology during a transition period, provided that semantic interpretation remains aligned with the new rulebook concept.

## Consequences

### What becomes easier?

- Inclusion of sole traders within the ecosystem.
- Broader applicability of PoA/PoR use cases.
- Improved alignment with real-world business structures.
- Better consistency across participating jurisdictions.

### What becomes more difficult?

- Cross-border identifier interoperability remains challenging.
- National registration systems may use incompatible identifiers.
- Additional governance may be required for identifier mapping.

### How do we address the risks introduced by this change?

- Reuse existing EBWOID work wherever possible.
- Define guidance for identifier mapping and interoperability.
- Continue collaboration with relevant European initiatives addressing economic operator identification.
- Define a migration approach for legacy terminology to avoid interpretation inconsistencies during rollout.

## Advice

- 2026-06-11: Consortium Working Group: The rulebook should support all relevant economic actors, not only legal persons.
- 2026-06-11: Identity Domain Experts: Existing EUID-like approaches should be reused where possible.
- 2026-06-11: Member States: Cross-border identifier harmonization remains an open challenge that requires further work.
