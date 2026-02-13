# Deliver business wallet data using QERDS

**Authors:**

- Sander Dijkhuis, Cleverbase, the Netherlands
- Leif Johansson, SIROS, Sweden

## Context

The WP4 Architecture group discussed at the [IRL Workshop](https://portal.webuildconsortium.eu/group/architecture/event/irl-workshop) the [draft on eDelivery](https://github.com/webuild-consortium/wp4-architecture/pull/25) for wallet-to-wallet messaging.
Afterwards, the European Commission published the European Business Wallet (EBW) proposal [COM(2025) 838 final](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0838) that includes a secure communication channel: a designated qualified electronic registered delivery service (QERDS).
See the definition in [Business Wallet Definition](https://portal.webuildconsortium.eu/group/16/files/4810/collabora-online/view/2773) (version 2026-01-14).
This definition and the WE BUILD approach was discussed during the [Business Wallet Workshop](https://portal.webuildconsortium.eu/group/wallet-providers/event/business-wallet-workshop).

While the QERDS was already part of the WE BUILD Grant Agreement, this record makes it explicit part of the WE BUILD architecture and specifies high-level starting points.
Use cases are encouraged to specify scenarios with the QERDS in wallet-to-wallet interactions as well as using gateways to connect to existing infrastructures.

The QERDS should comply to the eIDAS requirements for QERDS as well as the proposed EBW requirements for the designated QERDS.
The Commission Implementing Regulation [(EU) 2025/1944] applies regarding “reference standards for processes for sending and receiving data in \[QERDS\]s and as regards interoperability of those services”.
For the designated QERDS, no draft implementing act is available yet, but high-level requirements are included in the EBW proposal Annex chapter 11, as well as Article 5(3) for availability to European Digital Identity Wallets.
It is expected that WE BUILD implementation experience can contribute to the specification of the EBW implementing act.

[(EU) 2025/1944]: https://eur-lex.europa.eu/eli/reg_impl/2025/1944/oj

Key assumptions are:

- the use of the European Digital Directory (EBW Article 10) for identification (looking up EUIDs), discovery (finding networks and capabilities), and connections (retrieving protocol and endpoint information including public keys);
- the ability for multiple qualified trust service providers to federatively provide the QERDS;
- the application of architecture models from the reference standard [EN 319 522-1](https://www.etsi.org/deliver/etsi_en/319500_319599/31952201/01.02.01_60/en_31952201v010201p.pdf):
    - 4-corner model (§ 4.3) for EBW-to-EBW exchange;
    - extended model (§ 4.4) for exchange through a gateway (EBW Article 16(6)(b)).

For EBW-to-QERDS communication, there does not yet seem to exist a common protocol and the WP4 Architecture group has discussed various ideas.

For communication between QERDS providers, the reference standard [EN 319 522-4-1](https://www.etsi.org/deliver/etsi_en/319500_319599/3195220401/01.02.01_60/en_3195220401v010201p.pdf) specifies bindings based on AS4 (HTTP-based protocol in [ISO 15000-2:2021](https://www.iso.org/standard/79109.html), [OASIS Standard](https://docs.oasis-open.org/ebxml-msg/ebms/v3.0/profiles/AS4-profile/v1.0/os/AS4-profile-v1.0-os.html)) or email.
The AS4 standard is referenced in EU legislation and implementations such as Peppol using the [eDelivery AS4] building block. Other protocols that follow the same architectural model exist, and are outlined in the considered alternatives later in this section.

[eDelivery AS4]: https://ec.europa.eu/digital-building-blocks/sites/spaces/DIGITAL/pages/467110114/eDelivery

The AS4 protocol is based on XML signature and encryption which does do not yet provide post-quantum safety. There is no current effort in any standards development organisation to propose post-quantum algorithms for XML signatures or key agreement/encryption. This means that the effective lifetime of a solution based on AS4 as-is is limited to a maximum of 6 or 7 years from the required go-live date for the European Business Wallet. Therefore, in a production ecosystem, protocol migration should be possible.

The 4-corner model of the AS4 architecture provides a way to introduce an abstraction layer towards the QERDS, which means that in principle it is possible to replace the underlying QERDS protocol in the future, although such a task would present significant challenges in practice.

The following alternatives were considered:

- [OpenID4VC](https://openid.net/sg/openid4vc/) and [ISO/IEC 18013-7](https://www.iso.org/standard/91154.html) are standards for receiving credentials into and generating and presenting proofs from the EUDI Wallet. These protocols are well suited for flows that involve user interaction, but are more difficult to adapt to flows that involve automated systems or agents.
- [DIDComm](https://identity.foundation/didcomm-messaging/spec/v2.1/) is conceptually quite similar to AS4 and has many benefits including a better path towards quantum safe signatures and encryption than an XML-based protocol has at this point. The downside of this alternative is that the standards need to be profiled for use in the EU, for example to reference existing trust infrastructure.
- Alternatively, a new suite of protocols could be developed that fulfill the expected requirements of the EUBW such as suitability for automation and agents, compatibility with the EUDI natural person wallet etc. There are several options that could serve as a modern starting point for such work including the [Matrix](https://matrix.org/) protocol and [ActivityPub](https://activitypub.rocks/).

## Decision

WE BUILD tests and pilots a designated QERDS, with the following responsibilities:

- WP4 Trust Registry Infrastructure group establishes a WE BUILD Digital Directory aligned with the EU Digital Directory standards.
- WP4 QTSP group, in consultation with WP4 Architecture and WP4 Wallet Providers groups, specifies an optional API access protocol as an abstraction layer between the wallet and the QERDS.
- WP4 QTSP group facilitates pilots using [(EU) 2025/1944] and [eDelivery AS4].
- WP4 Architecture and WP4 QTSP groups jointly evaluate the requirements for a potential “AS5” alternative QERDS protocol, based on the needs of WP2/WP3 use cases.

If use cases require gateways to the designated QERDS, in principle the use cases are responsible for providing those gateways.

## Consequences

Testing and piloting with a designated QERDS makes it easier:

- To implement use cases for the EUBW that requires automation and/or agent-based access.
- To connect with organisations responsible for authentic sources for the retrieval and/or verification of attributes, which is necessary for the issuance of qualified electronic attestations of attributes (see [Feature: Verification of attributes](https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qeaa/verification.feature.md)).
- To develop the QERDS aspect of the envisioned EBW ecosystem, building upon existing ecosystems like the Once-Only Technical System and Peppol, using the WE BUILD ecosystem and its Interoperability Test Bed to provide a meaningful and collaborative context.

Open issues:

- Adapting end-to-end encryption in the four-corner model to the European Business Wallet.
- Support hardware bound credentials and differentiated level of assurance.

The WP4 Architecture group can provide the necessary design competence.

The following risks need to be addressed:

- QERDS and eDelivery are new subject matter to several wallet providers and implementers.
  They may be tempted to instead mold the well-known OpenID4VC protocols to use cases that are better suited for QERDS.
  To address this risk, WP4 Architecture group members and in particular Use Case Sync Leads are expected to learn about QERDS and engage with the WP2/WP3 groups to learn which practical use cases will drive adoption of automation and agent-based flows that are the main motivators for using QERDS in the EBW.
- The QERDS requires several cross-group implementations.
  To reduce interoperability risks, the WP4 QTSP group should:
    - specify at least two [Conformance Specifications](https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/README.md) in consultation with stakeholder groups:
        - EBW-to-QERDS;
        - QTSP-to-QTSP for QERDS;
        - (if use cases need it) EUDIW-to-QERDS;
    - work with the WP4 Testing group to perform testing using these Conformance Specifications on the [Interoperability Test Bed](https://github.com/webuild-consortium/wp4-interop-test-bed).

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- [2026-02-03, Andrew Freund, D-Trust, Germany](https://github.com/webuild-consortium/wp4-architecture/pull/61#pullrequestreview-3744059166): OK, with processed suggestions regarding detailed requirements and the Interoperability Test Bed.
- [2026-02-11, Alejandro Nieto, DigitelTS, Spain](https://github.com/webuild-consortium/wp4-architecture/pull/61#issuecomment-3885426557): OK, agreed with the proposed standards and protocols.
- [2026-02-11, Rune Kjørlaug, OpenPeppol, Belgium](https://github.com/webuild-consortium/wp4-architecture/pull/61#pullrequestreview-3785222841): Contributed comments regarding directory functions (parked for a next ADR), AS4 suitability, protocol migrations and avoiding lock-in, co-existence with existing ecosystems like Peppol.
- [2026-02-12, Giuseppe De Marco, Dipartimento per la trasformazione digitale, Italy](https://github.com/webuild-consortium/wp4-architecture/pull/61#pullrequestreview-3791113532): Recommendation to consider [relying party intermediary architectures](https://github.com/webuild-consortium/wp4-architecture/pull/31) when designing QERDS gateways.
