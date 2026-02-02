# Deliver business wallet data using QERDS

**Authors:**

- Sander Dijkhuis, Cleverbase, the Netherlands

## Context

The WP4 Architecture group discussed at the [IRL Workshop](https://portal.webuildconsortium.eu/group/architecture/event/irl-workshop) the [draft on eDelivery](https://github.com/webuild-consortium/wp4-architecture/pull/25) for wallet-to-wallet messaging.
Afterwards, the European Commission published the European Business Wallet (EBW) proposal [COM(2025) 838 final](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0838) that includes a secure communication channel: a designated qualified electronic registered delivery service (QERDS).
See the definition in [Business Wallet Definition](https://portal.webuildconsortium.eu/group/30/files/6277/collabora-online/edit/2773) (version 2026-01-14).
This definition and the WE BUILD approach was discussed during the [Business Wallet Workshop](https://portal.webuildconsortium.eu/group/wallet-providers/event/business-wallet-workshop).

While the QERDS was already part of the WE BUILD Grant Agreement, this record makes it explicit part of the WE BUILD architecture and specifies high-level starting points.
Use cases are encouraged to specify scenarios with the QERDS in wallet-to-wallet interactions as well as using gateways to connect to existing infrastructures.

The QERDS should comply to the eIDAS requirements for QERDS as well as the proposed EBW requirements for the designated QERDS.
The Commission Implementing Regulation [(EU) 2025/1944] applies regarding “reference standards for processes for sending and receiving data in \[QERDS\]s and as regards interoperability of those services”.
For the designated QERDS, no draft implementing act is available yet, but high-level requirements are included in the EBW proposal Annex chapter 11, as well as Article 5(3) for availability to European Digital Identity Wallets.
It is expected that WE BUILD implementation experience can contribute to the specification of the EBW implementing act.

[(EU) 2025/1944]: https://eur-lex.europa.eu/eli/reg_impl/2025/1944/oj

Key assumptions are:

- the use of the European Digital Directory (EBW Article 10) for access point discovery;
- the ability for multiple qualified trust service providers to federatively provide the QERDS;
- the application of architecture models from the reference standard [EN 319 522-1](https://www.etsi.org/deliver/etsi_en/319500_319599/31952201/01.02.01_60/en_31952201v010201p.pdf):
    - 4-corner model (§ 4.3) for EBW-to-EBW exchange;
    - extended model (§ 4.4) for exchange through a gateway (EBW Article 16(6)(b)).

For EBW-to-QERDS communication, there does not yet seem to exist a common protocol and the WP4 Architecture group has discussed various ideas.

For communication between QERDS providers, the reference standard [EN 319 522-4-1](https://www.etsi.org/deliver/etsi_en/319500_319599/3195220401/01.02.01_60/en_3195220401v010201p.pdf) specifies bindings based on AS4 (HTTP-based protocol in [ISO 15000-2:2021](https://www.iso.org/standard/79109.html), [OASIS Standard](https://docs.oasis-open.org/ebxml-msg/ebms/v3.0/profiles/AS4-profile/v1.0/os/AS4-profile-v1.0-os.html)) or email.
The AS4 standard is widely used in EU legislation and implementations such as Peppol using the [eDelivery AS4] building block.

[eDelivery AS4]: https://ec.europa.eu/digital-building-blocks/sites/spaces/DIGITAL/pages/467110114/eDelivery

Even though AS4 may have post-quantum cryptography deployment issues, due to its use of XML Digital Signature and XML Encryption, it can be a useful starting point for WE BUILD testing and piloting.
Due to the use of the 4-corner model or extended model, from the EBW or use case implementer’s perspective, the communication between QERDS providers can be considered an implementation detail that may evolve at a different pace.

The following alternatives were considered:

- [OpenID4VC](https://openid.net/sg/openid4vc/) and [ISO/IEC 18013-7](https://www.iso.org/standard/91154.html) also provide messaging to and from wallets, but only in the case of “verifiable credentials”, and the protocols are optimised for interactive connections without standardised evidence records.
- [DIDComm](https://identity.foundation/didcomm-messaging/spec/v2.1/) also provides messaging between wallets, but not using EU standards.
- Alternatively, use cases could specify ad hoc APIs between the systems of various natural and legal persons. However, this means that each ad hoc API brings additional work of specifying connectivity and security requirements, and dealing with technical challenges that are already solved with eDelivery.

## Decision

WE BUILD tests and pilots a designated QERDS:

- provided by the WP4 QTSP group, with interoperability using a common API;
- taking [(EU) 2025/1944] and [eDelivery AS4] as a starting point for the security requirements and for the common API between QTSPs;
- implemented in wallet solutions by the WP4 Wallets group using a common API, to be specified by the WP4 QTSP group;
- supported by a WE BUILD Digital Directory, provided by the WP4 Trust Registry Infrastructure group.

If use cases require gateways to the designated QERDS, in principle the use cases are responsible for providing those gateways.

## Consequences

Testing and piloting with a designated QERDS makes it easier:

- To exchange messages (documents, including electronic attestations of attributes, and notifications, including requests) between EBWs, without the need for web-based user interaction.
- To connect with organisations responsible for authentic sources for the retrieval and/or verification of attributes, which is necessary for the issuance of qualified electronic attestations of attributes (see [Feature: Verification of attributes](https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qeaa/verification.feature.md)).
- To develop the QERDS aspect of the envisioned EBW ecosystem, using the WE BUILD ecosystem and its Interoperability Test Bed to provide a meaningful and collaborative context.

It becomes more difficult:

- To provide full end-to-end encryption: while OpenID4VC and mdoc protocols are designed with it from the start, the QERDS may require additional work to protect protocol metadata.
  The WP4 Architecture group can provide the necessary design competence.

The following risks need to be addressed:

- QERDS and eDelivery are new subject matter to several wallet providers and implementers.
  They may be tempted to instead mold the well-known OpenID4VC protocols to use cases that are better suited for QERDS.
  To address this risk, WP4 Architecture group members and in particular Use Case Sync Leads are expected to learn about QERDS and guide the use cases in determining applicability.
- The QERDS requires several cross-group implementations.
  To reduce interoperability risks, the WP4 QTSP group should specify at least two [Conformance Specifications](https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/README.md) in consultation with stakeholder groups:
    - EBW-to-QERDS
    - QTSP-to-QTSP for QERDS
    - (if use cases need it) EUDIW-to-QERDS

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
