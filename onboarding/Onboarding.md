# Onboarding – Generic Process and Reference Guidance

**Purpose:** Reusable WP4 instructions for all partners and scenarios. Maintained centrally by WP4. Do not copy this document into individual partner trackers.

**Scope:** Stages 1–8 provide generic onboarding and provisioning instructions; Stage 9 is documented only as a hand-off to the use-case tracker, where interoperability test execution and results are recorded.

**Status rule:** All scenario-specific applicability, exact test-case IDs, owners, evidence, results and sign-off belong in the use case's copy of [Tracking_template.md](Tracking_template.md), in the use case's own repository. Generic examples below are not mandatory test-case selections.

## Identification and Wallet Setup

### Stage 1 – Role identification

1. Identify the use case, scenario, partner and business role (e.g., supplier, buyer, bank).
2. Confirm each technical role: 
   - Holder (natural and/or legal person)
   - Verifier/Relying Party
   - Issuer
   - Intermediary 
   A partner may have multiple technical roles.
3. Identify the required EUDI Wallet and/or Enterprise Business Wallet (EBW) implementations for each role.
4. Record the approved role assignment and wallet inventory in the scenario-specific partner tracker.

**Exit criterion:** Roles and wallet requirements have been confirmed by the use-case level.

### Stage 2 – Wallet initialization and deployment

**Goal:** A conformant wallet instance matching your role is installed and reachable.

**Actions**

