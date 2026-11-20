# Active Onboarding Tracker Template (`<UseCase>_<PartnerName>_<Business_Role>(<Technical_Role>).md`)

Copy this template to create your partner-specific tracking file (e.g., `PA3_Scenario1_Bosch_Company(Holder).md`).

## 📋 Profile Metadata

| Parameter              | Value                                              |
|:-----------------------|:---------------------------------------------------|
| **Use Case ID**        |                                                    |
| **Partner Name**       |                                                    |
| **Business Role**      | *(e.g., Supplier, Buyer, Bank)*                    |
| **Technical Role**     | *(e.g., Holder, Relying Party / Verifier, Issuer)* |
| **Onboarding Contact** | *(Email / Slack handle)*                           |

---

## 🏁 Step1 : Wallet Instance Deployment

| Position | Requirement                   | More Details | Status                                       | Evidence / Notes |
|:---------|:------------------------------|:-------------|:---------------------------------------------|:---|
| 1.1      | **EBW** Installed & Reachable |              | ⚪ Not Started / 🟡 In Progress / 🟢 Complete | *Insert endpoint URL*                       |
| 1.2*     | **EUDI Wallet** Installed     | Requester    | ⚪ Not Started / 🟡 In Progress / 🟢 Complete | *Insert wallet app name*                     |

*Adapt this checklist to your use case:*
- Remove any wallet type that is not required.
- The check marked with * need to duplicated for each distinct EUDI Wallet implementation required. Specify its provider, app name, version and role.
--

## 🏁 Phase 2: Interoperability Test Bed (ITB) & CTS Testing

| Check | Wallet | Requirement            | Test Case          | Status                               | Evidence / Notes   |
|:------|:-------|:-----------------------|:-------------------|:-------------------------------------|:-------------------|
| 2.1   |        | **ITB Portal Account** |                    | ⚪ Not Started / 🟢 Complete          | Username:          |
| 2.2   | EBW    | **CS-Basic**           | ex  VCI-006        | ⚪ Not Started / 🟢 Complete          | Execution Date:    |
| 2.3   | EBW    | **CS-Basic**           | ex. VP-011, VP-013 | ⚪ Not Started / 🟢 Complete          | Execution Date:    |
| 2.4*  | EUDI   | **CS-Basic**           | ex  VCI-006        | ⚪ Not Started / 🟢 Complete          | Execution Date:    |
| 2.5*  | EUDI   | **CS-Basic**           | ex. VP-011, VP-013 | ⚪ Not Started / 🟢 Complete          | Execution Date:    |
| 2.6   | EBW    | **CS-Trust**           | ex  VCI-006        | ⚪ Not Started / 🟢 Complete          | Execution Date:    |
| 2.7   | EUDI   | **CS-Trust**           | ex. VP-011, VP-013 | ⚪ Not Started / 🟢 Complete          | Execution Date:    |
| 2.8   | EUDI   | **CS-Signature**       | ex                 | ⚪ Not Started / 🟢 Complete          | Execution Date:    |
| 2.9   | EBW    | **CS-Issuer**          | ex. Test Case 001  | ⚪ Not Started / 🟢 Complete          | Execution Date:    |
| 2.10  | EUDI   | **CS-Issuer**          | ex. Test Case 002  | ⚪ Not Started / 🟢 Complete          | Execution Date:    |

*Adapt this checklist to your use case:*
- Remove any wallet type that is not required.
- The check marked with * need to duplicated for each distinct EUDI Wallet implementation required. Specify its provider, app name, version and role. 
---

## 🏁 Phase 3: Cryptographic Trust List Registration

* **Target Trust Register:** *(Refer to Section 3 of Master Blueprint to find the exact registry)*
* **IDunion Trust Console Account:** 🔲 Registered / ⚪ Pending / ❌ N/A

