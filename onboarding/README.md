# WEBUILD WP4 - Integration & Partner Onboarding Repository

Welcome to the central coordination repository for the **WEBUILD MVP & MVP++** interoperability and integration phase. This project facilitates secure, decentralized identity testing between consortium partners playing the roles of **Holders**, **Issuers**, and **Relying Parties (Verifiers)**.

To successfully run your the MVP and MVP++ between

- Partner A (role: Holder) 
- Partner B (role: Verifier)
- Partner C (role: Issuer)

we have a clear separation between generic guidelines and partner-specific tracking.

---

## 🗺️ Onboarding Strategy

To maintain a clean and scalable onboarding process, we separate **generic setup instructions** from **partner-specific progress tracking**:

1. **`Partner_Onboarding.md` (The Master Blueprint - Read-Only):**

   * This static document contains step-by-step instructions, reference links, schemas, and rulebook details. It serves as the single source of truth for both partners.

2. **`<UseCase>_<PartnerName>_<Business_Role>(<Technical_Roles>).md` (The Active Tracker - Write/Fill):**

    * A partner-specific checklist copied from the template.
    * It is used to track installation status, record ITB test runs, document trust registry configurations, and store evidence.
   
    * *Example:* 
    * If **CompanyA** plays both roles in `BU1_Scenario2` KYS process, they will fill out:
        * `BU1_Scenario2_CompanyA_Supplier(Holder/Issuer).md`
          *  in case that the CompanyA also must to issue self attestation this will documented also here
        * `BU1_Scenario2_CompanyA_Buyer(Verifier/Issuer).md`
          *  in case that the CompanyA also must to issue self attestation this will documented also here
        * in case that a CompanyC only issue 
          * `BU1_Scenario2_CompanyC_Authority(Issuer).md`
    * for each TODO block specify the list of required test cases inside the usecase      
```text
repo-root/
│
├── README.md                                # This entry point
├── Partner_Onboarding.md                    # Master instructions (Read-Only)
├── UseCase_PartnerName_Role_Tracking.md *   # Copy this to track your use case and extend it to your use requirements   
│
└── use-case tracking/                        # Directory for active trackers
    ├── BU1_Scenario2_CompanyA_Supplier(Holder/Issuer).md
    └── BU1_Scenario2_CompanyA_Buyer(Verifier).md
    └── BU1_Scenario2_CompanyC_Authority(Issuer).md
```
