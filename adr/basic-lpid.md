# Provide EBWOID as a stable minimal basis

**Authors:**

- Sander Dijkhuis, Cleverbase, the Netherlands

## Context

In BU3 on foreign tax declaration, an issue on [Identifiers in LPID](https://portal.webuildconsortium.eu/group/5/files/3645/collabora-online/edit/974) was raised to WP4 Architecture, which extends to EBWOID. In this context, EBWOID is *European Business Wallet owner identification data*. Should the EBWOID just be a “bootstrap identity” with a stable minimum attribute set, or should EBWOID be a “dynamic reference framework” containing many relevant attributes registered by competent bodies?

In the Annex of [(EU) 2024/2977](https://data.europa.eu/eli/reg_impl/2024/2977/oj), Table 3 specifies mandatory legal person identification data in line with the “bootstrap identity”, and Table 4 specifies optional legal person identification data that leans more towards the “dynamic reference framework”.

In [COM(2025) 838 final](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0838), Article 8(5) the EBWOID is specified to contain just the name and unique identifier in accordance with Article 9.
Furthermore, in Article 20, legal person identification data may become irrelevant under EU Digital Identity.

The implementation choice affects what other electronic attestations of attributes may be needed for use cases such as BU3.

Under EU Digital Identity, EU Member States may take different decisions with regard to this. The upcoming EU Business Wallet legislation may affect these decisions.

To achieve cross-border interoperability within WE BUILD, several options are possible:

- basic EBWOID everywhere (minimum attributes from a single source)
- extended EBWOID everywhere (attributes such as the VAT registration number)
- basic EBWOID in some EU Member States, extended EBWOID in others

## Decision

Rely on basic EBWOID everywhere as a minimum identity attestation which must be supported by everyone. Develop use cases under the assumption that other attributes require additional electronic attestations.
These other attributes can be used both for identifying the economic operator and for verifying additional claims.

## Consequences

The [EBWOID rulebook](https://github.com/webuild-consortium/eudi-wallet-rulebooks-and-schemas/blob/main/rulebooks/ds001-ebw-oid-rulebook.md) should be kept in line with this decision.

With this decision, it becomes easier to reason about the minimum set of additional electronic attestations.

With this decision, it becomes more difficult to test the extended EBWOID case, which may be relevant to some EU Member States. But note that the decision does not preclude testing with extended EBWOID as well.

To manage the risk that this approach differs from EU Business Wallet legislation, WE BUILD should take the definition of EBWOID in account in its upcoming definition of an EU Business Wallet.

To get started with the minimum identification data, the WP4 PID/LPID group should specify which unique identifier(s) to use.

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- [2025-11-17, Michelle Ludovici, Digg, Sweden](https://github.com/webuild-consortium/wp4-architecture/pull/27#discussion_r2534441610): OK, but this does not yet solve the question: which unique identifier should be used in the LPID and EBWOID? Proposing to use the European Unique Identifier from (EU) 2017/1132.
- [2025-11-18, Ronald Koenig, Spherity, Germany](https://github.com/webuild-consortium/wp4-architecture/pull/27): Only acceptable if it does not preclude the use of more comprehensive “identity attestations” (EUCC, KYC, etc.).
- [2026-02-02, Erwin Nieuwlaar, KvK, the Netherlands](https://github.com/webuild-consortium/wp4-architecture/pull/27#issuecomment-3835190788): The PID/EBWOID group agrees the EBWOID should consist of a minimal and stable set of fields. There is still discussion about whether EBWOID is necessary for a functional EBW (out of scope for this ADR).
- [2026-02-03, Jonas Toennis, Brønnøysund Registry Center, Norway](https://github.com/webuild-consortium/wp4-architecture/pull/27#issuecomment-3841325270): OK, and note that the PID/EBWOID group considers the EBWOID to functionally have the same effect for business wallets as PID for digital identity wallets. Also, there are questions regarding the use of other attestations for company identity (out of scope for this ADR).
- [2026-02-09, Sarah Amandusson, Digg, Sweden](https://github.com/webuild-consortium/wp4-architecture/pull/27#issuecomment-3872840145): Note the alignment on LPID removal and EBWOID spelling from pending ADR [#67](https://github.com/webuild-consortium/wp4-architecture/pull/67).
