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

The WE BUILD project adopts the [IETF Token Status List](https://datatracker.ietf.org/doc/draft-ietf-oauth-status-list/) as the mechanism for semantics, formats, and protocols regarding revocation.

## Consequences

### Easier:
* Alignment with OpenID4VC HAIP 1.0 for SD-JWT format is ensured, facilitating interoperability.
* Relying Parties have a standardized format to check for validity across different issuers.

### More Difficult:
* To ensure performance and privacy, Issuers must implement complex state management. One way to do it is to pre-allocate random indices in batches, rather than simple sequential generation.
* As Issuers have the sole right to revoke PIDs/EBWOIDs, Authentic Sources and Issuers must establish protocols to notify the Issuer of events requiring revocation (e.g., data changes or lost devices), as they cannot revoke the attestation directly.

### Risks:
*  Offline verification scenarios require Relying Parties to cache revocation lists. To address this, Issuers should include expiration dates and time-to-live (TTL) in revocation info to drive caching decisions.

### Impact (resulting from ADR High-Level Requirements):
* **Wallet Providers** MUST implement revocable Wallet Unit Attestations (WUAs).
* **Issuers** (PID/EBWOID Providers, EAA Providers, including QEAA, Pub-EAA) MUST implement attestation revocation for applicable attestations and that are valid for more than 24h.
* Both, **Wallet Providers** and **Issuers** MUST randomly assign a status list and random index within it for revocable WUAs and attestations before signing them, all in batches.
* **Wallet Providers** SHALL regularly verify that the security of the Wallet Unit is not breached or compromised and if so, and if the breach or compromise affects the trustworthiness or reliability of the Wallet Unit, the Wallet Provider SHALL immediately revoke the corresponding WUA(s).
* **PID/EBWOID Providers** MUST regularly check the status of WUA used during issuance and, if a WUA is revoked, the PID/EBWOID Provider SHALL immediately revoke the respective PIDs/EBWOIDs. Other attestation providers MAY decide to revoke the attestations their issued if the respective WUA is revoked.
* **Wallet Providers** SHOULD ensure their Wallet Units regularly check the revocation status of its PIDs, attestations, and WUAs, and notify the User if any is revoked.
* **Relying Parties** SHOULD check the revocation status via a Revocation Status Service. If reliable information is unavailable, they SHOULD perform a risk analysis rather than a mandatory failure.

## Advice

Once merged, this is our consortium’s decision. This does not mean all participants agree it is the best possible decision.

In the decision making process, we have heard the following advice:
- 2026-02-04, Jonas Toeniss, Brønnøysundregistrene (BRC), Norway: Move Impact items to Consequences section
- 2026-02-13, Feedback in WP4 Architecture meeting: Clarify that regular check of WUA revocation is a MUST only for PID/EBWOID Providers
