# Tracking Template – Scenario Requirements and Partner Execution

**Usage:** Copy this template first to an approved scenario baseline, then create a partner-specific copy for each partner/role combination. The use-case lead defines requirements; partners update actual progress. Generic procedures are maintained in [`WP4_Onboarding.md`](Onboarding.md).

**Statuses:** ⚪ Not started · 🟡 In progress · ✅ Done · 🔴 Blocked · ➖ N/A · ❔ To confirm. **Test outcomes:** Not run / Pass / Fail / Blocked / Retest pending.

## Scenario and partner profile

| Field                      | Value                           |
|----------------------------|---------------------------------|
| Use case / scenario        | `<UseCase>-<Scenario>`          |
| Partner                    | `<Partner>`                     |
| Partner owner / contact    | `<Name>`                        |
| Business role              | `<Supplier/Buyer/Bank/etc.>`    |
| Technical role(s)          | `<Holder/Verifier/Issuer/etc.>` |
| Baseline                   | baseline                        |
| Last updated               | `<YYYY-MM-DD>`                  |
| Overall status             | ⚪                               |

## Wallet inventory (available wallets, use case specific)

| Wallet| Wallet type / purpose                                          | MVP or MVP+ | Provider / version                | Scenario / partner / role | Status | Evidence |
|-------|----------------------------------------------------------------|-------------|-----------------------------------|---------------------------|--------|----------|
| EBW   | EBW for legal-entity workflows                                 | MVP         | <to be filled by use case>        | Business/Technical roles  | ❔      |          |
| EUDI  | EUDI Wallet for legal representative to obtain EBWOID& & EUCC  | MVP         | <to be filled by use case>        | Business/Technical roles  | ❔      |          |


## Stage 1 – Role identification

| ID  | Requirement                           | Status | Owner | Evidence |
|-----|---------------------------------------|--------|-------|----------|
| 1.1 | Business role and scenario confirmed  | ⚪      |       |          |
| 1.2 | Technical roles and wallet assignment | ⚪      |       |          |

## Stage 2 – Wallet initialization and deployment

| ID | Wallet Type | Requirement | Status | Date | Evidence |
|---|-------------|---|---|---|---|
| 2.1 | EUDI / EBW  | Wallet installed, configured and reachable | ⚪ | | |

## Stage 3 – ITB onboarding

| ID | Requirement | Status | Date | Evidence |
|---|---|---|---|---|
| 3.1 | ITB portal access activated | ⚪ | | |
| 3.2 | Joined `#wp4-testing` and reviewed guidance | ⚪ | | |

## Stage 4 – ITB Basic Conformance

**Use-case lead:** Select applicable CS-01 and CS-02 cases for each wallet/role. Examples in the generic guide are not automatic requirements.

| ID | Wallet | Role                | Block | Test case ID                               | Required? | Status | Result | Execution date | Evidence / issue |
|---|---|---------------------|---|--------------------------------------------|---|---|---|---|---|
| 4.1 | W1 | defined by usecase  | CS-01 Issuance | To be specified by the use case in detail  | ❔ | ⚪ | Not run | | |
| 4.2 | W1 | defined by usecase  | CS-02 Presentation | To be specified by the use case in detail  | ❔ | ⚪ | Not run | | |

## Stage 5 – WEBUILD Trust List Registration

Refer to the role-specific registries, Access/Registration Certificate requirements and Holder exception in `WP4_Onboarding.md` Stage 5.

| ID | Role / credential type | Registration / certificate requirement                        | Required? | Status | Owner | Date | Registry / evidence / N/A reason |
|---|---|---------------------------------------------------------------|---|---|---|---|---|
| 5.1 | | IDunion Console contact/access (optional Raidiam access)       | ❔ | ⚪ | | | |
| 5.2 | | CSR / public certificate prepared                             | ❔ | ⚪ | | | |
| 5.3 | | Role-specific trusted-list entry                              | ❔ | ⚪ | | | |
| 5.4 | | Access Certificate issued                                     | ❔ | ⚪ | | | |
| 5.5 | | Registration Certificate issued (repeat per attestation type) | ❔ | ⚪ | | | |
| 5.6 | | Registration validated                                        | ❔ | ⚪ | | | |

## Stage 6 – Trust conformance (CS-Trust)

| ID | Wallet | Role | Test case ID | Required? | Status | Result | Date | Evidence / defect |
|---|---|---|---|---|---|---|---|---|
| 6.1 | W1 | | TBD | ❔ | ⚪ | Not run | | |

## Stage 7 – Sectorial-specific conformance

| ID | Wallet | Role | Block (e.g., CS-Issuer, CS-Signature) | Test case ID | Required? | Status | Result | Date | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 7.1 | W1 | | TBD | TBD | ❔ | ⚪ | Not run | | |

## Stage 8 – Role-specific prerequisite provisioning

**Use-case lead:** Define the required credentials and attestation types. Holder obtains credentials; Verifier imports schemas and prepares DCQL; Issuer configures schemas, test data and issuance. See generic Stage 8 for PID, QEAA, EAA, EBWOID, EUCC and Self-EAA instructions.

| ID | Role | Credential / prerequisite | Requirement (obtain / schema / DCQL / issue) | Required? | Status | Owner | Date | Evidence / dependency |
|---|---|---|---|---|---|---|---|---|
| 8.1 | Holder | TBD | Obtain credential | ❔ | ⚪ | | | |
| 8.2 | Verifier | TBD | Import schema and configure proof request | ❔ | ⚪ | | | |
| 8.3 | Issuer | TBD | Configure schema, test data and issuance | ❔ | ⚪ | | | |

## Readiness gate (before Stage 9)

| Check | Status | Evidence / approved exception |
|---|---|---|
| Applicable Stages 1–8 complete or exceptions approved | ⚪ | |
| No critical unresolved blocker preventing MVP execution | ⚪ | |
| Use-case lead authorizes Stage 9 execution | ⚪ | |

## Stage 9 – MVP interoperability execution and sign-off

**Use-case lead:** Define the actual scenario steps, participating roles, expected results and acceptance criteria. Only this tracker and its partner/scenario copies hold MVP execution results.

### Approved scenario test steps

| Test ID | Scenario step | Issuer / Holder / Verifier participant | Expected result / acceptance criterion | Owner | Required? |
|---|---|---|---|---|---|
| MVP-01 | TBD | TBD | TBD | | ❔ |

### Actual execution runs (append every run and retest)

| Run ID | Test ID | Date | Partner / wallet version | Actual result | Outcome | Evidence / log | Defect ID | Retest of | Executor |
|---|---|---|---|---|---|---|---|---|---|
| RUN-001 | TBD | | | | Not run | | | | |

### Acceptance and sign-off

| Criterion | Status | Evidence / approver / date |
|---|---|---|
| All mandatory scenario test steps passed | ⚪ | |
| Critical defects resolved or formally waived | ⚪ | |
| Evidence links complete and reviewed | ⚪ | |
| Use-case lead final sign-off | ⚪ | |

## Issues and blockers

| ID | Stage / test | Description | Severity | Owner | Opened | Status | Resolution / date |
|---|---|---|---|---|---|---|---|
| ISSUE-001 | | | | | | | |

## Change log

| Date | Author | Change | Baseline version |
|---|---|---|---|
| | | Tracker instantiated | |
