# Architecture Overview

## The Ecosystem at a Glance
The EU digital identity and EU business wallet ecosystem is an instance of the 3 party model for verifiable digital credentials (VDCs). In this model there are 4 main actors:
1. The holder, aka the identity wallet that is controlled by a data subject (either a natural or legal person)
2. The isssuer that relies on authentic sources of information to issue VDCs to the holder/wallet
3. The verifier that recieves verifiable digital credential presentaions (VDPs) based on information present in VDCs from the holder/wallet.
4. The trust framework that in the EU ecosystems is based on ETSI TS 119604/119612 aka trust status lists populated by trust status providers that for some use cases are QTSPs

## System Landscape
```mermaid
issuer-->holder
holder-->verifier
issuer-->trust
verifier-->trust
holder-->trust
```
## Common Rules for Everyone
Security, error handling, auditability, portability.

## Wallet Implementation Models 
To be authored by Wallet Group. Describes the techn stacks, such as cloud-based vs. device-based solutions, and the differences between EUDIW for Natural Person and European Business Wallets for  economic operators.
### The EUDI Wallet for Natural Person
To come: [Issue 63](https://github.com/webuild-consortium/wp4-architecture/issues/63) will produce concept model in collaboration with Wallet Group.
### The Business Wallet for Economic Operators
To come: [Issue 63](https://github.com/webuild-consortium/wp4-architecture/issues/63) will produce concept model in collaboration with Wallet Group.


