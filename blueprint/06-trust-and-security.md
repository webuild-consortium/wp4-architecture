# Trust, Security and Governance

The previous chapter described the structure of the information stored in wallets and exchanged as attestations. This chapter describes the trust infrastructure that allows ecosystem participants to validate those attestations.

## Trust Ecosystem

The trust infrastructure for the EUDI and EBW ecosystem is based on three complementary processes: registration/onboarding of participants, notification of certain entities to the European Commission, and publication of Trusted Lists (or Lists of Trusted Entities) that provide cryptographic trust anchors for validation. 

## Establishing Trust Between Participants

WE BUILD defines the onboarding processes (how entities get registered), the trust framework (which rules apply), the PKI architecture (which certificates are used and how), the APIs used to query trust information programmatically, and the trust evaluation logic used by participants at runtime.

The infrastructure is based on the Trusted List model defined in the eIDAS Regulation and the ARF. It follows the European model in which a List of Trusted Lists (LoTL) points to Trusted Lists. Each Trusted List contains entries for authorised participants such as PID Providers, Attestation Providers (QEAA, PuB-EAA, non-qualified EAA), Wallet Providers, and Relying Parties.

The onboarding processes define how participants join the ecosystem. This includes how:
- **Relying Parties** register, accept policies and configure access controls
- **PID and Attestation Providers** register, declare supported attestation types and obtain registration and access certificates
- **Wallet Providers** register and issue wallet instance attestations
- **Trust Service Providers** register and publish relevant certificates

Once onboarding is completed, participants use the trust infrastructure to evaluate each other during normal operation. WE BUILD therefore defines a set of trust evaluation scenarios covering how participants verify each other at runtime.

These scenarios include: 
- a Wallet Unit evaluating a Credential Issuer before requesting a PID or attestation
- a Credential Issuer evaluating the Wallet Unit before issuing
- a Wallet Unit evaluating a Relying Party before presenting attributes
- a Relying Party evaluating presented credentials (PID, QEAA, PuB-EAA, non-qualified EAA)
- discovery and consumption of the LoTL and TLs.

For detailed information on authorities, registries and responsibilities, see [Appendix C - Trust Ecosystem](#appendix-c-trust-ecosystem).

For reference on relying party access certificates and relying party registration certificates, see the [RPAC/RPRC documentation](#rpacrprc-documentation).

### Trust infrastructure architecture (overview)

In the [Appendix - Trust Ecosystem](../appendix-trust-ecosystem.md) there is a diagram that summarises the roles of Member State and European Commission, the split between registration and notification, and how Trusted Lists and the LoTL are produced and consumed. A simplified version used in WE BUILD is shown below.

````mermaid
graph TB
    subgraph MS["weBuild Registry"]
        Registrar[Registration Service]
        TLProvider[Trusted List Provider]
        APTL[Attestation Provider TLs]
    end

    subgraph Entities["weBuild Participant"]
        AP[Attestation Provider]
        WP[Wallet Provider]
        RP[Relying Party]
    end

    subgraph TL["weBuild Trusted List Provider"]
        LoTLPublication[List of Trusted Lists]
    end

    AP -->|Register| Registrar
    WP -->|Register| Registrar
    RP -->|Register| Registrar

    LoTLPublication -->|references|TLProvider
    LoTLPublication -->|references|APTL

    style MS fill:#e1f5ff
    style TL fill:#fff4e1
    style Entities fill:#e8f5e9
````
WE BUILD participants select the registry in which they register.

## Revocation 
Revocation ensures that attestations that are no longer valid can no longer be trusted or used. 

WE BUILD distinguishes between attestation revocation, which is handled by issuers, and revocation or withdrawal of providers and services, which is reflected in the trust infrastructure.

### Technical realisation
Revocation of PID, EBWOID and attestations is implemented by issuers. In WE BUILD, attestation revocation follows the agreed mechanism defined in the [ADR on Attestation Revocation](https://github.com/webuild-consortium/wp4-architecture/blob/main/adr/attestation-revocation-mechanism.md), based on the IETF Token Status List and aligned with OpenID4VC HAIP.

Short-lived attestations (valid for 24 hours or less) are not subject to revocation.

Revocation or withdrawal of providers and services is reflected in the trust infrastructure through status changes in Trusted Lists and, where applicable, invalidation of certificates. 

### Provider Obligations
To maintain a trusted ecosystem, PID and EBWOID providers agree to:
  * Define and publish revocation policies.
  * Ensure that only the issuing authority can revoke its attestations.
  * Publish revocation status information within a reasonable time frame.

### Conditions for Mandatory Revocation
According to the rules, a provider must revoke without delay if:
 * The holder explicitly requests it.
 * The security of the wallet app itself (the unit certificate) is compromised.
 * Any of the specific situations defined in the provider's public policy occur.

