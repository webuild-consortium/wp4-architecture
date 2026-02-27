# Architecture Overview

## The Ecosystem at a Glance
The EU digital identity and EU business wallet ecosystem is an instance of the 3 party model for attestations. In this model there are 4 main actors:
1. The holder, aka the identity wallet that is controlled by either a natural or legal person
2. The issuer that relies on authentic sources of information to issue attestations to the holder/wallet
3. The verifier receives an attestation based on information present in the wallet.
4. The trust framework that in the EU ecosystems is based on ETSI TS 119604/119612 aka trust status lists populated by trust status providers that for some use cases are QTSPs

The EU ecosystem for the natural person wallet is described in more detail in [ARF]. The corresponding document for the EU legal person wallet is in progress.

Several sources exist for describing the more general 3rd party model, including ongoing work in the IETF eg [https://datatracker.ietf.org/doc/draft-ietf-spice-vdcarch/]

## System Landscape

The diagram below illustrates the baseline trust topology of the EU wallet ecosystem. Issuers provide attestations to holders, holders present them to verifiers, and all parties anchor trust decisions against the EU trusted lists defined under ETSI TS 119 612 and ETSI TS 119 604 within the framework of the eIDAS Regulation. The trusted lists specify the recognised participants in schemes for electronic identification and trust services.

```mermaid
graph LR;
  issuer-->holder;
  holder-->verifier;
  issuer-->trust["trust "];
  verifier-->trust["trust "];
  holder-->trust["trust "];
```

In the WE BUILD project the focus is primarily on wallets for economic operators and public sector bodies. In this case the proposed regulation COM(2025) 838 includes the use of qualified electronic registered delivery services (QERDS) to enable messaging services between entities recognised in the ecosystem, and listed in a common digital directory. Accordingly, the generic trust anchor is replaced by a Qualified Trust Service Provider operating a Qualified Electronic Registered Delivery Service (QTSP/QERDS), through which senders and recipients route their trust and messaging interactions. The QTSP is recognised in a scheme for trust services, just like in the previous diagram, enabling other participants to verify QERDS evidence issued by the QTSP. The diagram changes to this:

```mermaid
graph LR;
  sender-->recipient;
  sender-->QTSP/QERDS;
  recipient-->QTSP/QERDS;
```

The sender and recipient can exchange documents such as electronic attestations of attributes and notifications. In some cases, senders and recipients can take the issuer-holder-verifier roles as illustrated above.

## Common Rules for Everyone
Security, error handling, auditability, portability.

## Wallet Implementation Models 
To be authored by Wallet Group. Describes the techn stacks, such as cloud-based vs. device-based solutions, and the differences between EUDIW for Natural Person and European Business Wallets for  economic operators.
### The EUDI Wallet for Natural Person
To come: [Issue 63](https://github.com/webuild-consortium/wp4-architecture/issues/63) will produce concept model in collaboration with Wallet Group.
### The Business Wallet for Economic Operators
To come: [Issue 63](https://github.com/webuild-consortium/wp4-architecture/issues/63) will produce concept model in collaboration with Wallet Group.
