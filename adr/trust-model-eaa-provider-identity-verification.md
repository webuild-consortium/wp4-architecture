# ADR: A Complementary Hybrid Trust Model for EAA Provider Identity Verification

**Authors:**

- Werner Folkendt
- Niels Klomp
- Lal Chandran
- Eelco Klaver
- George Padayatti
- Florin Coptil

**Related ADRs:** This ADR builds upon and reconciles [EAA Provider Identity Verification via Attestation Chaining](./EAA-Chaining.md) and [EAA provider identity verification based on live key-binding query](./eaa-key-binding-authzen.md).

## 1. Context and Problem Statement

Architectural discussions have yielded two distinct models for EAA Provider identity verification:

1. **[The Chaining Model](./EAA-Chaining.md):** A decentralized approach that embeds a full, signed credential (like the EBWOID) into the EAA header. It provides a self-contained, offline-verifiable proof of identity, making it ideal also for archival and offline verifiable attestations, primary trade-off is a larger EAA payload size and a fresh cached trusted list if no internet calls are possible.

2. **[The Central Registry API Model](./eaa-key-binding-authzen.md):** A centralized approach that uses a lightweight EAA containing only the issuer's identifier and public key. It relies on the verifier making a live API call to a national registry to confirm the key-binding. It offers a minimal payload but is dependent on the creation of currently non-existent historical query APIs across all Member States.

Neither model alone optimally serves the entire spectrum of We Build use cases. The chaining model model may be inefficient for high-volume transactional checks, while a Central Registry API model may lack future resilience requirements due to several single point of failures, and does not satisfy the short availability constraints within We Build. Forcing the ecosystem to choose one would create unnecessary limitations and block important scenarios.

This ADR establishes a consensus architecture that accommodates both, providing maximum flexibility and future-proofing.

## 2. The Architectural Decision: Adopt a Complementary Hybrid Model

Instead of viewing the [Chaining Model](./EAA-Chaining.md) and the [Central Registry API Model](./eaa-key-binding-authzen.md)) as mutually exclusive competitors, we will adopt a **complementary hybrid architecture**. This approach provides a robust, flexible, and pragmatic path forward, allowing the ecosystem to leverage the strengths of both models while mitigating their respective weaknesses.

A verifier's wallet must be built to handle both patterns seamlessly. Upon receiving an EAA, it would inspect the header:

* If a full, chained credential (like an EBWOID) is present, it performs the offline, self-contained cryptographic validation as specified in the [Chaining Model](./EAA-Chaining.md).

* If only a lightweight identifier and key are present, it initiates the online query to the central registry's API as specified in the [Central Registry API Model](./eaa-key-binding-authzen.md).

This hybrid design empowers EAA issuers to select the optimal trust mechanism on a per-use-case basis, as defined in the attestation's rulebook.

## 3. Consequences of the Decision

### What Becomes Easier or Possible?

* **Empowers Use-Case Designers:** This approach removes the decision from a small architecture group and places it in the hands of the business and legal experts designing the specific attestations. They can choose the model that best fits their specific security, compliance, and operational constraints.

* **Achieves We Build's Core Objectives:** A hybrid model allows the consortium to fulfill two key objectives from the grant agreement. We can fully "test out and give feedback" on both architectural patterns. We can pilot the short-term viable Chaining Model for our MVP+, while simultaneously helping to "identify the regulatory, semantic, and technical gaps" that currently block the Central Registry model (like the lack of a historical query API). This provides invaluable, real-world feedback to the European Commission.

* **Future-Proofs the Architecture (Extensibility):** This model is not a closed system. The chaining mechanism is inherently extensible. For example, to integrate with an EBSI-based system, a new EBWOID variant could be defined that chains a `did:ebsi` identifier. This same pattern allows for the future integration of other decentralized trust infrastructures in parallel, without requiring a forklift upgrade of the entire ecosystem.

* **Short-Term Availability for We Build:** If wallet providers support attestation chaining (a prerequisite for EBWOID verification), a robust and compliant solution for the MVP+ pilots can be made available quickly.

### What Becomes More Difficult or Requires Care?

* **Implementation Effort for Wallet Providers:** Wallet providers would need to implement the verification logic for both models.
    * **Mitigation:** This is less burdensome than it appears. The verification logic for the Chaining Model (validating an X.509-based chain) is a mandatory prerequisite for any wallet that needs to verify the EBWOID itself. The work to implement the [Chaining Model](./EAA-Chaining.md) is therefore largely a sunk cost. The additional effort is to implement the client-side logic for the [Central Registry API Model](./eaa-key-binding-authzen.md) API query.

## 4. Advice

Once merged, this is our consortium’s decision. This decision represents a consensus achieved through extensive analysis of two competing but valuable architectural patterns, providing a flexible and pragmatic path forward for the We Build project and the broader EUDI Wallet ecosystem.
