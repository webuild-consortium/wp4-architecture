# Provide LPID and EBW-OID as a stable minimal basis

**Authors:**

- Sander Dijkhuis, Cleverbase, the Netherlands

## Context

In BU3 on foreign tax declaration, an issue on [Identifiers in LPID](https://portal.webuildconsortium.eu/group/5/files/3645/collabora-online/edit/974) was raised to WP4 Architecture, which extends to EBW-OID. In this context, LPID is *legal person identification data* and EBW-OID is *European Business Wallet owner identification data*. Should the LPID and EBW-OID just be a “bootstrap identity” with a stable minimum attribute set, or should LPID and EBW-OID be a “dynamic reference framework” containing many relevant attributes registered by competent bodies?

In the Annex of [(EU) 2024/2977](https://data.europa.eu/eli/reg_impl/2024/2977/oj), Table 3 specifies mandatory PID for the legal person in line with the “bootstrap identity”, and Table 4 specifies optional PID for the legal person that leans more towards the “dynamic reference framework”.

In [COM(2025) 838 final](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0838), Article 8(5) the EBW-OID is specified to contain just the name and unique identifier in accordance with Article 9.
Furthermore, in Article 20, LPID may become irrelevant under EU Digital Identity.

The implementation choice affects what other electronic attestations of attributes may be needed for use cases such as BU3.

Under EU Digital Identity, EU Member States may take different decisions with regard to this. The upcoming EU Business Wallet legislation may affect these decisions.

To achieve cross-border interoperability within WE BUILD, several options are possible:

- basic LPID and EBW-OID everywhere (minimum attributes from a single source)
- extended LPID and EBW-OID everywhere (attributes such as the VAT registration number)
- basic LPID and EBW-OID in some EU Member States, extended LPID and EBW-OID in others

## Decision

Rely on basic LPID and EBW-OID everywhere as a minimum identity attestation which must be supported by everyone. Develop use cases under the assumption that other attributes require additional electronic attestations.
These other attributes can be used both for identifying the economic operator and for verifying additional claims.

## Consequences

The [EBW-OID rulebook](https://github.com/webuild-consortium/eudi-wallet-rulebooks-and-schemas/blob/main/rulebooks/ds001-ebw-oid-rulebook.md) should be kept in line with this decision.
The LPID rulebook, if any (removed in [webuild-consortium/eudi-wallet-rulebooks-and-schemas#24](https://github.com/webuild-consortium/eudi-wallet-rulebooks-and-schemas/pull/24)), as well.

With this decision, it becomes easier to reason about the minimum set of additional electronic attestations.

With this decision, it becomes more difficult to test the extended LPID and EBW-OID case, which may be relevant to some EU Member States. But note that the decision does not preclude testing with extended LPID and EBW-OID as well.

To manage the risk that this approach differs from EU Business Wallet legislation, WE BUILD should take the definition of LPID and EBW-OID in account in its upcoming definition of an EU Business Wallet.

To get started with the minimum identification data, the WP4 PID/LPID group should specify which unique identifier(s) to use.

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- [2025-11-17, Michelle Ludovici, Digg, Sweden](https://github.com/webuild-consortium/wp4-architecture/pull/27#discussion_r2534441610): OK, but this does not yet solve the question: which unique identifier should be used in the LPID and EBW-OID? Proposing to use the European Unique Identifier from (EU) 2017/1132.
- [2025-11-18, Ronald Koenig, Spherity, Germany](https://github.com/webuild-consortium/wp4-architecture/pull/27): Only acceptable if it does not preclude the use of more comprehensive “identity attestations” (EUCC, KYC, etc.).
