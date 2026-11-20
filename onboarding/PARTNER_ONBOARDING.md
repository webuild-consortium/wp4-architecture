# WEBUILD MVP Partner Onboarding Blueprint

This master document outlines the standard prerequisites, conformance testing, trust registration, and credential provisioning required to successfully run a WEBUILD MVP or MVP++ between **Partner A (Holder)** and **Partner B (Relying Party / Verifier)**.

---

## 🚀 Step-by-Step Onboarding Process

### Step 1: Wallet Instance Deployment
Each partner must deploy a conformant wallet instance aligned with their designated role.

You can deploy your own business wallet (conforming to WEBUILD standards) or choose from the predefined list:
👉 [WEBUILD WP4 Wallets Directory](https://webuild-consortium.github.io/wp4-wallets-group/)

#### Identify Your Wallet Requirements
* **Natural Person Wallet (EUDI Wallet):** Required if your use case has a Holder role played by a natural person.
    * [WEBUILD WP4 Wallets Directory](https://webuild-consortium.github.io/wp4-wallets-group/)
    * *Selection:* Filter by `Wallets that can be used by natural persons` on the directory.
* **Enterprise Business Wallet (EBW):** Required for legal entities acting as Holders, Verifiers/Relying Parties, or Issuers.
    * [WEBUILD WP4 Wallets Directory](https://webuild-consortium.github.io/wp4-wallets-group/)
    * *Selection:* Filter by `Wallets that can be used by legal persons` on the directory.
    * ⚠️ **Important Notes:** Setting up an EBW requires a valid **EBWOID** credential, which in turn requires a natural person with an **EUDI Wallet** to authorize the company issuance.

| Check | Requirement | Status | Evidence / Notes |
|:---|:---|:---|:---|
| 🔲 | **EBW** Installed & Reachable | ⚪ Not Started | Public Endpoint URL (if available): |
| 🔲 | **EUDI Wallet** Installed | ⚪ Not Started | Wallet App & Version: |

*Note: Each use case already has a list of predefined Wallet Providers (both natural and business wallets) involved.*

---

### Step 2: Interoperability Test Bed (ITB) Onboarding & Testing Alignment
Before executing any tests, register in the ITB environment and pass the **WEBUILD Conformance Test Suite (CTS)**.

*Prerequisite: Step 1 (Wallet Instance Deployment) must be completed.*

1. **ITB Portal Access:** Request login credentials:
    * **Portal Link:** [ITB Login Portal](https://dev-i4mlab.aegean.gr/itb/app#/login)
    * **Action:** Email **Nico** or **Elster**, or ping on the Slack channel.
2. **Slack Channel:** Coordinate your testing in [#wp4-testing](https://we-build-consortium.slack.com/archives/C09K65GLKT2).
3. **Master Documentation:** Refer to the comprehensive [Webuild Google Doc Guidance](https://docs.google.com/document/d/1NR6O5WGA1z1rw4zHtBmGvFkjd9SyTTVdR2TjbJrubc0/edit?pli=1&tab=t.0#heading=h.l16nv1c1n7ja).

---

### Step 3: WEBUILD Trust List Registration Matrix
To establish ecosystem-wide trust, you must register your certificate/key on the IDunion trust console.
Every cryptographic certificate/key used to build trust in your MVP must be registered in the correct trusted list on the IDunion console. Below is the mapped-out catalog representing what is listed on [IDunion Trusted Lists](https://console.dev.idunion.info/trusted-lists), structured role-by-role.

The process can be done directly on the [IDunion Console](https://console.dev.idunion.info/trusted-lists/).

1. **Get Console Access:** Register a contact person for your company on the [IDunion Console](https://console.dev.idunion.info/).
2. **Registration Steps (for respective registers, except Access and Registration Certificates):**
    * **Export CSR:** Connect to your wallet instance and export your **Certificate Signing Request (CSR)** or public certificate.
    * **Register Certificate:** Upload/register your certificate according to your MVP role in the corresponding registry.
3. **In case of Access and Registration Certificate**, the process need to be made by Access Certificate Authority or Registration Certificate Authority.
    * Refer to the onboarding spec: [Raidiam WEBUILD Ecosystem Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs).

---

### 1. Relying Party (Verifier) Role

#### 1.1. For EUDI Credentials
*If you are the verifier (e.g., verifying a personal identity using an EUDI Wallet), register your credentials in the following registries:*

> ⚠️ **Important Registration Note:** This process cannot be registered directly on the console and must be performed by an authorized authority (Raidiam in this ecosystem). Two registrations are required (one for access and the second for reading):

| Registry Display Name | Description | Reference / Registration Link |
|:---|:---|:---|
| **WEBUILD - Access Certificate Authorities** | Trusted List showing Access Certificate Authorities. | [Raidiam WEBUILD Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |
| **WEBUILD - Access Registration Authorities** | Trusted List showing Registration Certificate Authorities. | [Raidiam WEBUILD Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |

#### 1.2. For EBW Credentials
* No registration is required, except if your specific use case requires one.

---

### 2. Issuer Role (EUDI / EBW Credentials)
*If you are issuing company details, attestations, personal credentials, or payment credentials, locate your designated credential type below to find the target registry:*

#### 2.1. PuB-EAA (Public Sector Attribute Attestation) Issuer
| Registry Display Name | Description | Direct Registry Console / Reference Link |
|:---|:---|:---|
| **WEBUILD - Pub-EAA Providers** | Trusted List showing PuB-EAA Providers. | [IDunion Console](https://console.dev.idunion.info/trusted-lists/OsVKoh6j) or [Raidiam Specs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |

#### 2.2. QEAA (Qualified Electronic Attribute Attestation) Issuer
| Registry Display Name | Description | Direct Registry Console / Reference Link |
|:---|:---|:---|
| **WEBUILD - QEAA Providers** | Trusted List showing QEAA Providers. | [IDunion Console](https://console.dev.idunion.info/trusted-lists/OsVKoh6j) or [Raidiam Specs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |

#### 2.3. EBWOID (Enterprise Business Wallet OID) Issuer
| Registry Display Name | Description | Direct Registry Console / Reference Link |
|:---|:---|:---|
| **WEBUILD - EBWOID Providers** | Trust registry list showing authorized EBWOID Providers in the consortium. | [IDunion Console](https://console.dev.idunion.info/trusted-lists/OsVKoh6j) or [Raidiam Specs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |

#### 2.4. PID (Personal Identification Data) / Registration Issuer
| Registry Display Name | Description | Direct Registry Console / Reference Link |
|:---|:---|:---|
| **WEBUILD - PID Providers** | Dedicated registry for Personal Identification Data (PID) Providers. | [IDunion Console](https://console.dev.idunion.info/trusted-lists/OsVKoh6j) or [Raidiam Specs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |

#### 2.5. Sectoral & Bilateral EAAs for EUDI Wallets (ex. SCA, PCF Auditors, DPC)
*Direct onboarding is available for each of these sectoral EAAs:*

| Registry Display Name | Description | Specs Reference Link |
|:---|:---|:---|
| **Chamber of Auditors EAA Provider** | Trusted PCF (Product Carbon Footprint) Auditors registration point. | [IDunion Console](https://console.dev.idunion.info/trusted-lists/) |
| **UseCase Bank SCA** | Trust registry list dedicated to bank-issued credentials in financial scenarios (e.g., SCA). | [IDunion Console](https://console.dev.idunion.info/trusted-lists/) |
| **UseCase DPC** | Trusted List showing trusted EAA Providers for Digital Payment Credential (DPC). | [IDunion Console](https://console.dev.idunion.info/trusted-lists/) |

*Notes* Additionally the access and registration certificate are required
| Registry Display Name | Description | Specs Reference Link |
|:---|:---|:---|
| **WEBUILD - Access Certificate Authorities** | Trusted List showing Access Certificate Authorities. | [Raidiam WEBUILD Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |
| **WEBUILD - Access Registration Authorities** | Trusted List showing Registration Certificate Authorities. | [Raidiam WEBUILD Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |

TODO FC multiply with the attestations that you want to issued

#### 2.6. Issuer of EUDI Credentials (ex Employee,A1)

| Registry Display Name | Description | Specs Reference Link |
|:---|:---|:---|
| **WEBUILD - Access Certificate Authorities** | Trusted List showing Access Certificate Authorities. | [Raidiam WEBUILD Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |
| **WEBUILD - Access Registration Authorities** | Trusted List showing Registration Certificate Authorities. | [Raidiam WEBUILD Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |
* in case that many attestation are issued by the same entity for each attestation a registration certificate is required

#### 2.7. Issuer of EBW Credentials
* No registration is required, except if your specific use case requires one.

---

### 3. Intermediary / Transit Role
| Registry Display Name | Description | Specs Reference Link |
|:---|:---|:---|
| **WEBUILD - WP 4 - Group 5 - Trust Registry Infrastructure Access Certificate Authority** | Anchor list allowing intermediaries to securely connect and interface with the Group 5 testing APIs. | [Act as Intermediary Tutorial](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs/act-as-intermediary/) |

---

### 4. Wallet Provider
| Registry Display Name | Description | Onboarding Link |
|:---|:---|:---|
| **WEBUILD - Wallet Providers** | Providers of digital identity wallet solutions. | Open onboarding portal |

---

## ⚠️ Holder Role Exception
> **Note for Holders (Mobile / Enterprise Wallets):**
> Pure **Holders** (natural persons using EUDI mobile wallets or businesses using pure Enterprise Wallets with no issuance/verification roles) **do not require any registry entries** on the IDunion trusted list console. Their trust is established unilaterally by presenting credentials that trace back cryptographically to the registered Issuers listed above.

---

### Step 4: Conformance Testing Baselines (CTS)

1. Log in to your ITB Account: [ITB Login Portal](https://dev-i4mlab.aegean.gr/itb/app#/login)
2. Select **"My Conformance Statements"** from the left-hand menu.
3. Select **"Base Protocols"**.
4. Execute the tests specified in each block one-by-one according to your use case definition (if required).


#### 4.1. CS-Basic (Mandatory to run the MVP)

##### 4.1.1. WE BUILD CTS - CS-01 Issuance
Verify if the wallet can successfully receive credentials/attestations (without any trust check).
* **Test Case:** *At least one test case must be specified.*
    * *Example:* `Test Case VCI-006 [Wallet SUT]: WE BUILD - Pre-authorized code flow - SD-JWT - X509`
    * *Note: Key Attestation (KA) is required.*
* **Execution Flow:**
    1. Retrieve the `openid4vci` request (via QR Code or Link).
    2. Review the offer and accept it.
    3. Check and log the transaction status.

##### 4.1.2. WE BUILD CTS - CS-02 Presentation
Verify if the wallet can successfully present requested claims to a Verifier (without any trust check).
* **Test Case:** *At least one test case must be specified.*
    * *Examples:*
        * `Test Case VP-011: CS-02 hash presentation invoked with OpenID4VP [Wallet SUT]`
        * `Test Case VP-013: CS-02 hash presentation invoked with haip-vp [Wallet SUT]`
* **Execution Flow:**
    1. Retrieve the `openid4vp` request (via QR Code or Link).
    2. Present the requested credential.
    3. Check and log the transaction status.
* *Note: Document this in the usecase_tracklist.*

---

#### 4.2. WE BUILD CTS - Trust Framework Integration (Use-Case Dependent)

##### 4.2.1. TrustFramework - Issuance
Verify if the wallet can successfully receive credentials/attestations with WEBUILD trust.
* **Test Case:** *At least one test case must be specified.*
    * *Example:* `Test Case VCI-006 [Wallet SUT]: WE BUILD - Pre-authorized code flow - SD-JWT - X509`
* **Execution Flow:**
    1. Retrieve the `openid4vci` request (via QR Code or Link).
    2. Review the offer and accept it.
    3. Check and log the transaction status.

##### 4.2.2. TrustFramework - Presentation
Verify if the wallet can successfully present requested claims to a Verifier with WEBUILD Trust Registry.
* **Test Case:** *At least one test case must be specified.*
    * *Examples:*
        * `Test Case VP-011: CS-02 hash presentation invoked with OpenID4VP [Wallet SUT]`
        * `Test Case VP-013: CS-02 hash presentation invoked with haip-vp [Wallet SUT]`
* **Execution Flow:**
    1. Retrieve the `openid4vp` request (via QR Code or Link).
    2. Present the requested credential.
    3. Check and log the transaction status.

---

#### 4.3. CS-Signature (If required by Use Case)
* **QES via QTSP:** Validate whether the wallet can present PID, download QES, and sign the document hash.

---

#### 4.4. CS-Issuer: WE BUILD Relying Parties Conformance Test Suite (If required by Use Case)

##### 4.4.1. CS-Issuer - Issuance
Verify if your component can successfully issue:
* **Test Case:** `Test Case 001 [Issuer SUT]:: WE BUILD Issuer VCI 1.0`
* **Execution Flow:**
    1. Retrieve the `openid4vci` from your wallet instance.
    2. Paste it in the next step.
    3. Check and log the transaction status.

##### 4.4.2. CS-Issuer - Verification
Verify if your component can successfully verify:
* **Test Case:** `Test Case 002 [Verifier SUT]:: WE BUILD Issuer VP 1.0`
* **Execution Flow:**
    * *Prerequisite:* Step **4.4.1 (CS-Issuer - Issuance)** must be executed successfully before running verification.
    1. Retrieve the `openid4vp` from your wallet instance.
    2. Paste it in the next step.
    3. Check and log the transaction status.

---

### Conformance Baseline Summary Checklist

| Wallet Type | Test Baseline | Status | Evidence / Notes |
|:---|:---|:---|:---|
| **EBW** | CS-Basic | ⚪ Not Started | |
| **EUDI** | CS-Basic | ⚪ Not Started | |
| **EBW** | CS-Trust (Optional) | ⚪ Not Started | |
| **EUDI** | CS-Trust (Optional) | ⚪ Not Started | |
| **EUDI** | CS-Signature (Optional) | ⚪ Not Started | |
| **EBW** | CS-Issuer (Optional) | ⚪ Not Started | |
| **EUDI** | CS-Issuer (Optional) | ⚪ Not Started | |

*Note: In order to start the MVP, CS-Basic is mandatory. Depending on the use case, additional CS types may be required (please check your specific use case).*
----

### Step 5: Environment Setup & Credential Provisioning

#### 5.1. Personal Identification Data (PID) (Rulebook: [rb-pid](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-pid))

##### 5.1.1 How to Obtain
1. **Attribute Preparation:** Prepare required details like Legal Name, First Name, Date of Birth, and Place of Birth.
2. **Build Credential:** Visit the chosen portal from the directories below:

   | PID Issuer | Location | Remarks |
      |:---|:---|:---|
   | EUDI Wallet demo application | [PID Issuer Portal](https://issuer.eudiw.dev/display_credential_offer) | Define your own PID based on your data. Note: this demo issuer is not registered in the Webuild trusted list. |
   | Credenco Wallet | [Credenco Playground](https://playground.credenco.com/webuild) | Dutch playground |

3. Fill in the required data fields.
4. **Accept in Wallet:** Scan the generated QR code with your mobile EUDI Wallet and accept.
5. **Verifier/RP Setup:** Import the *PID Schema* into your EBW/Verifier system, and prepare your **DCQL Query** requesting `urn:eu.europa.ec.eudi:pid:1` with the `family_name` attribute.

##### 5.1.2 🛠️ Prepare Proof Request (RP)
* **Import Schemas:** Import the schemas from the `PID.schema.json` rulebook into your EBW Company Wallet (or coordinate with your wallet provider to enable them).
* **Build Request:** Construct the proof request by combining the required attributes, or use the provided DCQL Query attached to the standard `PID.dcql.standard.json`.

---

#### 5.2. Obtain Enterprise Business Wallet ID (EBWOID) (Rulebook: [rb-eucc](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-eucc))

##### 5.2.1 How to Obtain
1. **Get Authorized Person Data:** Access public registers to retrieve information about the legal representative (Name, Surname, Birthdate, Location).
    * *Fallback:* If not available in the public register, check with EBWOID Providers to use standard test personas.
2. **Initiate Request:** Navigate to the EBWOID Provider page 

   | Register Name      | Covered Countries                  | Direct Access Portal Link                                                                   |
   |:-------------------|:-----------------------------------|:--------------------------------------------------------------------------------------------|
   | **Bundesanzeiger** | DE, AT, PL, CH, etc. (8 Countries) | [Bundesanzeiger Attested Issuance Page](https://eida-issuer.spherity.dev/attested-issuance) |
   | **Infogreffe**     | FR                                 | to be filled                                                                                |
   | **InfoCert**       | IT                                 | to be filled  |
   | **Bolagsverket**   | SE                                 | to be filled  |

In case if *Bundesanzeiger* selection
3. **Select Attestation:** Click on **EBWOID Attestation**.
4. **Identify Company:** Search and select your company name.
5. **Scan & Present PID:** Use your EUDI Wallet (with the PID obtained in 5.1) to scan the QR code and authorize.
6. **Claim Credential:** Copy the generated Credential Offer link and paste it into your company's EBW to accept.
7. **Verifier/RP Setup:** Import the *EBWOID Schema* into your EBW, and build the required DCQL presentation query.

##### 5.2.2 🛠️ Prepare Proof Request (RP)
* **Import Schemas:** Import the schemas of the `EBWOID.schema.json` rulebook into your EBW Company Wallet (or coordinate with your wallet provider to enable them).
* **Build Request:** Construct the proof request by combining the required attributes, or use the provided DCQL Query attached to the standard `EBWOID.dcql.standard.json`.

---

#### 5.3. European Union Company Credential (EUCC) (Rulebook: [rb-eucc](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-eucc))

##### 5.3.1 How to Obtain
1. **Initiate Issuance:** Visit the [Bundesanzeiger Attested Issuance Page](https://eida-issuer.spherity.dev/attested-issuance) and select **EUCC Attestation**.
2. **Request Proof:** Copy the generated presentation request.
3. **Present EBWOID:** Paste the request into your company EBW, review the requested EBWOID attributes, and present.
4. **Claim Credential:** Return to the Spherity Issuer page, copy the generated **EUCC Credential Offer** link, and accept it in your company EBW.

##### 5.3.2 🛠️ Prepare Proof Request (RP)
* **Import Schemas:** Import the schemas of `EUCC.schema.json` into your EBW Company Wallet (or coordinate with your wallet provider to enable them).
* **Build Request:** Construct the proof request by combining the required attributes, or use the provided DCQL Query attached to the standard `EUCC.dcql.standard.json`.

---

#### 5.4. Company Self-Attested Attestation (Self-EAA)

##### 5.4.1 How to Create It

| Name                      | Rulebooks                                                                                                                                              |
|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **CompanyInfo**           | [rb-company-info](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-company-info)                     |
| **ContactPerson**         | [rb-contact-person](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-contact-person)                 |
| **VAT**                   | [rb-vat](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-vat)                                       |
| **Owner**                 | [rb-owner](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-owner)                                   |
| **Control**               | [rb-control](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-control)                               |
| **UBO**                   | [rb-ubo](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-ubo)                                       |
| **AuthorisedSignatories** | [rb-authorised-signatories](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-authorised-signatories) |

##### 5.4.2 How to Obtain It for the Legal Entity (Company)
1. **Open Wallet & Load Schemas:** Open your company wallet and ensure the rulebook schemas are imported.
2. **Prepare Data:** Gather the mandatory data fields for each attestation (template/demo data can be extracted from the rulebook definitions).
3. **Trigger Issuance:** Start the issuer process, input the prepared metadata, and copy the generated Credential Offer.
4. **Accept in Wallet:** Paste the offer into your company wallet, review, and confirm acceptance.

#### 5.4. Company Self-Attested Attestation (Self-EAA)

| Name | Rulebooks |
|:---|:---|
| **CompanyInfo** | [rb-company-info](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-company-info) |
| **ContactPerson** | [rb-contact-person](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-contact-person) |
| **VAT** | [rb-vat](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-vat) |
| **Owner** | [rb-owner](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-owner) |
| **Control** | [rb-control](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-control) |
| **UBO** | [rb-ubo](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-ubo) |
| **AuthorisedSignatories** | [rb-authorised-signatories](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-authorised-signatories) |


##### 5.4.1 How to Obtain It for the Legal Entity (Company)
1. **Open Wallet & Load Schemas:** Open your company wallet and ensure the rulebook schemas are imported.
3. **Prepare Data:** Gather the mandatory data fields for each attestation (template/demo data can be extracted from the rulebook definitions).
4. **Trigger Issuance:** Start the issuer process, input the prepared metadata, and copy the generated Credential Offer.
5. **Accept in Wallet:** Paste the offer into your company wallet, review, and confirm acceptance.

##### 5.4.2 🛠️ Prepare Proof Request (RP)

1. **Import Schemas:** Import the schemas into your EBW Company Wallet.

| Name                      | Schema File                         |
|:--------------------------|:------------------------------------|
| **CompanyInfo**           | `CompanyInfo.schema.json`           |
| **ContactPerson**         | `ContactPerson.schema.json`         |
| **VAT**                   | `VAT.schema.json`                   |
| **Owner**                 | `Owner.schema.json`                 |
| **Control**               | `Control.schema.json`               |
| **UBO**                   | `UBO.schema.json`                   |
| **AuthorisedSignatories** | `AuthorisedSignatories.schema.json` |

2. **Build Request:** Construct the proof request by combining the required attributes, or use the provided DCQL queries:

| Name                      | DCQL Query File                            |
|:--------------------------|:-------------------------------------------|
| **CompanyInfo**           | `CompanyInfo.dcql.standard.json`           |
| **ContactPerson**         | `ContactPerson.dcql.standard.json`         |
| **VAT**                   | `VAT.dcql.standard.json`                   |
| **Owner**                 | `Owner.dcql.standard.json`                 |
| **Control**               | `Control.dcql.standard.json`               |
| **UBO**                   | `UBO.dcql.standard.json`                   |
| **AuthorisedSignatories** | `AuthorisedSignatories.dcql.standard.json` |

*Note: Check your use case (predefined combined DCQL queries are already available - use case specific).*
......
