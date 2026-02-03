# Revocation Mechanism

**Authors:**

- Artur Reaboi, e-Governance Agency, Republic of Moldova
- Alexandru Cozlovschi, e-Governance Agency, Republic of Moldova
- Fabrizio Notarnicola, InfoCamere, Italy
- Alessandro Bazzolo, InfoCamere, Italy

## Context

Revocation is the process by which an attestation (including PID/EBWOID) is invalidated before its natural expiry so that it can no longer be trusted or used. While short-lived attestations (expiring in 24 hours or less) do not require revocation, long-term attestations need a standardized mechanism to handle invalidation due to reasons such as lost devices, data inaccuracy, or regulatory changes.

The architecture must ensure that the revocation status check preserves the privacy of the Wallet Holder (herd privacy) and allows for scalable implementation,. Additionally, the solution must align with the OpenID4VC HAIP 1.0 specifications.

## Decision

The WE BUILD project adopts the [IETF Token Status List](https://datatracker.ietf.org/doc/draft-ietf-oauth-status-list/)  as the mechanism for semantics, formats, and protocols regarding revocation:

* **Wallet Providers** MUST implement revocable Wallet Unit Attestations (WUAs).
* **Issuers** (PID/EBWOID Providers, EAA Providers, including QEAA, Pub-EAA) MUST implement revocable attestations.
* Both, **Wallet Providers** and **Issuers** MUST randomly assign a status list and random index within it for revocable WUAs and attestations before signing them, all in batches.
* **Issuers** MUST regularly check the status of WUA and, if a WUA is revoked, the Issuer MUST revoke the corresponding PIDs/EBWOIDs.
* **Relying Parties** SHOULD check the revocation status via a Revocation Status Service. If reliable information is unavailable, they SHOULD perform a risk analysis rather than a mandatory failure.

## Consequences

### Easier:
* Alignment with OpenID4VC HAIP 1.0 for SD-JWT format is ensured, facilitating interoperability.
* Relying Parties have a standardized format to check for validity across different issuers.

### More Difficult:
* To ensure performance and privacy, Issuers must implement complex state management. One way to do it is to pre-allocate random indices in batches, rather than simple sequential generation.
* As Issuers have the sole right to revoke PIDs/EBWOIDs, Authentic Sources and Issuers must establish protocols to notify the Issuer of events requiring revocation (e.g., data changes or lost devices), as they cannot revoke the attestation directly.

### Risks:
*  Offline verification scenarios require Relying Parties to cache revocation lists. To address this, Issuers should include expiration dates and time-to-live (TTL) in revocation info to drive caching decisions.

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice:

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice

