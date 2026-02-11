# Wallet Unit Attestation and Lifecycle Management

**Status**: Proposed  
**Date**: 11 February 2026  
**Authors**: WP4 Architecture  

- Lal Chandran, iGrant.io, Sweden
- Sander Dijkhuis, Cleverbase, the Netherlands
- George J Padayatti, iGrant.io, Sweden

## Context

The European Business Wallet represents an economic operator and operates within a cloud or on-premise environment under regulatory oversight derived from revised eIDAS and related Implementing Regulations.

Trust in a Business Wallet must be established at two distinct levels:

1. Cybersecurity assurance in the wallet’s secure execution and key management environment.
2. Organisational entity authentication assurance (cf. ISO/IEC 29115) represented by the European Business Wallet Owner ID (EBWOID).

At present, the architecture does not formally define:

- A Wallet Unit Attestation (WUA) model for European Business Wallet.
- A clear lifecycle model governing Wallet Unit states.
- The downgrade and revocation semantics between structural and identity trust.

Without an explicit lifecycle and attestation model, revocation handling, issuance eligibility and cross-border interoperability remain ambiguous.


## Decision

The European Business Wallet SHALL introduce:

1. A mandatory Wallet Unit Attestation (WUA).
2. A defined lifecycle model governing Wallet Unit state transitions.

### Wallet Unit Attestation (WUA)

A Wallet Unit Attestation is a signed object issued by the Wallet Provider that:

- Binds the Wallet Unit to a secure cryptographic environment.
- Contains public keys used for credential binding.
- Includes validity and revocation information.
- Is presented to Issuers and Attestation Providers.
- Is not presented to Relying Parties unless explicitly required.

A valid WUA is required for a Wallet Unit to operate within the EBW ecosystem.

### Wallet Unit Lifecycle Model

The Wallet Unit SHALL follow the lifecycle states defined below:

**UNINSTALLED**  

No wallet instantiated. No cryptographic material. No WUA. No EBWOID.

**INSTALLED**  

Wallet software deployed and environment prepared, but no WUA issued.

**OPERATIONAL**  

Valid WUA present. Structural trust established. EBWOID not yet acquired or pending.

**VALID**  

Valid WUA and valid EBWOID present. Fully functional for regulated and cross-border use.

### State Transitions

- **UNINSTALLED → INSTALLED**  
  Organisation instantiates the software.

- **INSTALLED → OPERATIONAL**  
  Wallet Unit acquires the WUA.

- **OPERATIONAL → VALID**  
  Wallet Unit acquires the EBWOID.

- **VALID → OPERATIONAL**  
  EBWOID revoked or expired.

- **OPERATIONAL or VALID → INSTALLED**  
  WUA revoked or expired.

- **INSTALLED → UNINSTALLED**
   Uninstallation or decommissioning of a WU, for e.g. during porting from one service provider to other.

Structural trust (WUA) is foundational. Identity trust (EBWOID) depends upon it. A Wallet Unit cannot be VALID without a valid WUA.

## Consequences

- Cybersecurity assurance and Organisational entity authentication assurance are explicitly separated.
- Revocation of WUA immediately suspends infrastructural legitimacy.
- Revocation of EBWOID suspends identity validity while preserving structural trust.
- Issuers gain a clear rule for issuance eligibility.
- Lifecycle handling becomes testable within ITB and conformance specifications.
- Cross-border interoperability is strengthened through explicit state semantics.
- Wallet Providers are expected to implement this which will be elaborated on further, for.g. via a conformance specification.

This ADR establishes WUA and lifecycle management as mandatory architectural components of the European Business Wallet.
