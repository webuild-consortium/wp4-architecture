# Trust, Security & Governance

## Trust Ecosystem

The trust infrastructure for the EU Digital Identity and European Business Wallet ecosystem rests on three distinct but complementary processes: **registration/onboarding** of participants, **notification** of certain entities to the European Commission, and **publication of Trusted Lists** (or Lists of Trusted Entities) that provide cryptographic trust anchors for validation. WE BUILD aligns with the [EUDI Wallet Architecture and Reference Framework (ARF)](https://eudi.dev/) and the trust-infrastructure model described in the WP4 Trust Group deliverables.

## How do participants in the WE BUILD wallet ecosystem verify that other participants are who they say they are, and that they are authorised to do what they claim?

To answer the above question we will in WE BUILD define the onboarding processes (how entities get registered), the trust framework (what rules apply), the PKI architecture (which certificates are used and how), the APIs (how systems query trust information programmatically), and the trust evaluation logic (how each participant checks the others at runtime).

The infrastructure is based on the Trusted List model defined by the eIDAS Regulation and the EUDI Wallet Architecture and Reference Framework (ARF). It builds on the well-established European model where a List of Trusted Lists (LoTL), points to Trusted Lists. Each Trusted List contains entries for the entities that have been authorised to operate, such as PID Providers, Attestation Providers (QEAA, PuB-EAA, non-qualified EAA), Wallet Providers, and Relying Parties.

This includes how Relying Parties (RPs) register, accept policies, and set up access controls; how PID Providers and Attestation Providers (EAA, QEAA, PuB-EAA) registers, declare attestation types, obtain access and registration certificates, and get their trust anchors published in Trusted Lists; how Wallet Providers register, issue wallet instance attestations; and how Trust Service Providers register and submit certificates.

Building on the onboarding foundation, we have recently developed a complete set of trust evaluation use cases that describe how participants actually verify each other at runtime.
These cover the Wallet Unit evaluating a Credential Issuer before requesting a PID or attestation; the Credential Issuer evaluating the Wallet Unit before issuing; the Wallet Unit evaluating a Relying Party before presenting attributes; the Relying Party evaluating presented credentials (PID, QEAA, PuB-EAA, non-qualified EAA); and the cross-cutting process of Trusted List discovery and consumption (how any participant finds and uses the LoTL and TLs).

For detailed information on authorities, registries, responsibilities etc read [Appendix C - Trust Ecosystem](#appendix-c-trust-ecosystem) that describes everything in more detail.

### Relation to QTSP and Trust Registry

WE BUILD will adopt and cross-reference the following policy and attestation structures:

- **EC Attestation Rulebooks, Attestation Schemas, and Attestation Catalogues** (and EU CIR 2025/1569 attestation schemes and catalogues where applicable).
- **ETSI TS 119 471** QEAA Trust Service Policy and Electronic Attestation of Attributes Policies (EAAPs).

The blueprint aims to describe how WE BUILD structures and cross-references Rulebooks, Schemas, and EAAPs with trust marks and ETSI-based trusted lists used in the wallet ecosystem.

### Trust infrastructure architecture (overview)

In the [Appendix C - Trust Ecosystem](#appendix-c-trust-ecosystem) there is a diagram that summarises the roles of Member State and European Commission, the split between registration and notification, and how Trusted Lists and the LoTL are produced and consumed. The simplified version for WE BUILD:

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

WE BUILD participants willing to register are going to be able to select a registry in which they are going to be registered. 

## Revocation and Trust Status Framework
In order to fulfill the Article 5 baseline established in [Revocation Mandate](../02-regulatory-alignment.md#revocation-mandate), the consortium has identified the following operational scenarios.

The revocation mechanism for PID, EBWOID, and for person wallet instances (Wallet Units) **is a critical component** of the European Digital Identity Wallet ecosystem. 

### Operational Revocation Scenarios

The following scenarios align with and extend the revocation baseline defined in the [EUDI Wallet Architecture and Reference Framework (ARF)](https://eudi.dev/). The ARF specifies: (a) **Topic 7** (Attestation revocation and revocation checking), including revocation methods (Attestation Status List, Attestation Revocation List, or short-lived attestations), irreversibility of revocation, and mandatory revocation when security is compromised or upon user request; (b) **Topic 38** (Wallet Unit revocation) and **ARF Section 6.5.4.2**, which require Wallet Unit revocation at least when the user requests it (e.g. loss or theft), when the PID Provider requests it (e.g. death of the natural person), when the security of the Wallet Unit is breached, or when the Wallet Solution is suspended or withdrawn; (c) **Article 5** of the European Digital Identity Regulation, under which a PID Provider must revoke a PID when the Wallet Unit to which it was issued is revoked. **EBWOID** (European Business Wallet Owner Identification Data) revocation follows the same principles as PID revocation where applicable for the European Business Wallet; any additional provisions are as defined in the European Business Wallet regulation and related ARF updates.

It is necessary to identify and categorize all potential situations that necessitate the invalidation of a PID, an EBWOID, or a Wallet. The resulting framework should address a wide range of real-world events, from user-initiated requests to administrative actions and security incidents.
<!-- TODO, categorize under Security and Unauthorized Access, Lifecycle and Inactivity Management, Compliance and Service Terms and End-of-Life Events? -->

* **Explicit User Request:** A direct request from the holder or an authorized representative to revoke the relevant data.
   * _Example: A change in ownership of a company could be a reason for authorized representatives to revoke the EBWOID._
     
* **Data Inaccuracy or Modification:** Revocation initiated by the provider when the holder's underlying data is found to be inaccurate or has been officially modified.
   * _Example: The holder changes name and the PID needs to be reissued._
     
* **Regulatory Changes:** Revocation required by regulatory changes that result in an incompatible PID/EBWOID, such as required attribute added, attribute removed or renamed.
   * _Example:  A new obligatory attribute is introduced in the EBWOID following a new regulation._
     
* **Loss, Theft, or Compromise:** Notification that the holder's credentials or authentication device have been lost, stolen, or otherwise compromised.
   * _Example: Theft of a YubiKey, potentially allowing adversaries to use a business's wallet_
     
* **Provider Revocation:** Revocation due to revocation of wallet unit certificate (e.g. as a result of Wallet Provider compromise) or PID/LPID Provider certificate.
   * _Example: A Wallet Provider fails to meet mandatory security compliance standards, resulting in the withdrawal of its authorization to operate in the eIDAS Trust Framework and is thus not allowed to provide wallet solutions anymore._
     
* **Abusive or Fraudulent Use:** Detection of abusive, fraudulent, or unauthorized activities associated with the identity data.
   * _Example: An economic operator observes that the business wallet is used for unauthorized transactions by representatives of the company._
   * _Example2: A law enforcement agency asks the PID provider by court order for revocation of a criminal user's PID._
     
* **Prolonged Inactivity:** Revocation/Cancelling of reissuance due to extended periods of non-use, as defined by the provider's policy.
   * _Example: A new PID is issued to replace an expiring one, but the holder fails to actively accept or "pick up" the new credential within the allowed grace period, leading the provider to revoke/cancel the unclaimed PID to prevent it from remaining in a pending state._
     
* **Violation of Service Terms:** A breach of contractual obligations, service terms of use, or other applicable regulations by the holder.
   * _Example: The EBWOID Issuers terms of service specify an annual fee for issued attestations which the business fails to pay._
     
* **End-of-life Revocation Events:** End of life lifecycle events for natural respectively legal persons.
  * _Example PID: Death of holder_
  * _Example EBWOID: Termination or dissolution of the legal entity/business activity such as liquidation of a company._

#### Technical realisation

Revocation of **PID or attestation data** itself is implemented by Issuers through issuer-specific mechanisms (e.g. revocation lists). **Revocation or withdrawal of providers or services** is reflected in the trust infrastructure as follows: (1) status changes in **Trusted Lists / Lists of Trusted Entities** (e.g. service status values, withdrawn or suspended), and (2) where applicable, invalidation of access or unit certificates. Wallet Units and Relying Parties SHALL evaluate Trusted Lists and registry information per the referenced ETSI procedures and ARF trust-evaluation requirements (e.g. ISSU_24, ISSU_24a, ISSU_34a, RPA_04, RPRC_16, RPRC_21) so that revoked or withdrawn providers and services are not trusted. Formats and procedures are specified in the WP4 Trust Group trust-infrastructure schema and ETSI trusted lists implementation profile.

#### Provider Obligations
To maintain a trusted ecosystem, PID and EBWOID providers agree to:
  * Publish clear policies: state exactly when and how data is revoked.
  * Own the Authority: only the original issuer can materially revoke the data it issued.
  * Notify holders promptly: if data is revoked, the holder must be informed of the reason within 24 hours via a secure channel.
  * Be Irreversible: Once identity data is revoked, it stays revoked to prevent fraud.

#### Conditions for Mandatory Revocation
According to the rules, a provider must revoke without delay if:
 * The holder explicitly requests it.
 * The security of the wallet app itself (the unit certificate) is compromised.
 * Any of the specific situations defined in the provider's public policy occur.