| Check   | Wallet     | Requirement | Test Case / Verification | Status | Evidence / Notes |
|:--------|:-----------|:---|:---|:---|:---|
| 3.1.1   | EUDI       | **Verifier — Access certificate** | Confirm the verifier has a valid access certificate from an authority anchored in **WEBUILD - Access Certificate Authorities**. | ⚪ Not Started | Certificate reference, issuer, expiry date. Onboarding via Raidiam. |
| 3.1.2*  | EUDI       | **Verifier — Registration certificate** | Confirm the registration certificate covers the intended service, requested attributes and purpose. Check its issuing authority against **WEBUILD - Access Registration Authorities**. | ⚪ Not Started | Certificate reference, registered scope, approval date. |
| 3.2.1   | EUDI/EBW   | **PuB-EAA issuer — Provider registration** | Confirm the issuer’s entry and trust anchor in **WEBUILD - Pub-EAA Providers**. | ⚪ Not Started | Registry entry, organisation identifier, trust-anchor reference. |
| 3.2.2   | EUDI/EBW   | **QEAA issuer — Provider registration** | Confirm the issuer’s entry and trust anchor in **WEBUILD - QEAA Providers**. | ⚪ Not Started | Registry entry and applicable qualified-status evidence. |
| 3.2.3   | EUDI/EBW   | **EBWOID issuer — Provider registration** | Confirm the issuer’s entry in **WEBUILD - EBWOID Providers**. | ⚪ Not Started | Registry entry, organisation identifier, authorised scope. |
| 3.2.4   | EUDI       | **PID issuer — Provider registration** | Confirm the issuer’s entry and trust anchor in **WEBUILD - PID Providers**. | ⚪ Not Started | Registry entry, organisation identifier, trust-anchor reference. |
| 3.2.5*  | EUDI       | **PCF auditor EAA — Sector registration** | Confirm the issuer’s entry in **Chamber of Auditors EAA Provider**. | ⚪ Not Started | Registry entry, credential type, onboarding date. |
| 3.2.6   | EUDI       | **Bank SCA credential — Sector registration** | Confirm the issuer’s entry in **UseCase Bank SCA**. | ⚪ Not Started | Registry entry, credential type, onboarding date. |
| 3.2.7*  | EUDI       | **DPC credential — Sector registration** | Confirm the issuer’s entry in **UseCase DPC**. | ⚪ Not Started | Registry entry, credential type, onboarding date. |
| 3.2.8   | EUDI       | **Sectoral EAA issuer — Access certificate** | Confirm a valid access certificate from an authority anchored in **WEBUILD - Access Certificate Authorities**. | ⚪ Not Started | Certificate reference, issuer, expiry date. |
| 3.2.9*  | EUDI       | **Sectoral EAA issuer — Registration certificate** | Confirm the registration certificate covers the specific attestation type being issued. | ⚪ Not Started | Attestation type, certificate reference, registration authority. |
| 3.2.10  | EUDI       | **Other EAA issuer — Access certificate** | Confirm a valid access certificate for the issuer service, e.g. for employee or A1 credentials. | ⚪ Not Started | Issuer service, certificate reference, expiry date. |
| 3.2.11* | EUDI       | **Other EAA issuer — Registration scope** | Confirm registration coverage for each intended attestation type. Confirm whether separate certificates are required by this ecosystem. | ⚪ Not Started | Attestation type, certificate reference, registered scope. |
| 3.3.1   | EUDI / EBW | **Intermediary — Infrastructure access** | Verify the certificate chain against **WEBUILD - WP 4 - Group 5 - Trust Registry Infrastructure Access Certificate Authority**. | ⚪ Not Started | Certificate reference, trust anchor, validation result. |
| 3.4.1   | EUDI / EBW | **Wallet provider — Registry entry** | Confirm the provider’s entry in **WEBUILD - Wallet Providers**. | ⚪ Not Started | Registry entry, provider identifier, trust-anchor reference. |

*Adapt this checklist to your use case:*
- Remove any wallet type that is not required.
- The check marked with * need to duplicated for each distinct EUDI Wallet implementation required. Specify its provider, app name, version and role.
- The check marked with * need to duplicated for each attestation.
---


## 🏁 Phase 4: Credential Provisioning Tracker

| Check | Credential Type | Status | Issuance Portal / Source Used |
|:---|:---|:---|:---|
| 4.1 | **PID** (EUDI Wallet) | ⚪ Not Started / 🟢 Complete | `https://issuer.eudiw.dev/display_credential_offer` or `https://playground.credenco.com/webuild` |
| 4.2 | **EBWOID** (EBW) | ⚪ Not Started / 🟢 Complete | `https://eida-issuer.spherity.dev/attested-issuance` |
| 4.3* | **EUCC** (EBW) | ⚪ Not Started / 🟢 Complete | `https://eida-issuer.spherity.dev/attested-issuance` |
| 4.4* | **CompanyInfo** (EBW Self-EAA) | ⚪ Not Started / 🟢 Complete | Self-issued via Company Wallet |
| 4.5* | **ContactPerson** (EBW Self-EAA) | ⚪ Not Started / 🟢 Complete | Self-issued via Company Wallet |
| 4.6* | **VAT** (EBW Self-EAA) | ⚪ Not Started / 🟢 Complete | Self-issued via Company Wallet |
| 4.7* | **Owner** (EBW Self-EAA) | ⚪ Not Started / 🟢 Complete | Self-issued via Company Wallet |
| 4.8* | **Control** (EBW Self-EAA) | ⚪ Not Started / 🟢 Complete | Self-issued via Company Wallet |
| 4.9* | **UBO** (EBW Self-EAA) | ⚪ Not Started / 🟢 Complete | Self-issued via Company Wallet |
| 4.10* | **AuthorisedSignatories** (EBW Self-EAA) | ⚪ Not Started / 🟢 Complete | Self-issued via Company Wallet |

*Adapt this checklist to your use case:*
- Remove any wallet type that is not required.
- The check marked with * need to duplicated for each distinct EUDI Wallet implementation required. Specify its provider, app name, version and role.
---
