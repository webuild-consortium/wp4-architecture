# Identity Matching and Subject Linking in WE BUILD

**Authors:**

- Michelle Ludovici, DIGG, Sweden
- Malin Norlander, Bolagsverket, Sweden

**Obsoletes:** N/A

**Obsoleted by:** N/A

## Context

The WE BUILD consortium needs to determine how identity matching and subject linking should be handled in the context of the European Digital Identity Wallet and the European Business Wallet.

Under Regulation (EU) 2024/1183, identity matching is defined as a process where person identification data or electronic identification means are matched with, or linked to, an existing account belonging to the same person. For cross-border services, Member States acting as relying parties must ensure unequivocal identity matching for natural persons using notified electronic identification means or European Digital Identity Wallets. This obligation is considered mandatory for relying parties that are public bodies.

The main issue is that the mandatory attributes in the PID (family name, given name, birth date, birthplace and nationality) are not always sufficient to perform unequivocal identity matching. Each public-sector relying party therefore needs to determine what level of legal identity matching is sufficiently secure for its processes.

The consortium discussed several possible approaches during the workshop in Amsterdam on the 10th and the 11th of June 2026. One option is the use of pseudonyms, including directed pseudonyms that are unique per user and per relying party. Another option is the use of e-signatures, where a qualified signature could support a deterministic and persistent match, although this would introduce dependencies on signature providers. A third option is enrichment of attributes, for example through IBAN, national unique identification numbers, VAT numbers or other attestations. The consortium also discussed the possibility of testing a Photo ID attestation based on ISO 23220, as well as the inclusion of a unique persistent identifier in the PID that can be selectively disclosed where needed.

The main trade-off is between technical feasibility, interoperability, legal certainty, regulatory requirements and privacy. Some relying parties, such as banks or public bodies, may need an official unique identifier from an authentic source. Other relying parties may only need to recognise a returning user without receiving a cross-context identifier. Pseudonyms can support privacy-preserving recognition within one relying-party context, but may not satisfy regulated use cases requiring auditability or official identification. Attribute enrichment can improve matching, but may create GDPR, consistency and interoperability issues if every relying party requests different attestations. E-signatures may shift some legal accountability to the user, but they do not solve the underlying issue of insufficient PID attributes.

For subject linking, the consortium also discussed whether attestations such as EUCC or UBO could be used to prove representative rights. The conclusion was that EUCC and UBO attestations should not be used as mandate attestations, as company ownership or company information does not itself prove a right to act on behalf of the company. Separate mandate attestations are therefore needed.

## Decision

The consortium agrees on the following decisions for WE BUILD.

First, for use cases that, by law, need to register an official identifier from an authentic source, WE BUILD will use a unique persistent identifier in the PID. This identifier should be selectively disclosable, so that it is only revealed where the relying party has a legitimate need for an official unique identifier, for example in regulated or public-sector use cases.

Second, for use cases that do not need an official identifier or are not bound by strict regulations, but do need a unique and persistent identifier, WE BUILD will implement directed pseudonym attestations. The pseudonym will be derived from a seed (NONs) provided by the PID provider, and generated through a pseudonym service that can be implemented either by the wallet provider or by a dedicated pseudonym service component.

Third, WE BUILD will test the use of Photo ID, based on ISO 23220, as an additional option for identity matching in selected use cases. This is considered an enrichment option for use cases where a persistent and official identifier may be needed, while recognising that overuse of Photo ID should be avoided.

Fourth, for subject linking, WE BUILD will not use EUCC or UBO attestations as mandate attestations. Separate mandate attestations, such as proof of authority, proof of representation or authorisation attestations, are needed to prove that a natural person is entitled to act on behalf of a legal person.

Fifth, for subject linking and identity matching, WE BUILD will apply the principle of one pseudonym per subject and per relying party. This limits the creation of multiple pseudonyms for the same subject within the same relying-party context and supports repeated authentication to the same account or service.

Finally, two pull requests will be created on GitHub. One pull request will cover the decisions on the unique persistent identifier in the PID and directed pseudonym attestations. A second pull request will cover the Photo ID option.

## Consequences

This decision makes it easier for relying parties that legally require an official identifier to perform identity matching through a selectively disclosable unique persistent identifier in the PID. It also provides a privacy-preserving option for relying parties that do not need an official identifier, by allowing them to recognise returning users through directed pseudonyms. The approach creates a clearer distinction between use cases that require official identification and use cases that only require recurring recognition of the same user. It also clarifies that company information, UBO information or EUCC attestations should not be treated as proof of authority.

At the same time, the decision introduces implementation challenges. PID providers and wallet providers will need to support the inclusion, protection and selective disclosure of a unique persistent identifier. Directed pseudonyms will require implementation by wallet providers, PID providers or pseudonym services, including agreement on generation logic, lifecycle and persistence. If a user changes wallet provider, pseudonym continuity may become difficult unless the architecture ensures persistence independently from the wallet provider. Pseudonyms may also not meet the needs of regulated sectors that require official identification and auditability.

The Photo ID option may support certain regulated or higher-assurance use cases, but it also introduces risks around proportionality and over-disclosure. It should therefore not be used as a default solution, particularly in situations where the PID or a pseudonym would be sufficient. Attribute enrichment more generally may raise GDPR and interoperability concerns, especially if different relying parties request different additional attestations.

The risks introduced by this decision should be addressed through clear scoping and data minimisation. The unique persistent identifier should only be disclosed where legally or operationally required. Directed pseudonyms should be used where relying-party-specific recognition is sufficient. Photo ID should be tested only in clearly defined use cases where its use is proportionate. The consortium should also clarify lifecycle rules for pseudonyms, including what happens when the PID is revoked, reissued or when the user changes wallet provider. Wallet providers and PID providers should be consulted on feasibility, implementation responsibilities and lifecycle implications. Finally, separate mandate attestations should be used for representative rights, rather than relying on EUCC or UBO attestations.

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- 2026-06-16, Astrid Verhallen, Infogreffe, FR: OK
- 2026-06-16, Erwin Nieuwlaar, KVK, NL: OK
