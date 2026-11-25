# ADR: Point-in-Time Validity for Chained Attestations

**Authors:**

- Werner Folkendt, Robert Bosch GmbH, Germany
- Coptil Florin, Robert Bosch GmbH, Germany

**Related ADRs:** ADR-168 (EAA Provider Identity Verification via Attestation Chaining), ADR-371 (A Complementary Hybrid Model for EAA Provider Identity Verification)

## 1. Context and Problem Statement

ADR-168 establishes a "Chaining Model" where an EAA's header contains the issuer's full credential (e.g., the EBWOID), creating a self-contained proof of identity. This model is essential for supporting offline and archival verification.

However, a critical challenge arises from the lifecycle of credentials and the threat of key compromise.

**The Core Problem:** An issuer's EBWOID may be short-lived (e.g., valid for one year) while the EAA it was used to sign has a much longer validity. When a verifier encounters an EAA with a chained EBWOID that is now expired or administratively revoked (e.g., due to key rotation or headquarters relocation), they must be able to determine if the EBWOID was valid **at the moment the EAA was issued**.

Furthermore, if an EAA Provider's private signing key is compromised, the provider will revoke their EBWOID. An attacker holding the compromised key could attempt to sign a fraudulent EAA and backdate its self-asserted issuance date (`iat`) to a past date when the key was still valid.

To prevent this key-compromise backdating attack, the verifier cannot rely on the self-asserted `iat` claim in the EAA payload. The verifier needs a cryptographically secure, unforgeable proof of the **exact time of signing**. This ADR defines the mechanism to achieve this **Point-in-Time Validity** at issuance.

## 2. The Architectural Decision: Trusted Timestamps

To achieve Point-in-Time Validity and prevent backdating fraud, the issuance process for chained EAAs **MUST** secure the signature using a **Trusted Timestamp (TSA)**.

*   **The Mechanism:** The EAA Provider obtains a cryptographically signed timestamp token from an independent, trusted Time-Stamping Authority (TSA) over the EAA signature. This timestamp token is embedded directly within the EAA's signature block.
*   **The Verification Logic:**
    *   The Trusted Timestamp proves the exact date and time the EAA was signed, making the signing time unforgeable.
    *   If the issuer's EBWOID has been revoked, the verifier retrieves the revocation list (e.g., CRL or OAuth Status List) from the QTSP. This list publishes the **revocation time** and **revocation reason** (e.g., `keyCompromise` vs. administrative reasons).
    *   The verifier compares the EAA's Trusted Timestamp against the EBWOID's revocation time:
        *   If the timestamp is **before** the revocation time (or if the revocation was purely administrative), the signature is accepted as valid.
        *   If the timestamp is **after** the revocation time and the reason was `keyCompromise`, the signature is rejected as a post-compromise forgery.
*   **Simplification Benefit:** This approach **eliminates the need to fetch and embed revocation proofs (like OCSP responses) at the moment of issuance.** The issuer only needs to obtain a trusted timestamp, significantly reducing issuance-side complexity and runtime dependencies.

## 3. Implementation Options for Timestamps

The level of trust in the timestamp determines the legal and business value of the proof. The architecture allows for flexibility, enabling issuers to choose a method appropriate for their use case:

**a) Qualified Timestamping (Highest Trust)**
*   **Mechanism:** For each EAA, the issuer's wallet makes a live request to an external, qualified Time-Stamping Authority (TSA). The TSA returns a legally-binding, signed timestamp token that is embedded with the signature.
*   **Use Case:** Legally binding documents, high-value credentials, government-issued attestations.
*   **Trade-off:** Highest trust and legal value, but incurs a per-transaction cost and a dependency on the TSA service during issuance.

**b) Batch Timestamping (Balanced Trust and Cost)**
*   **Mechanism:** The issuer signs a large number of EAAs locally throughout a set period. The system then creates a single hash representing the entire batch of signatures and obtains a single qualified timestamp for that batch hash. When an EAA is presented, it is accompanied by the batch timestamp and a proof of its inclusion in the batch.
*   **Use Case:** High-volume issuance where qualified trust is required but per-transaction costs are prohibitive (e.g., product passports).
*   **Trade-off:** Balances high trust with very low cost, but adds complexity to the issuance and verification logic.

