**POSITION PAPER:  
SECURING THE BUSINESS VALUE OF THE EUROPEAN BUSINESS WALLET (EBW)**

*Restoring Critical Industry/Economy Capabilities and Enabling Scalable Trust Chaining in the EBW Regulation*

> **Target Audience:** We Build Member State Advisory Board participants  
> **Date:** September 2026  
> **Subject:** Restoring Critical Industry/Economy Capabilities and Enabling Scalable Trust Chaining in the EBW Regulation  
> **Author:** Werner Folkendt (Robert Bosch GmbH) supported by participants from Deutsche Bank, DATEV, Siros, iGrant, Siemens, Schweizer Bundesbahn, Platform Industry 4.0

# Table of Contents

[Table of Contents [2](#table-of-contents)](#table-of-contents)

[1. Executive Summary & Key Takeaways [4](#executive-summary-key-takeaways)](#executive-summary-key-takeaways)

[2. Reinstating Independent EAA Issuing as a Core Functionality (Article 5(1)(f)) [5](#reinstating-independent-eaa-issuing-as-a-core-functionality-article-51f)](#reinstating-independent-eaa-issuing-as-a-core-functionality-article-51f)

[2.1 “WE BUILD" Consortium (WBC) lessons learned: Independent issuing of EAAs by EBW owners is mandatory [5](#we-build-consortium-wbc-lessons-learned-independent-issuing-of-eaas-by-ebw-owners-is-mandatory)](#we-build-consortium-wbc-lessons-learned-independent-issuing-of-eaas-by-ebw-owners-is-mandatory)

[2.2 Case Study: Why External QTSPs Cannot Assure Liability for Issued Bank Credentials [6](#case-study-why-external-qtsps-cannot-assure-liability-for-issued-bank-credentials)](#case-study-why-external-qtsps-cannot-assure-liability-for-issued-bank-credentials)

[2.3 Self-Assertion is Not a Trust Service [6](#self-assertion-is-not-a-trust-service)](#self-assertion-is-not-a-trust-service)

[2.4 The Economic Impact: The SME “Pay-per-Credential” cost increase [7](#the-economic-impact-the-sme-pay-per-credential-cost-increase)](#the-economic-impact-the-sme-pay-per-credential-cost-increase)

[3. Mandating Protocol Support for the Issuing Role (Article 6(1)(a)) [7](#mandating-protocol-support-for-the-issuing-role-article-61a)](#mandating-protocol-support-for-the-issuing-role-article-61a)

[4. Scaling the Trust Ecosystem via Attestation Chaining (Article 5(1)(g)) [8](#scaling-the-trust-ecosystem-via-attestation-chaining-article-51g)](#scaling-the-trust-ecosystem-via-attestation-chaining-article-51g)

[4.1 The Problem: The Trusted Lists (TLs) Bottleneck [8](#the-problem-the-trusted-lists-tls-bottleneck)](#the-problem-the-trusted-lists-tls-bottleneck)

[4.2 The Solution: Cryptographic “Identity Attestation Chaining” [8](#the-solution-cryptographic-identity-attestation-chaining)](#the-solution-cryptographic-identity-attestation-chaining)

[5. The Principle of Equivalence — Cryptographic EAAs vs. Paper [9](#the-principle-of-equivalence-cryptographic-eaas-vs.-paper)](#the-principle-of-equivalence-cryptographic-eaas-vs.-paper)

[6. Restoring Legal Support for AI-Driven Agents & Smart Objects [10](#restoring-legal-support-for-ai-driven-agents-smart-objects)](#restoring-legal-support-for-ai-driven-agents-smart-objects)

[7. Line-by-Line Legislative Amendments Table [10](#line-by-line-legislative-amendments-table)](#line-by-line-legislative-amendments-table)

[8. Supporting Organizations and Endorsements [11](#supporting-organizations-and-endorsements)](#supporting-organizations-and-endorsements)

# 1. Executive Summary & Key Takeaways

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><em>The 3rd Presidency compromise proposal (Draft 3) introduces vital improvements and supervisory oversight. However, as the European Union prepares for the upcoming trilogues next month, European industry urges Member State representatives to address two critical flaws that reduce the European Business Wallet (EBW) value proposition for the European economy significantly and create significant risk for commercial success:</em></p>
<ul>
<li><p><strong>The removal of independent issuing capabilities</strong> from the European Business Wallet (EBW) core functionalities under Article 5.1(f).</p></li>
<li><p><strong>The absence of a scalable, decentralized trust verification mechanism</strong> under Article 5.1(g) (Attestation Chaining) to verify millions of business issuers without overloading national Trusted Lists (TLoLs).</p></li>
</ul>
<p><em>Without native, independent issuing of Electronic Attestations of Attributes (EAAs) and a robust legal framework for Attestation Chaining, key industry-driven MVP use cases—such as automated customer/supplier onboarding (KYC/KYS) and bank account opening—will become impossible to implement digitally and scale through supply chains.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Key Recommendations for Member State Advisory Board**

- **Restore Independent Issuance (Art. 5(1)(f)):** Re-establish the EBW owner’s right to independently self-issue and sign corporate credentials. Without that WBC use cases can’t be piloted. Self-assertion are required and are not an eIDAS Trust Service and does not trigger Trust Service Provider (TSP) liabilities.

- **Support Issuing Protocols (Art. 6(1)(a)):** Mandate that the EBW supports communication protocols for both the issuing (attestation provider) and receiving (holder) roles to prevent architectural fragmentation.

- **Legislate Attestation Chaining (Art. 5(1)(g)):** Mandate a decentralized trust verification model where the issuer's wallet-bound identity (EBWOID) is chained in the credential header, allowing immediate verification via the national TLoL without requiring millions of individual EBW businesses owners to register.

- **Adopt the Principle of Equivalence for Cryptographic EAAs:** Recognize that digitally signed, cryptographically bound EAAs provide vastly stronger security guarantees than physical, stamped paper documents.

- **Support Automated Transactions (EP Amendment 19a):** Re-introduce legal definitions for authorized digital and AI-driven agents to secure future-proof use cases like optimization of production processes with the help of Agentic AI or independent charging and paying of electric vehicles at charging stations.

# 2. Reinstating Independent EAA Issuing as a Core Functionality (Article 5(1)(f))

## 2.1 “WE BUILD" Consortium[^1] (WBC) lessons learned: Independent issuing of EAAs by EBW owners is mandatory

An important lesson learned from the specification and pilot operation of WBC is that independent (self)-issuing of EAAs (SELF-EAA) by the EBW owner is a mandatory requirement for the implementation of important use cases like Know your Supplier, Know your Customer and Corporate Banking.
The demand to independently issue EAAs complements the demand for attestations issued by QTSP’s.

- **Mandatory onboarding data can be provided only by the owner:** A small supplier must provide the same basic attributes (UBO, Control and Ownership Structure, …) as a multinational enterprise to clear compliance (KYC, KYS, open bank account). This data can be provided only by the legal entity itself to its business partners. They are not completely available in official registries (e.g. owners outside the EU)

- **Majority of attestations are EAA:** The number of required EAAs is already significantly higher than the number of Public EAAs (PUB-EAAs) and Qualified EAAs (QEAAs) combined. Means going in operation area will have definitly more EAA ( ex. invoice, receipt, iban, sites, quality company certificates...)  
  **Table 1: EAA Requirements in Core WBC Use Cases for first pilot iteration (MVP)**

| Use Case                                                 | Required EAAs         | QEAAs Required | PUB-EAAs Required |
|----------------------------------------------------------|-----------------------|----------------|-------------------|
| KYC – Financial Sector (e.g., Open Bank Account Service) | 7-14                  | 3-4            | 1                 |
| KYS – Supplier Onboarding                                | 5-12                  | 2-3            | 1                 |
| KYC – Non-Financial Sector                               | 3-11                  | 2-4            | 1                 |

Note: Many required data points (e.g., Ultimate Beneficial Owner (UBO) data required by banks under AMLR) do not exist in official registries because they have no access to registries outside of the EU and therefore must be self-asserted by the company.

- **Scaling requires self-issued EAAs:** To scale the use cases even smaller companies need the capability to self-issue attestations. EBW owners cannot wait until all accredited attestation providers are able to issue attestations (e.g. Company Certificates from TÜV, IBAN attestations from banks) Therefore for existing bank accounts and company certificates (already available as \*.pdf and valid during the next 3-5 years) legal entities need to self-issue attestations.

- **EBWOID together with EBW is a means of authentication**  
  The EBW together with EBWOID should be a means of authentication in the same way as it is stated for EUDIW/PID in eIDAS2.

## 2.2 Case Study: Why External QTSPs Cannot Assure Liability for Issued Bank Credentials

To assess the feasibility of different issuance models, a joint evaluation was conducted by Bosch, Deutsche Bank, and a QTSP. This discussion clarified the distinct and complementary roles of authoritative data sources (like banks) and Qualified Trust Service Providers (QTSPs) in the ecosystem.
The central conclusion is that a balanced approach is required. The EU’s Trusted-List (TL) framework, which governs QTSPs, provides the essential foundation of legal accountability and identity verification for the entire system.
The evaluation highlighted two key points:
1.	The Authoritative Source Principle: For certain highly sensitive or dynamic attributes, such as IBAN account ownership, the bank remains the sole authoritative source of truth. A third-party QTSP cannot independently verify this information in real-time due to structural barriers like banking secrecy and data security. In this model, the QTSP's primary role is to securely verify the identity of the issuer (the bank), while the bank, as the issuer, remains liable for the accuracy of the data itself.
2.	The Value of the QTSP Framework: For other types of credentials, the existing QTSP framework provides a robust and trusted mechanism for issuance. QTSPs are subject to rigorous liability and audit requirements under eIDAS, and when they issue credentials (like a QEAA), they ground them in clear legal accountability. This model should be leveraged where appropriate.
   
This analysis confirms that a one-size-fits-all, mandatory intermediation by a third party for all types of attestations is not practical. 
The most secure and viable model is a flexible one: allowing authoritative sources (like a bank) to issue data directly, using a legal identity that has been rigorously verified by a QTSP. This approach respects the established eIDAS trust framework while accommodating the structural realities of sensitive corporate data.
The same applies to other EAAs like UBO, Control Structure, Ownership Structure,… and other attestations which need to be issued by the EBW owner. 


## 2.3 Self-Assertion is Not a Trust Service

We understand that the Council’s legal concern regarding EAA issuance as a core functionality stems from the assumption that any issuance of EAAs constitutes a “trust service” under eIDAS 2.0. Under this interpretation, an EBW owner would be classified as a Trust Service Provider (TSP) merely by issuing EAAs, thereby imposing disproportionate regulatory and compliance burdens for SMEs.

**An EBW owner who self-issues EAAs or offers EAAs without renumeration does not act as a TSP:**

- **Definition of Trust Service:** Under eIDAS, a Trust Service is defined as an electronic service normally provided for remuneration to third parties.

- **Self-Assertion:** When a company (e.g., Company A) cryptographically signs and issues its own data (such as its IBAN, company address, …) to a customer, it is performing self-assertion.

- **No TSP Liability:** Company A is not offering a commercial trust service to others; it is simply presenting its own corporate claims digitally. Therefore, self-issuing corporate attributes does not trigger the regulatory, auditing, and cybersecurity liabilities of a TSP.

## 2.4 The Economic Impact: The SME “Pay-per-Credential” cost increase

We understand that the Council’s intention to remove native issuance from Article 5.1 was to “reduce costs for SMEs’ by allowing for a simplified low-cost European Business Wallet (EBW), this approach is highly likely to achieve the exact opposite. Stripping the EBW of native issuing capabilities will, in fact, drive up operational costs for SMEs by forcing them to rely on external third-party services for routine business verifications:

- **The Tollbooth Model:** If SMEs cannot natively sign and issue basic self-asserted attributes from their own EBW, they will be forced to buy validation or issuance services from external QTSPs for every routine B2B transaction (e.g. eInvoices, eReceipts, …). This creates an expensive, permanent pay-per-credential model for SMEs.

- **Market-Driven Wallet Pricing:** The EBW backend natively requires sealing/signing capabilities anyway. Exposing this through an API does not drive-up development costs. The market will naturally offer "basic" (holder-only) and "premium" (holder + issuer) frontends, ensuring competitive pricing. The regulation does not need to protect SMEs from additional unnecessary costs.

# 3. Mandating Protocol Support for the Issuing Role (Article 6(1)(a))

By restricting the technical features in Article 6 to receiving and sharing, the current text forces rigid, one-way architecture. If the EBW is technically prevented from running the protocols necessary to act in the “attestation provider” (issuer) role, the entire WBC blueprint, existing Architectural Design Records (ADRs) and current pilot implementations will be rendered obsolete. This would inevitably mandate a complete redesign, significantly delaying the marked readiness of the EBW.  
“Article 6

Technical features for European Business Wallets

1\. Providers of European Business Wallets shall ensure that the European Business Wallets support common protocols and interfaces:

a\) for the issuance of European Business Wallet owner identification data, qualified and non-qualified electronic attestations of attributes … to European Business Wallets;”

To ensure interoperability, the technical protocols must explicitly support the outbound issuance flow:

- **German Translation Alignment:** In German translation, "Issuing" means "Ausstellen." Therefore, the protocol to issue attestations must be supported symmetrically alongside receipt protocols.

- **Proposed Text Correction:** Article 6(1)(a) must be amended to explicitly state that protocols support both the attestation provider role and the holder role.

  Proposed text: “…for the issuing in the attestation provider role and for receiving issued attestations in the holder role of European Business Wallet owner identification data… to European Business Wallets;”

# 4. Scaling the Trust Ecosystem via Attestation Chaining (Article 5(1)(g))

## 4.1 The Problem: The Trusted Lists (TLs) Bottleneck

Under the current eIDAS framework, trust is established by registering accredited Trust Service Providers (TSPs) on national Trusted Lists (TLs), which are aggregated by the European Commission into the List of Trusted Lists (LOTL).

- **The Scale Problem:** This approach is fundamentally unsuited for B2B transactions. Most EU Member States lack the administrative capacity to register and maintain millions of European businesses as EAA Providers in their national TLs.

- **The Legacy Project Risk:** Temporary industry-specific directories (such as the We Build trust list extension also for EAAs) will dissolve when pilot phases conclude. This will leave businesses without a permanent, legally viable mechanism to verify the authenticity and validity of standard B2B credentials.

## 4.2 The Solution: Cryptographic “Identity Attestation Chaining” 

To enable the ecosystem to scale rapidly without creating administrative bottlenecks, we must leverage the “Identity Attestation Chaining” framework already anchored in the EBW regulation in parallel with other trust infrastructures like EBSI or others. By embedding the issuer’s European Business Wallet Owner Identification Data (EBWOID) directly into the cryptographic header of each issued EAA, we establish a decentralized, high-assurance verification chain that links every credential back to a legally verified organizational identity:

- **Zero Trust-List Overhead:** The EAA Provider does not need to be registered on any national trusted lists.

- **Simple Verification Path:** The Relying Party (verifier) only needs to access the public LOTL to verify the identity of the EBWOID Provider (which is a recognized QTSP). They then cryptographically traverse the chain to verify that the EAA was indeed signed by the legitimate EBW owner.

- **Long-Lived, Offline Verifiability:** Because the cryptographic proof chain (EBWOID + EAA) is entirely self-contained within the credential’s metadata header, the document remains verifiable offline and in the long term - even if the issuing company ceases to exist. This is a critical requirement for long-lived records such as academic diplomas, warranties, or material composition certificates for Digital Product Passports (DPPs).

# 5. The Principle of Equivalence — Cryptographic EAAs vs. Paper

The Council’s approach significantly weakens the principle of equivalence by limiting it to qualified trust services, arguing that non-qualified self-asserted EAAs inherently possess a lower level of trust. Such a limitation would render Article 4 of the EUBW Regulation largely redundant. The legal effects of qualified trust services are already comprehensively governed by the eIDAS Regulation. It is therefore unclear what additional value would be achieved beyond the existing legal framework, whereas it is evident that such an approach would create new questions. In fact, it would create a regulatory double standard: Why does a physically stamped paper letter from a bank should have more legal standing than a cryptographically secured EAA?

An EAA issued natively via an EBW provides infinitely stronger technical guarantees than paper, specifically through:

- **Cryptographically Signed & Tamper-Evident:** Any modification to the data structure instantly invalidates the credential.

- **Cryptographic Binding (Holder binding):** The credential is key-bound directly to the holder’s wallet. This prevents unauthorized transfer, theft or reuse by third parties.

- **Automated Verifiability:** Relying parties can digitally verify the issuer's identity (via the chained EBWOID), the precise timestamp of issuance, and the status of the trust chain.

**Conclusion**: To foster a modern B2B ecosystem, Member States must ensure that a cryptographically verified digital EAA is legally recognized as at least equivalent to its physical, paper-based counterpart.

In addition, the Council clarifies that where existing EU or national legislation imposes requirements relating to electronic formats as part of an administrative procedure, those requirements remain fully applicable and must continue to be complied with. This means that the use of the European Business Wallet would no longer automatically satisfy all procedural requirements. As a result, businesses would still need to assess, on a case-by-case basis, whether the specific format requirements of the relevant legal framework are met, thereby reducing legal certainty and limiting the practical benefits of the EUBW.   

A possible compromise could be to preserve the principle of equivalence in its original and comprehensive form, ensuring that actions carried out through the EUBW have the same legal effect as in-person procedures, paper-based processes and other digital procedures. At the same time, Member States could be granted the right, within 12 months of the Regulation’s entry into force, to identify and notify specific national administrative procedures for which the EUBW cannot be used. 

# 6. Restoring Legal Support for AI-Driven Agents & Smart Objects

The Council’s removal of EP Amendment 19a (Automated Transactions) severely limits the EBW’s utility in a modern, software- and data driven economy. Without a clear and robust legal framework for automated, machine-driven transactions, EU businesses will face significant legal barriers when deploying:

- **AI-Driven Procurement:** Autonomous AI agents executing purchase orders, clearing customs requirements, or signing supply chain declarations will operate in a legal gray zone, creating substantial compliance risks.

- **Digital Product Passports (DPPs):** Products (such as batteries, industrial machinery or vehicles) will be legally restricted from autonomously presenting verified compliance and lifecycle data to regulators or supply chain partners.

- **Smart Asset Wallets (Industrial IoT):** Connected physical assets (e.g., shared fleet vehicles, manufacturing machines) will be unable to autonomously negotiate or execute legally binding contracts.

**Call to action:** We strongly urge Member States to support the European Parliament’s position to reinstate Amendment 19a. Defining “automated transactions” as those executed by authorized digital or AI-driven agents under a valid, auditable, and revocable delegation from the EBW owner is essential to future-proof industry.

# 7. Line-by-Line Legislative Amendments Table

To secure the EBW’s market adoption, industry recommends the following compromise positions during the upcoming trilogue negotiations:

<table>
<colgroup>
<col style="width: 13%" />
<col style="width: 27%" />
<col style="width: 29%" />
<col style="width: 29%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Article</strong></th>
<th><strong>Council Draft Text (compromise)</strong></th>
<th><strong>Industry Proposed Text (Trilogue Compromise)</strong></th>
<th><strong>Rationale</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>Art. 5(1)(f)<br />
(Core Func.)</strong></td>
<td>“…(f) have electronic attestations of attributes securely issued by the provider on behalf of the European Business Wallet owner…”</td>
<td><strong>“…(f) issue, or have securely issued on their behalf, electronic attestations of attributes relating securely to European Business Wallets…”</strong></td>
<td>Restores the right of companies to independently self-assert their own corporate data without forcing them into a costly, third-party QTSP dependency.</td>
</tr>
<tr class="even">
<td><strong>Art. 5(1)(g)<br />
(Chaining)</strong></td>
<td><del>issue electronic attestations of attributes through the European Business Wallet of the owner, allowing the issued attestation to be linked to other relevant attestations forming part of a chain</del> link electronic attestations of attributes issued pursuant to point (f) to other electronic attestations of attributes forming part of a chain;</td>
<td><strong>Use EC proposed paragraph (g):<br />
“issue electronic attestations of attributes through the European Business Wallet of the owner, allowing the issued attestation to be linked to other relevant attestations forming part of a chain”</strong></td>
<td>Establishes the legal and technical foundation for decentralized B2B trust verification, eliminating the administrative bottleneck of registering millions of SMEs on national trusted lists.</td>
</tr>
<tr class="odd">
<td><strong>Art. 6(1)(a)<br />
(Tech. Features)</strong></td>
<td>“…for the issuance of European Business Wallet owner identification data… to European Business Wallets;”</td>
<td><strong>“…for the issuing in the attestation provider role and for receiving issued attestations in the holder role of European Business Wallet owner identification data… to European Business Wallets;”</strong></td>
<td>Prevents technical fragmentation and ensures EBW solutions natively support symmetric protocols for sending and receiving credentials.</td>
</tr>
<tr class="even">
<td><strong>Recital /<br />
Art. 19a<br />
(AI &amp; Auto.)</strong></td>
<td>Deleted in Council Version</td>
<td><p><strong>Reinstate EP Amendment in Article 3 pragraph 1 -point 19a (new) :<br />
“‘<em>(19a) ‘automated transaction’ means atransaction executed by an authorised</em></strong></p>
<p><em><strong>digital or AI-driven agent, performing</strong></em></p>
<p><em><strong>actions under a valid, auditable and</strong></em></p>
<p><em><strong>revocable authorisation issued by the</strong></em></p>
<p><em><strong>European Business Wallet owner or</strong></em></p>
<p><em><strong>authorised user;</strong></em></p></td>
<td>Provides the necessary legal foundation for the Machine Economy, Digital Product Passports (DPPs), and autonomous AI agents.</td>
</tr>
<tr class="odd">
<td><strong>Art. 4<br />
(Equivalence)</strong></td>
<td>Limits equivalence to qualified trust services</td>
<td><strong>“…resulting action shall have the same legal effect as if the action had been lawfully carried out in person, in paper form, or via any other means… including verified Electronic Attestations of Attributes (EAAs</strong>) cryptographically bound to the owner.”</td>
<td>Ensures that highly secure digital attributes are not legally disadvantaged compared to easily falsified physical paper documents.</td>
</tr>
</tbody>
</table>

# 8. Supporting Organizations and Endorsements

Document was created based on discussions and meetings with We Build participants from: Deutsche Bank, Datev, Siemens, Sirion, Schweizer Bundesbahn, Platform Industrie4.0 and other We Build participants

This position paper represents the consolidated stance of leading European industrial, financial, and digital trust organizations active within the "We Build" Initiative and participants of the “Platform Industrie 4.0”

The recommendations and legislative amendments proposed in this document are currently supported by participants from the following organizations: Deutsch Bank, Robert Bosch GmbH, Siemens, Schweizer Bundesbahn, Siros, iGrant, Datev,…

The paper represents the opinion of individual participants and not the formal official position of their organisation. The position paper is currently discussed with additional organizations, therefore, the above list will be updated.

Please contact Werner Folkendt (<werner.folkendt@de.bosch.com>) for questions or feedback

[^1]: [WE BUILD Consortium \| EUDI & EU Business Wallet Use Cases](https://www.webuildconsortium.eu/)
