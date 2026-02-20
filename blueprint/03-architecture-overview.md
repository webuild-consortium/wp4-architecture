# Architecture Overview

## The Ecosystem at a Glance
The EU digital identity and EU business wallet ecosystem is an instance of the 3 party model for attestations. In this model there are 5 main actors:
1. The holder, aka the natural or legal party controlling the identity wallet
2. The issuer (oe Electronic Attestation of Attributes Service Provider, EAASP) that relies on authentic sources of information to issue attestations to the holder/wallet
3. The verifier (or Relying Party, RP) receives an attestation based on information present in the wallet.
4. The Relying Party Intermediary (RPI) may act as a trusted intermediary between the verifier and the wallet, handling protocol complexity, attestation validation, and attribute transformation on behalf of the verifier (as recognized in eIDAS 2 Article 5b(10))
5. The trust framework that in the EU ecosystems is based on ETSI TS 119604/119612 aka trust status lists populated by trust status providers that for some use cases are QTSPs

The EU ecosystem for the natural person wallet is described in more detail in [ARF]. The corresponding document for the EU legal person wallet is in progress.

Several sources exist for describing the more general 3rd party model, including ongoing work in the IETF eg [https://datatracker.ietf.org/doc/draft-ietf-spice-vdcarch/]

## System Landscape

The diagram below illustrates the baseline trust topology of the EU wallet ecosystem. Issuers provide attestations to holders, holders present them to verifiers, and all parties anchor trust decisions against the EU trusted lists defined under ETSI TS 119 612 and ETSI TS 119 604 within the framework of the eIDAS Regulation.

```mermaid
graph LR;
  issuer-->holder;
  holder-->verifier;
  issuer-->trust;
  verifier-->trust;
  holder-->trust;
```

In the WE BUILD project the focus is primarily on wallets for legal entities. In this case the regulation includes the use of qualified electronic registered delivery services to enable messaging services between entities in the ecosystem. Accordingly, the generic trust anchor is replaced by a Qualified Trust Service Provider operating a Qualified Electronic Registered Delivery Service (QTSP/QERDS), through which issuers, holders, and verifiers route their trust and messaging interactions. The diagram changes to this:

```mermaid
graph LR;
  issuer-->holder;
  holder-->verifier;
  issuer-->QTSP/QERDS;
  verifier-->QTSP/QERDS;
  holder-->QTSP/QERDS;
```

When an RPI is involved, the trust topology extends to include the intermediary:

```mermaid
graph LR;
  issuer-->holder;
  holder-->RPI;
  RPI-->verifier/RP;
  issuer-->QTSP/QERDS;
  verifier/RP-->QTSP/QERDS;
  holder-->QTSP/QERDS;
```

## Common Rules for Everyone
Security, error handling, auditability, portability.

## Wallet Implementation Models 
To be authored by Wallet Group. Describes the techn stacks, such as cloud-based vs. device-based solutions, and the differences between EUDIW for Natural Person and European Business Wallets for  economic operators.
### The EUDI Wallet for Natural Person
To come: [Issue 63](https://github.com/webuild-consortium/wp4-architecture/issues/63) will produce concept model in collaboration with Wallet Group.
### The Business Wallet for Economic Operators
To come: [Issue 63](https://github.com/webuild-consortium/wp4-architecture/issues/63) will produce concept model in collaboration with Wallet Group.