**c) Wallet-Internal Timestamping (Lowest Trust)**
*   **Mechanism:** The EBW itself, as a certified and integrity-protected device, generates and signs a timestamp using its own internal clock.
*   **Use Case:** Low-risk or informational attestations where the risk of the issuer tampering with their own clock is considered negligible.
*   **Trade-off:** No external cost or dependency, but offers the lowest level of trust as it is not provided by a neutral third party.

## 4. Decision

The architecture will recommend and support all three timestamping mechanisms. Rulebooks for specific attestations MUST define the minimum required level of timestamp trust. For any attestation intended to have long-term legal value or support compliance use cases, a qualified timestamp (either per-signature or per-batch) is mandatory.

## 5. Consequences of the Decision

### 5.1 What becomes easier?

*   **True Archival Verification:** This decision makes the promise of ADR-168 a practical reality. It provides a standardized, interoperable mechanism to verify the authenticity of credentials over their entire lifecycle.
*   **Dramatic Issuance Simplification:** By relying solely on Trusted Timestamps and standard revocation list metadata (time/reason), EAA Providers do not need to fetch and package OCSP/CRL snapshots at issuance.
*   **Clarity for Implementers:** Wallet providers and verifiers have a clear, standards-based path (PAdES/CAdES/XAdES) for implementing validation logic.
*   **Flexible Trust Models:** EAA issuers can choose the most appropriate and cost-effective timestamping method based on the specific requirements of their attestation.

### 5.2 What becomes more difficult?

*   **Dependency on Timestamp Services:** During issuance, the EAA Provider's system has a live dependency on an external TSA (unless using local wallet-internal timestamps). An outage in the TSA service could temporarily halt the issuance of timestamped EAAs.
*   **Increased Payload Size:** The embedded timestamp tokens will increase the overall size of the EAA signature block.
*   **Verification Logic:** While based on standards, the validation logic is slightly more complex than a simple signature check, requiring verifier wallets to parse the timestamp and compare it against the revocation metadata.

### Annex
# Cryptographic Attack Vector: Key-Compromise Backdating in Wallet Ecosystems

## 1. User Story & Attacker Persona
*   **The Attacker:** A malicious hacker employed by a legitimate Supplier organization with administrative access to the Supplier’s EBW.
*   **The Objective:** Divert financial payments from a Relying Party into a private account using a forged IBAN attestation carrying the hacker's personal account number.
*   **The Breach:** The hacker extracts the Bank's private EAA signing key (`key_A`) and registers a temporary, compliant "Attacker EBW" to masquerade as an active issuing node.

## 2. The Real, Successful Attack Vector (Key-Compromise Backdating)
*   The attacker avoids using their own "Attacker EBWOID" (which would trigger an identity mismatch). Instead, they embed the **Bank's genuine, public `EBWOID_Bank`** (which they obtained from a previous transaction) in the EAA header.
*   They sign the forged EAA with the stolen private key `key_A`, and **backdate the `iat` to 2024** (when the key was valid).
*   The Supplier's wallet accepts and stores the EAA because the backdated `iat` makes the `EBWOID_Bank` appear valid during the `HW-TV-01` check.
*   When presented to the Relying Party in 2026, the verifier finds that:
    1.  The issuer in the payload (`EUID_Bank`) matches the subject in the chained EBWOID (`EUID_Bank`). **Match!**
    2.  The signature validates perfectly against the public key inside the EBWOID. **Match!**
    3.  The EBWOID chains to the TLoL. **Match!**
    4.  The EAA itself is not revoked. **Match!**
    5.  Under `RP-TV-06`, the verifier is forbidden from checking the current status of the EBWOID.
*   **Result:** All checks pass. The fraudulent IBAN is accepted as 100% genuine.

## 3. Why the Wallet Natively Fails to Block This (Without Timestamps)
This attack succeeds because standard wallet-to-wallet protocols cannot verify the exact time of signing without an external, independent trust anchor.
*   By backdating the `iat` claim, they bypass historical checks.
*   Without checking the *current* status of the EBWOID, they never learn that the key was revoked for compromise.
*   **The Solution:** Embedding a **Trusted Timestamp (TSA)** in the EAA signature block at issuance is the mandatory production control required to cryptographically lock the signing time and prevent this fraud.
