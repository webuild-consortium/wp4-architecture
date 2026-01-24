# Publish consortium trusted lists

**Authors:**

- Sander Dijkhuis, Cleverbase, the Netherlands

## Context

For the first usage of the interoperability testbed, and for the first increment, it is required to enable trust between issuers, wallets, and verifiers. EWC proposed a trust evaluation mechanism (see [EWC RFC 012](../ewc-rfcs/ewc-rfc012-trust-mechanism.md)) including an [Trusted List](https://github.com/EWC-consortium/ewc-trust-list).

According to the evaluation made so far by the Mapping Task Force, at least the QTSP group needs a similar approach for the first QEAAs to test. We need to specify who provides this.

At ETSI, the TS 119 612 ([V2.3.1](https://www.etsi.org/deliver/etsi_ts/119600_119699/119612/02.03.01_60/ts_119612v020301p.pdf) at time of this release) series is being updated to support the European Digital Identity. This may require further alignment with the current EWC implementations.

## Decision

The WP4 Trust Registry Infrastructure group provides trusted lists.

The issuers in the WP4 PID/LPID/QTSP/Wallet provider groups request registration on the trusted lists before testing.

The wallets in the WP4 Wallet provider group include validation with the trusted lists in their verification processes.

The relying parties in WP2/3/4 include validation with the trusted lists in their verification processes.

The starting point is TS 119 612 V2.3.1. Since a profile and implementation guidance are likely needed, and EWC RFC 012 has not yet been effective in practice, these should be specified in separate WE BUILD architecture documents.

## Consequences

This decision makes interop between consortium members easier.

This decision makes it harder to test with ad-hoc pairwise trust relationships.

To address the risk of bottlenecks in implementing this decision, the Mapping Task Force pays extra attention to potential blockers for each involved WP4 group.

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- 2025-10-27, Leif Johansson, Sunet, Sweden: OK
- 2025-10-27, Giuseppe De Marco, Dipartimento per la trasformazione digitale, Italy: OK