1. Choose your wallet from the [WEBUILD WP4 Wallets Directory]([https://webuild-consortium.github.io/wp4-wallets-group/](https://wallets.webuildconsortium.eu/)), or deploy your own WEBUILD-conformant business wallet.

| Wallet type                          | Needed when                                          | Directory filter                              | 
|:-------------------------------------|:-----------------------------------------------------|:----------------------------------------------|
| **EUDI Wallet** (natural person)     | The use case has a Holder played by a natural person | `Wallets that can be used by natural persons` |
| **EBW** (Enterprise Business Wallet) | A legal entity acts as Holder, Verifier/RP or Issuer | `Wallets that can be used by legal persons`   |

3. Install the **EUDI Wallet first**. Activating an EBW needs an **EBWOID**, and issuing the EBWOID requires a natural person with an EUDI Wallet to authorize it (see Stage 8, EBWOID guidance).
3. If you use several distinct EUDI Wallet implementations, track each one separately.

**Exit criteria:** Wallet(s) installed; EBW endpoint reachable (if applicable).
**Record in tracker:** Provider, app name, version, role, endpoint URL.

---

## ITB Onboarding and Basic Conformance

### Stage 3 – ITB onboarding

**Goal:** You can log in to the Interoperability Test Bed and coordinate testing.

*Prerequisite: Wallet access sufficient to begin ITB testing (Stage 2).*

**Actions**

1. Request ITB credentials: email **Nico** or **Ester** (*contact details to be added*) or ask on Slack. Portal: [ITB Login Portal](https://dev-i4mlab.aegean.gr/itb/app#/login)
2. Join Slack channel [#wp4-testing](https://we-build-consortium.slack.com/archives/C09K65GLKT2).
1. Request ITB access as described in the [ITB user guide, section 2.1](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/user-guide-interoperability-test-bed.md#21-obtaining-the-access): post in the [#itb-support](https://we-build-consortium.slack.com/archives/C09K65GLKT2) Slack channel with your organisation, intended roles and targeted protocol versions.
2. Log in to the [ITB portal](https://dev-i4mlab.aegean.gr/itb/app#/login) once you have received your credentials.

**Exit criteria:** You can log in to the ITB; you are in #itb-support.
**Record in tracker:** ITB username, date of access.

---

### Stage 4. ITB Basic Conformance (CS-Basic)

**Goal:** Your wallet can receive and present credentials (no trust check).

*Prerequisite: Stage 3.*

**How to run any CTS block**

1. Log in to the ITB.
2. Open **My Conformance Statements** → **Base Protocols**.
3. Execute the tests of each block one by one, according to your use-case definition.

| Block                  | Purpose                                               | Test cases                                                                                                                                        | Notes                                                                                                   |
|:-----------------------|:------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|
| **CS-01 Issuance**     | The wallet can receive credentials/attestations       | At least one, defined by the use case. Illustrative example: `VCI-006` in `PA3.Scenario1` (pre-authorized code, SD-JWT, X.509, without BWUA)                   | **Key Attestation (KA) is required.**                                                                   |
| **CS-02 Presentation** | The wallet can present requested claims to a Verifier | At least one, defined by the use case. Illustrative example: `VP-001` in `PA3.Scenario1` (DCQL request for `urn:eu.europa.ec.eudi:pid:1`, claim `family_name`) | Flow: retrieve the `openid4vp` request → present the credential → check and log the transaction status. |

> **Naming:** In the tracker, CS-01 and CS-02 are grouped as **CS-Basic**. Run them once per wallet type (EBW and each EUDI Wallet).

**Exit criteria:** All specified CS-01 and CS-02 test cases passed for every wallet you operate.
**Record in tracker:** Test case ID, execution date, result link or screenshot.

---

**Scenario-specific rule:** The use-case lead selects the applicable CS-01/CS-02 cases; the partner tracker records test IDs, runs, evidence and results. Do not treat the examples above as universally mandatory.

## Trust and Role-Specific Conformance

### Stage 5 – WEBUILD Trust List Registration

To establish ecosystem-wide trust, organisations that issue or verify credentials must be registered. The WP4 Trust group maintains the onboarding guides: [Trusted Lists onboarding](https://github.com/webuild-consortium/wp4-trust-group/blob/main/task1-use-cases/subtask1-1-onboarding/trusted-lists-onboarding.md) and [Relying Party registry onboarding](https://github.com/webuild-consortium/wp4-trust-group/blob/main/task1-use-cases/subtask1-1-onboarding/relying-party-registry-onboarding.md). This section summarises which registration applies to which role.

#### General procedure

1. **Trusted Lists:** follow the [Trusted Lists onboarding guide](https://github.com/webuild-consortium/wp4-trust-group/blob/main/task1-use-cases/subtask1-1-onboarding/trusted-lists-onboarding.md) to register on the IDunion console.
2. **Access and Registration Certificates** are issued by Raidiam, not registered on the console. See [Relying Party registry onboarding](https://github.com/webuild-consortium/wp4-trust-group/blob/main/task1-use-cases/subtask1-1-onboarding/relying-party-registry-onboarding.md) and the [Raidiam WE BUILD docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs).

#### Reference: Access / Registration Certificate registries

These two registries are used by Verifiers and by Issuers of EUDI credentials. Both registrations are required.

| Registry | Description | Reference |
|:---|:---|:---|
| **WEBUILD – Access Certificate Authorities** | Trusted list of Access Certificate Authorities | [Raidiam Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |
| **WEBUILD – Registration Certificate Authorities** *(shown on the console as "Access Registration Authorities")* | Trusted list of Registration Certificate Authorities | [Raidiam Docs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |

#### 5.1 Relying Party (Verifier)

| Credentials verified | Registration needed |
|:---|:---|
| **EUDI credentials** (e.g., personal identity via EUDI Wallet) | Access Certificate + Registration Certificate (see reference above), obtained via Raidiam |
| **EBW credentials** | None, unless your use case requires it |

#### 5.2 Issuer

Find your credential type below. How to request the listing is described in the [Trusted Lists onboarding guide](https://github.com/webuild-consortium/wp4-trust-group/blob/main/task1-use-cases/subtask1-1-onboarding/trusted-lists-onboarding.md).

| Issuer type | Registry | Link |
|:---|:---|:---|
| **PuB-EAA** (Public Sector Attribute Attestation) | WEBUILD – Pub-EAA Providers | [IDunion Console](https://console.dev.idunion.info/trusted-lists/OsVKoh6j) · [Raidiam Specs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |
| **QEAA** (Qualified Electronic Attribute Attestation) | WEBUILD – QEAA Providers | [IDunion Console](https://console.dev.idunion.info/trusted-lists/OsVKoh6j) · [Raidiam Specs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |
| **EBWOID** (European Business Wallet Owner Identification Data) | WEBUILD – EBWOID Providers | [IDunion Console](https://console.dev.idunion.info/trusted-lists/OsVKoh6j) · [Raidiam Specs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |
| **PID** | WEBUILD – PID Providers | [IDunion Console](https://console.dev.idunion.info/trusted-lists/OsVKoh6j) · [Raidiam Specs](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs) |

#### 5.2.5 Sectoral & bilateral EAAs for EUDI Wallets (e.g., SCA, PCF Auditors, DPC)

Direct onboarding is available for each sectoral EAA:

| Registry | Description | Link |
|:---|:---|:---|
| **Chamber of Auditors EAA Provider** | Trusted PCF (Product Carbon Footprint) Auditors | [IDunion Console](https://console.dev.idunion.info/trusted-lists/) |
| **UseCase Bank SCA** | Bank-issued credentials in financial scenarios (e.g., SCA) | [IDunion Console](https://console.dev.idunion.info/trusted-lists/) |
| **UseCase DPC** | Trusted EAA Providers for Digital Payment Credentials (DPC) | [IDunion Console](https://console.dev.idunion.info/trusted-lists/) |

In addition, **Access and Registration Certificates are required** (see reference above).

#### 5.2.6 Issuer of other EUDI credentials (e.g., Employee, A1)

Access and Registration Certificates are required (see reference above). If one entity issues several attestation types, **a separate Registration Certificate is required for each attestation type.**

#### 5.2.7 Issuer of EBW credentials

No registration is required unless the use case specifies otherwise. Note: whether an Access Certificate is required when issuing to another business wallet is an open decision in WP4. Check with your use-case lead.

**Note:** If the use case requires additional registration to establish trust or authorization, contact the IDunion team for support. 

#### 5.3 Intermediary / Transit

| Registry | Description | Reference |
|:---|:---|:---|
| **WEBUILD – WP 4 – Group 5 – Trust Registry Infrastructure Access Certificate Authority** | Anchor list allowing intermediaries to securely connect to the Group 5 testing APIs | [Act as Intermediary tutorial](https://www.raidiam.com/developers/docs/raidiam-webuild-eudi-ecosystem-docs/act-as-intermediary/) |

For non-qualified EAA Providers: If your Use Case requires a Trusted List (or LoTE) that is not available, please request your list to be set up via info@idunion.eu. Please provide some basic information about your Use Case (Work Package, number of listed entities, potential restrictions for listings, etc.)

#### 5.4 Wallet Provider

| Registry | Description | Onboarding |
|:---|:---|:---|
| **WEBUILD – Wallet Providers** | Providers of digital identity wallet solutions | [Wallet Provider onboarding](https://github.com/webuild-consortium/wp4-wallets-group/blob/main/guidance/trusted-list-onboarding/README.md) |

#### Holder role exception

Pure **Holders** (natural persons using EUDI mobile wallets, or businesses using Enterprise Wallets with no issuance or verification role) **need no registry entries** on the IDunion console. Their trust is established by presenting credentials that trace back cryptographically to the registered Issuers.

#### Stage 5 checklist

| Check | Requirement | Status | Evidence / Notes |
|:---:|:---|:---:|:---|
| 🔲 | Contact person registered on IDunion Console | ⚪ | |
| 🔲 | Certificate/CSR registered in role-specific registry | ⚪ | Registry: |
| 🔲 | Access Certificate obtained (if applicable) | ⚪ | |
| 🔲 | Registration Certificate(s) obtained (if applicable) | ⚪ | One per attestation type |

---

### Stage 6 – Trust conformance (CS-Trust)

**Goal:** Demonstrate the applicable trust-framework integration using the ITB. The generic reference covers wallet trust and, where relevant, Wallet Unit Attestation ([CS-01, CS-02, CS-04](https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/README.md)). Baseline trust validation is being specified in CS-018 (pre-flight).

**Applicability:** Defined by the use-case lead for each technical role and wallet implementation. The business-wallet validation specification is marked **to be confirmed** in the source guidance.

**Procedure:** Select the approved CS-Trust cases in the ITB, execute them, and record test case IDs, execution date, results and evidence in the partner tracker.

**Exit criterion:** Every applicable CS-Trust case has passed, or an approved exception is recorded.

### Stage 7 – Sectorial-specific conformance (use-case-dependent)

*Prerequisites: Stage 3 passed; Stage 5 trust registration and Stage 6 trust conformance completed where required.*

| Block            | What it validates                                                                                                   | Applies to   | Status of definition |
|:-----------------|:--------------------------------------------------------------------------------------------------------------------|:-------------|:---|
| **CS-Issuer**    | The entity can successfully trigger EAA issuance                                                                    | EBW and EUDI | Defined |
| **CS-Signature** | The wallet can present a PID, obtain a QES via a QTSP and sign the document hash                                    | EUDI         | Defined |
| **CS-QERDS**     | The wallet can communicate over the QERDS channel | EUDI/EBW     | Defined |

ITB blocks and the WBCS they test: CS-Issuer → CS-01, CS-Signature → CS-03, CS-QERDS → CS-15 / CS-16. See the [WBCS list](https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/README.md). *Extensions for further processes: to be added.*

**Exit criteria:** All blocks required by the use-case definition passed.
**Record in tracker:** Test case ID, execution date, result link.

---

## Prerequisites Provisioning and MVP Execution

### Stage 8 – Generic prerequisite provisioning guidance

**Principle:** The use-case defines which credentials, schemas, proof requests, issuers and test data are required for each Holder, Verifier and Issuer. The approved scenario tracker is the source of those requirements. The following is a reference catalog and procedural guide, not a universal checklist.

### 8.1 Credential selection and dependencies

**Reference ID note:** The source credential catalog uses legacy IDs 8.1–8.8; the detailed instructions below are grouped as subsections 8.2.1–8.2.8. These are reference identifiers only, not partner-tracker task IDs.

#### Credential dependency chain

Obtain credentials in this order. Skip what your use case does not need.

| ID  | Credential                                               | Held in     | Requires first               | Test issuer                                           |
|:---:|:---------------------------------------------------------|:------------|:-----------------------------|:------------------------------------------------------|
| 8.1 | **PID** (Person Identification Data)                     | EUDI Wallet | EUDI Wallet installed        | PID test issuers (see 8.1)                            |
| 8.2 | **QEAA** (e.g., qualified attestation)                   | EUDI Wallet | EUDI Wallet installed        | issued to eudi wallet by QTSP Provider (see 8.2)      |
| 8.3 | **EAA** (ex. Employee,A1,.....)                          | EUDI Wallet | EUDI Wallet installed        | issued to eudi wallet by other entities see 8.3)      |
| 8.4 | **EBWOID** (European Business Wallet Owner Identification Data) | EBW | PID + EBW installed | EBWOID Issuers see 8.4)                               |
| 8.5 | **EUCC** (EU Company Credential)                         | EBW         | EBWOID                       | EUCC issuers (see 8.5                                  |
| 8.6 | **QEAA** (ex. VAT,TAX,...)                               | EBW         |                              | issued by QTSP (contact QTSP Provider) (8.6)          |
| 8.7 | **EAA** (ex. IBAN,SCA,.....)                             | EBW         | EBW OID + process to obtain  | issued to your company wallet by other entities (8.7) |
| 8.8 | **Self-EAA** (ex. CompanyInfo, ContactPerson, VAT, etc.) | EBW         | EBW + imported schemas       | Self-issued via your company wallet (8.8)             |

Rulebook catalog: [webuild-attestation-rulebooks-catalog](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks)

#### Role-specific provisioning guidance

* **As holder:** Obtain the credential (section "How to obtain").
* **As verifier/RP:** Import the schema into your EBW and prepare the DCQL query (section "Prepare proof request") with the respective VCT 
* **As issuer:** Import the schema into your EBW and use the test data provided in the respective schemas folder
---

#### 8.2.1 Personal Identification Data (PID)

**Rulebook:** [rb-pid](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-pid)

##### How to obtain

1. **Prepare attributes:** see the mandatory attributes in the [PID Rulebook, section 3.2](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/blob/main/rulebooks/rb-pid/README.md#32-mandatory-attributes) (e.g. `family_name`, `given_name`, `birth_date`).
2. **Choose a PID issuer:**
   a. choose a predefined PID Issuers if your use case already have one
   b. choose a generic PID Test Issuers or a country Issuers (according to your use case) from the [List of PID issuers](https://github.com/webuild-consortium/wp4-pid-ebwoid-group/blob/main/List%20of%20issuers.md#pid-issuers), maintained by the PID/EBWOID group. It includes country issuers and generic test issuers supporting multiple countries. Note that some test issuers are not registered in the WE BUILD trusted lists.

4. **Fill in** the required data fields.
5. **Accept in wallet:** scan the QR code with your mobile EUDI Wallet and accept.

##### Prepare proof request (RP)

* Import `PID.schema.json` into your EBW (or ask your wallet provider to enable it).
* Build the request yourself, or use `PID.dcql.standard.json`. Baseline test: `urn:eu.europa.ec.eudi:pid:1` with `family_name`.

---
#### 8.2.2 QEAA to EUDI Wallet 
- To be completed for the relevant scenario.
- 
#### 8.2.3 EAA to EUDI Wallet 
- To be completed for the relevant scenario (e.g., Employee or SCA).

#### 8.2.4 European Business Wallet Owner Identification Data (EBWOID)

**Rulebook:** [rb-ebwoid](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-ebwoid)

*Prerequisites: PID in your EUDI Wallet (8.1); company EBW installed.*

##### How to obtain

1. **Get authorized-person data:** look up the legal representative (name, surname, birthdate, location) in public registers.
2. **Choose an EBWOID issuer**
   a. choose a predefined EBWOID Test Issuers if your use case already have one
   b. choose a generic EBWOID Issuers or a country Issuers (according to your use case) from the [List of EBWOID issuers](https://github.com/webuild-consortium/wp4-pid-ebwoid-group/blob/main/List%20of%20issuers.md#ebwoid-issuers), maintained by the PID/EBWOID group. It includes country issuers and generic test issuers supporting multiple countries.

4. **Open the issuer portal and select** *EBWOID Attestation*.
5. **Identify the company:** search for and select it.
6. **Scan and present PID:** use your EUDI Wallet (with the PID from 8.1) to scan the QR code and authorize.
7. **Claim:** copy the Credential Offer link and paste it into your company EBW.

##### Prepare proof request (RP)

* Import `EBWOID.schema.json`; use `EBWOID.dcql.standard.json` or build your own.

---

#### 8.2.5 European Union Company Credential (EUCC)

**Rulebook:** [rb-eucc](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-eucc)

*Prerequisite: EBWOID in your company EBW (8.4).*

##### How to obtain

1. **Initiate issuance:** An EBWOID is required.
2. **Choose a generic EUCC issuer supporting multiple countries:**
   [Bundesanzeiger Attested Issuance Page](https://eida-issuer.spherity.dev/attested-issuance/eucc). 
3. **Request proof:** copy the generated presentation request.
4. **Present EBWOID:** paste the request into your company EBW, review the requested attributes, present.
5. **Claim:** Return to the Spherity page, copy the **EUCC Credential Offer** link, accept it in your company EBW.

##### Prepare proof request (RP)

* Import `EUCC.schema.json`; use `EUCC.dcql.standard.json` or build your own.

---
#### 8.2.6 QEAA for business wallet 
To be completed by the use-case lead. 

#### 8.2.7 EAA for business wallet 

Ex:
| Attestation | Rulebook | Schema | DCQL |
|:---|:---|:---|:---|
| **IBAN-OV** | [rb-iban-ov](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-iban-ov) | `ibanov.schema.json` | `ibanov.dcql.standard.json` |
| **SCA** | [rb-sca-iban](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-sca-iban), [rb-sca-card-dpc](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-sca-card-dpc), [rb-sca-user](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-sca-user) | `sca.schema.json` | `sca.dcql.standard.json` |
| **GS1** | [rb-company-info](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-company-info) | `gs1.schema.json` | `gs1.dcql.standard.json` |
etc 


####### How to obtain it, repeated per attestation

1. **Load schemas:** make sure the rulebook schema is imported in your company wallet.
2. **Prepare data:** gather the mandatory fields. Demo data can be taken from the rulebook definition.
3. **Trigger issuance:** start the issuer process, enter the data and copy the Credential Offer. *(To confirm: which issuer or tool performs this step.)*
4. **Accept in wallet:** paste the offer into your company wallet, review, confirm.

##### Prepare proof request (RP)

Import the schema files from the table into your EBW, then build the request yourself or use the matching `*.dcql.standard.json` file.



#### 8.2.8 Company Self-Attested Attestations (Self-EAA)

Ex:
| Attestation | Rulebook | Schema | DCQL |
|:---|:---|:---|:---|
| **CompanyInfo** | [rb-company-info](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks/rb-company-info) | `CompanyInfo.schema.json` | `CompanyInfo.dcql.standard.json` |
all other self attested 

####### How to obtain it, repeated per attestation

1. **Load schemas:** make sure the rulebook schema is imported in your company wallet.
2. **Prepare data:** gather the mandatory fields. Demo data can be taken from the rulebook definition.
3. **Trigger issuance:** start the issuer process, enter the data and copy the Credential Offer. *(To confirm: which issuer or tool performs this step.)*
4. **Accept in wallet:** paste the offer into your company wallet, review, confirm.

##### Prepare proof request (RP)

Import the schema files from the table into your EBW, then build the request yourself or use the matching `*.dcql.standard.json` file.

### Stage 9 – MVP interoperability execution

Stage 9 is **tracked only in the scenario/partner tracker**. The use-case lead defines the end-to-end test steps and acceptance criteria; participating partners record each execution run, actual result, evidence, defects, retests and final approval. This generic onboarding document does not store MVP test results.

WP4 owns this generic document. Proposed changes should be reviewed centrally; scenario-specific selections and evidence must remain in the trackers.
