# EAA Provider Identity Verification via Attestation Chaining

**Authors:**

- Werner Folkendt, Robert Bosch GmbH, Germany
- Florin Coptil, Robert Bosch GmbH

**Obsoletes:** N/A

## 1. Context and Problem Statement

The European Business Wallet (EBW) ecosystem will consist of millions of legal entities acting as Electronic Attestation of Attributes (EAA) Providers. A fundamental challenge is establishing a scalable and secure method for these providers to prove their identity to relying parties (verifiers) who need to validate the authenticity of an EAA.

The established eIDAS framework relies on Qualified Trust Service Providers (QTSPs) having their certificates listed in a national Trusted List (TLoL). However, it is not feasible for Member States to manage a TLoL containing millions of individual EAA Providers. This creates a trust gap: without being listed, how can an EAA Provider's identity be verified?

This Architectural Decision Record (ADR) defines a solution that is secure, scalable, and independent of any single project's infrastructure, addressing the following core requirements:

*   **Decentralized and Scalable:** The solution must not require every EAA Provider to be registered in a national TLoL.
*   **Provider Sovereignty:** EAA Providers must be able to use key pairs generated and managed within their own EBW to issue EAAs, without depending on external (remote) sealing services for every transaction.
*   **Long-Term Verifiability (Archival Support):** A verifier must be able to validate an EAA many years after its issuance, even if the original EAA Provider is offline or has ceased to exist. This necessitates a portable proof of identity that does not depend on a live connection to the issuer's domain.
*   **Trust Anchored in eIDAS:** The identity claim of an EAA Provider must ultimately be verifiable against a legally recognized trust anchor, which is a credential issued by a QTSP (i.e., the EBWOID).

## 2. The Architectural Decision: The Chaining Model

To meet these requirements, we will adopt a **"Chaining Model"**. This model embeds the necessary identity credentials directly within the header of each EAA, creating a self-contained, verifiable proof of the issuer's identity.

This decision entails the following architectural commitments:

1.  **The EBWOID as the Root of Trust:** The EBWOID, as a qualified credential issued by a QTSP, will serve as the trust anchor for the EAA Provider's identity. To facilitate this, the EBWOID credential **MUST** be extended to contain the public key (`signing_key`) of the EBW owner. This binds the owner's identity (EUID) to a specific key under the authority of a QTSP.

2.  **Chaining the EBWOID in the EAA Header:** Every EAA issued by an EBW owner **MUST** include the issuer's full EBWOID credential (containing their `signing_key`) in its header. This provides the verifier with all the necessary data to validate the issuer's identity and the EAA's signature.

3.  **Hierarchical Key Delegation (for Key Rotation):** To avoid the need for re-issuing the EBWOID for routine key rotations, an EAA Provider can self-issue a delegated "Issuing Attestation".
    *   This attestation binds a new, subordinate public key to the provider's primary identity.
    *   This self-issued attestation is signed by the primary `signing_key` from the EBWOID and includes the EBWOID in its own header.
    *   When issuing EAAs with the subordinate key, both the "Issuing Attestation" and the EBWOID are chained into the EAA header, creating a verifiable delegation chain.

## 3. Foundational Principle: Long-Term Validation (LTV)

A core principle underpinning this architecture is the requirement for **Point-in-Time Validation or Long-Term Validation (LTV)**. For any attestation, a verifier's wallet must be able to determine the validity of a credential and its signature chain *at the time the attestation was issued*, not at the current time.

This involves validating each credential in the chain (EAA, Issuing Attestation, EBWOID) against its respective validity period and historical revocation status at the moment of issuance. LTV is a baseline capability required for most We Build use cases involving archival, compliance, or legally binding records.

The specific mechanisms to achieve LTV, including the use of trusted timestamps and embedded revocation proofs, will be detailed in a separate, forthcoming ADR dedicated to this topic.

## 4. Consequences of the Decision

### What Becomes Easier or Possible?

*   **Massive Scalability without Administrative Overhead** The ecosystem can scale to millions of EAA Providers without creating an administrative bottleneck at national TLoLs. No EBW owner needs to register anywhere.
*   **Worldwide Verifiability** Every EBW Owner who has read access to the TLoL and trust the EU Supervisory Bodies can verify all received attestations.
*   **Immediate Viability:** This solution can be piloted and deployed rapidly, as it relies on existing PKI principles and standards. It does not require new EU-level legislation or the creation of new, complex, centralized API infrastructures across all Member States.
*   **Archival and Compliance:** The model inherently supports long-lived, non-revocable attestations (e.g.,supply chain attestations required for KyS and KyC, diplomas, product passports, material composition records), as verification is completely independent of the issuer's operational status.
*   **Provider Autonomy:** EAA Providers can issue attestations autonomously using their own wallets once they possess a valid EBWOID.
*   **Simplified Delegation:** The hierarchical model provides a natural and secure pattern for delegating authority, such as for Mandates, Power of Representation, or IoT device identities (e.g., "truck wallets").

### What Becomes More Difficult or Requires Care?

*   **EAA Payload Size:** Chaining the EBWOID and other attestations increases the size of the EAA header compared to models that only include an identifier. This trade-off of a larger payload is necessary to achieve offline and archival verifiability.
*   **Dependency on TLoL Caching:** For true offline verification, the verifier's wallet must have access to a reasonably recent, cached copy of the TLoL to validate the QTSP's root certificate.
*   **Standards Evolution:** This model requires proposing and adopting extensions to standards like IETF SD-JWT VC and relevant interoperability profiles to formalize the use of chained attestations in the header.

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
