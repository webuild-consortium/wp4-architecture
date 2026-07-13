# Credential offer endpoint registry and lookup

**Authors:**

- Lal Chandran, iGrant.io, Sweden
- Nikolaos Triantafyllou, University of Aegean, Greece

## Context

Issuer-initiated credential issuance requires a European Business Wallet (EBW) to expose a credential offer endpoint, that is, a reachable target to which an Issuer can deliver a credential offer. Mandating such an endpoint is necessary for interoperability: without it, an Issuer cannot rely on any given EBW being able to receive a pushed credential offer, and issuer-driven flows such as onboarding, re-issuance and attestation delivery become unreliable.

A naively mandated endpoint, however, makes every EBW a permanently reachable, publicly addressable target. This strips engagement control from the Wallet Owner, creates an unsolicited-inbound surface for credential spam and phishing, and disproportionately affects SMEs and sole traders who lack filtering and security operations.

The [Wallet Unit Attestation and lifecycle management](wallet-unit-lifecycle-management.md) decision deferred this concern, noting that the availability of the Wallet Owner for notifications and submission of documents is a separate layer governed by entry in the WE BUILD Digital Directory. This ADR specifies that layer, so that the mandated endpoint delivers interoperability without becoming an open relay.

## Decision

The WE BUILD Digital Directory layer SHALL be composed of two distinct components: a **Registry** as the authoritative source of record, and a **Lookup Service** as the permissioned resolution interface over it. The write path (registration, governed by the Wallet Provider and Wallet Owner) is kept independent from the read path (resolution, exposed to Issuers).

**Registry**

- Registration MUST be performed by the Business Wallet Provider on behalf of the Wallet Unit, and MUST be opt-in by the Wallet Owner.
- The Wallet Owner MUST control which Issuers, or classes of Issuer, are authorised to resolve and reach its endpoint.
- A Registry entry binds the endpoint to the Wallet Unit's identity (EBWOID) and structural trust (WUA).
- The Registry is the single point at which endpoint records and authorisation policy are created, updated and removed.

**Lookup Service**

- A credential offer endpoint MUST NOT be published openly; it MUST be resolved through the Lookup Service rather than discovered, scraped or enumerated directly.
- Resolution MUST be permissioned. Only authenticated Issuers MAY resolve a Business Wallet endpoint, and the Lookup Service MUST enforce the authorisation policy held in the Registry.
- The Lookup Service MUST NOT confirm the existence of a registered entity to an unauthenticated or unauthorised querier, to prevent enumeration of SMEs and sole traders.

Resolution of an endpoint MUST NOT by itself entitle an Issuer to deliver. The endpoint MUST enforce a consent or allow-list check at delivery time, so that it rejects credential offers from Issuers the Wallet Owner has not accepted.

## Consequences

Authorised Issuers can reliably find and reach Business Wallets for issuer-initiated flows, preserving interoperability. Business Wallets are not open relays: an endpoint is reachable only for Issuers the Wallet Owner has accepted, and invisible to everyone else. Engagement control returns to the Wallet Owner through opt-in registration and per-Issuer authorisation, and the credential spam surface is removed by permissioned resolution and the delivery-time consent gate. SMEs and sole traders receive these protections by default, with no security setup on their end, and enumeration risk is mitigated because the Lookup Service does not disclose entities to unauthorised queriers.

Wallet Providers are expected to implement registration and resolution, to be elaborated further via a conformance specification. Actors can verify conformance through testing against other implementations.

## Advice

Once merged, this is our consortium's decision. This does not mean all participants agree it is the best possible decision.
