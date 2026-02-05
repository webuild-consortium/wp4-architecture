# Trust, Security & Governance

## Trust Ecosystem
### Relation to QTSP and Trust Registry.
Todo: We could describe how WE BUILD will adopt the QEAA Trust Service Policy document structure. There are currently the Attestation Rulebooks, Attestion Schemas and Attestation Catalogues specified by the EC, whilst ETSI TS 119 471 has specified the QEAA Trust Service Policy and the EAAPs. Furthermore, EU CIR 2025/1569 specifies attestation schemes and catalogues. It could be useful to describe how WE BUILD will structure and cross-reference the Rulebooks, Schemas and EAAPs.

## Security Measures
Signatures, authentication, key lifecycle.

The wallet secure cryptographic application/device (WSCA/WSCD) architecture is to be specified by the Architecture and Wallets groups, and in the case of remote WSCA/WSCD, together with the QTSP group.

## Revocation and Trust Status Framework
In order to fulfill the Article 5 baseline established in [Revocation Mandate](../02-regulatory-alignment.md#revocation-mandate), the consortium has identified the following operational scenarios.

A robust and harmonized revocation mechanism for  Personal Identification Data (PID) and European Business Wallet Owner Identification Data (EBWOID) is a critical component of the European Digital Identity Wallet ecosystem. 
### Operational Revocation Scenarios
First we need to identify and categorize all potential situations that necessitate the invalidation of a PID or EBWOID. This analysis ensures that the resulting framework can address a wide range of real-world events, from user-initiated requests to administrative actions and security incidents. 
<!-- TODO, categorize under Security and Unauthorized Access, Lifecycle and Inactivity Management, Compliance and Service Terms and End-of-Life Events? -->

* **Explicit User Request:** A direct request from the user or an authorized representative to revoke their data.
   * _Example: A change in ownership of a company could be a reason for authorized representatives to revoke the EBWOID._
     
* **Data Inaccuracy or Modification:** Revocation initiated by the provider when the holder's underlying data is found to be inaccurate or has been officially modified.
   * _Example: A user changes their last name and the PID needs to be reissued._
     
* **Regulatory Changes:** Revocation required by regulatory changes that result in an incompatible PID/EBWOID, such as required attribute added, attribute removed or renamed.
   * _Example:  A new obligatory attribute is introduced in the EBWOID following a new regulation._
     
* **Loss, Theft, or Compromise:** Notification that the user's credentials or authentication device has been lost, stolen, or otherwise compromised.
   * _Example: Theft of a YubiKey, potentially allowing adversaries to use a business's wallet_
     
* **Provider Revocation:** Revocation due to revocation of wallet unit certificate (e.g. as a result of Wallet Provider compromise) or PID/LPID Provider certificate.
   * _Example: A Wallet provider fails to meet mandatory security compliance standards, resulting in the withdrawal of their authorization to operate in the eIDAS Trust Framework and is thus not allowed to provide wallet solutions anymore._
     
* **Abusive or Fraudulent Use:** Detection of abusive, fraudulent, or unauthorized activities associated with the identity data.
   * _Example: An economic operator observes that the business wallet is used for unauthorized transactions by representatives of the company._
   * _Example2: A law enforcement agency asks the PID provider by court order for revoation of a criminal users' PID._
     
* **Prolonged Inactivity:** Revocation/Cancelling of reissuance due to extended periods of non-use, as defined by the provider's policy.
   * _Example: A new PID is issued to replace an expiring one, but the user fails to actively ano,,ccept or "pick up" the new credential within the allowed grace period, leading the         provider to revoke/cancel the unclaimed PID to prevent it from remaining in a pending state._
     
* **Violation of Service Terms:** A breach of contractual obligations, service terms of use, or other applicable regulations by the holder.
   * _Example: The EBWOID Issuers terms of service specify an annual fee for issued attestations which the business fails to pay._
     
* **End-of-life Revocation Events:** End of life lifecycle events for natural respectively legal persons.
  * _Example PID: Death of holder_
  * _Example EBWOID: Termination or dissolution of the legal entity/busienss activity such as liquidation of a company._


#### Provider Obligations
To maintain a trusted ecosystem, PID and EBWOID providers agree to:
  * Publish clear policies: Tell the public exactly when and how you revoke data.
  * Own the Authority: Only the original issuer can revoke the data they issued.
  * Notify users fast: If data is revoked, the user must be told why within 24 hours via a secure channel.
  * Be Irreversible: Once identity data is revoked, it stays revoked to prevent fraud.

#### Conditions for Mandatory Revocation
According to the rules, a provider must hit the revocation button without delay if:
 * The user explicitly asks for it.
 * The security of the wallet app itself (the unit certificate) is compromised.
 * Any of the specific situations defined in the provider's public policy occur.

## Relying Party Registration & Access Certificates 
To be authored by Trust Group (registration) and the QTSP group (certificate issuance). Describes how verifiers registers and obtain the access certificates needed to securely identify themselves to a wallet

## Validation Functions for Relying Parties 
To be authored by the PID Providers group (for PID and LPID/EBW-OID) and the QTSP group (for EAA). Details the services provided to help Relying Parties authenticate and validate the person identification data and attestations they receive.

## Governance Responsibilities
Who owns what in the consortium.


