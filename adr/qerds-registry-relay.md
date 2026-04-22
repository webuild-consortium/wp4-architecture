# Separate QERDS registry from relay

**Authors:**

- Sander Dijkhuis, Cleverbase, the Netherlands

## Context

To [Deliver business wallet data using QERDS](https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/build-qerds.md), the WP4 QTSP group is specifying an interoperability framework for testing and piloting this Qualified Electronic Registered Delivery Service using WE BUILD Business Wallets. Two major components of its [reference architecture](https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qerds/architecture.md) are:

- delivery registry: register evidence of submission or notification upon identity verification of the sender or recipient;
- delivery relay: between QERDS providers, relay documents, notifications, or evidence.

To simplify the framework, ETSI [TR 119 520-1](https://www.etsi.org/deliver/etsi_tr/119500_119599/11952001/01.01.01_60/tr_11952001v010101p.pdf) proposes to treat these as orthogonal concerns.

The framework defines the concept of a *package*: an immutable sealed artifact comprising user content, delivery evidence, and relay metadata. The package is potentially partly or fully end-to-end encrypted.

In the TR 119 520-1 treatment, the delivery registry (“smart wrap service”) results in dispatch or receipt packages. This means that most security requirements regarding confidentiality and integrity are implemented by QERDS providers upon delivery registry. Delivery relay (“XXTP(S) service”) is about transport protocols for interoperable message exchange between QERDS providers, and is only necessary if the sender uses another provider than the recipient.

An alternative approach would be to implement QERDS security requirements using the security features of the delivery relay interoperability protocol. For example, eDelivery AS4 applies XML Signature and XML Encryption features for delivery relay. Implementations of QERDS could apply these features to protect not only the relay metadata exchanged between QERDS providers, but also the submission or notification and the QERDS evidence. However, this would increase the complexity of changes to either the security or interoperability specifications.

The ETSI EN 319 522 series have not yet been updated to apply the findings from TR 119 520-1, and there do not seem to be concrete plans to. The ETSI STF 705 project WP4 ongoing until June 2027 or another project may apply this eventually. In the meantime, WE BUILD needs to have some interoperability profile that works today and is sufficiently future-proof with the current knowledge.

## Decision

WE BUILD separates the specification of:

- **delivery registry** to produce and consume packages on behalf of authenticated users;
- **delivery relay** to transport packages between QERDS providers.

In the context of delivery registry, the semantics of the packages are defined in ETSI [EN 319 522-2](https://www.etsi.org/deliver/etsi_en/319500_319599/31952202/01.02.01_60/en_31952202v010201p.pdf). Following TR 119 520-1, WE BUILD applies at minimum:

- **dispatch package** (“ERD dispatch”): document submission or procedural notification, along with delivery evidence;
- **receipt package** (“ERDS receipt”): notification of a delivery event related to an earlier dispatch package.

For delivery relay, the transport protects against QERDS provider impersonation and eavesdropping relay metadata. It is applied only under the condition the sender and recipient have different QERDS providers.

## Consequences

The decision makes it easier to learn about the consequences of the technical direction in TR 119 520-1. It also decomposes the problem into two sub-problems, making it easier to specify technical solutions. The decomposition also enables separate interoperability testing of the specifications.

The decision precludes solutions where the transport protocol may already provide the end-to-end security required from QERDS in European Business Wallets. For example, while mTLS between business wallet instances could technically be used for the mandatory identification of sender and recipient or for the mandatory end-to-end encryption, WE BUILD deliberately decouples these functions from the transport.

The main risk to manage is divergence with the ongoing ETSI standardisation and European Business Wallet legislation by the European Commission, rendering the test and pilot results less relevant for the production ecosystem. We address this risk by requesting early feedback on WE BUILD deliverables from both the Commission and ETSI STF 705 WP4.

## Advice

Once merged, this is our consortium’s decision. This does not mean all participants agree it is the best possible decision. In the decision making process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice (to be added)
