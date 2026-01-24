# Baseline protocols

**Authors:**

- Leif Johansson, Sunet, Sweden
- Sander Dijkhuis, Cleverbase, the Netherlands
- Sarah Amandusson, Digg, Sweden
- George J Padayatti, iGrant.io, Sweden
- Lal Chandran, iGrant.io, Sweden

## Context
The EUDI Wallet ecosystem is mandated by eIDAS to ensure secure, interoperable cross-border digital identity.
This implementation is guided by the Architecture and Reference Framework (ARF), which translates legal mandates into technical specifications.
To achieve mandatory interoperability for Issuance and Presentation of Person Identification Data (PID) and Electronic Attestations of Attributes (EAA), implementing regulations require compliance with foundational standards.
OID4VCI (Issuance) and OID4VP (Presentation) are adopted as the ARF-recommended baseline protocols for technically implementing the required data models and web-based transport mechanisms in the pilot.

Proximity flows are out of scope for the current architecture decision.

While the architecture decision to [Publish consortium trusted lists](trusted-lists.md) based on TS 119 612 has already been recorded, the consortium also needs a selection of PID/EAA issuance and presentation protocols.

## Decision

Each recognized role in the WE BUILD project - PID/LPID Providers, EAA Providers (including QEAA, Pub-EAA), Relying Parties, Wallet Providers, and Trust Service Providers — is REQUIRED to implement the corresponding technical profiles described here.
Actors performing multiple roles MUST meet all requirements relevant to those roles.

* PID/LPID Providers, EAA Providers (including QEAA, Pub-EAA) MUST implement [OpenID4VCI version 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html)
* Relying Parties MUST implement [OpenID4VP version 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)
* Wallet Providers MUST implement in wallet solutions [OpenID4VCI version 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) and [OpenID4VP version 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)

## Consequences

Implementations following this profile ensure interoperability between actors within the WE BUILD ecosystem.
Actors can verify conformance through testing against other implementations.

The selected protocols may not suffice for async or proximity use cases. Once the requirements for such use cases appear, the decision may need to be nuanced to enable for example Relying Parties to implement different protocols.

## Advice

Once merged, this is our consortium’s decision. This does not mean all participants agree it is the best possible decision. 

