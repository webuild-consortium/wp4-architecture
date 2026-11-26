# Onboarding & Tracking 

**Purpose:** Define how UseCases manages generic onboarding guidance, scenario-specific requirements and evidence-based MVP execution tracking.

## Document architecture

| Document                   | Owner                                                   | Scope | Copies                                                                      |
|----------------------------|---------------------------------------------------------|---|-----------------------------------------------------------------------------|
| [webuild-onboarding.md](webuild-onboarding.md)        | WP4                                                     | Generic procedures, ITB, trust registration, conformance and prerequisite provisioning | **No.** Read and link to it. |
| [Tracking_template.md](Tracking_template.md) | WP4; generic template                                   | Scenario requirements and partner-specific status, evidence and MVP execution | **Yes**, into your use case's own repository |

**Separation of concerns:** 
- Onboarding describes **how**; 
- the scenario tracker specifies **what** is required; partner copies record **actual execution**. 
- No partner-specific progress or MVP test results belong in the generic documents.

## Nine-stage model

| Phase                                          | Stage | Activity                                    | Output in tracker                         |
|------------------------------------------------|-------|---------------------------------------------|-------------------------------------------|
| Identification and Wallet Setup                | 1     | Role identification                         | Confirmed business and technical roles    |
| Identification and Wallet Setup                | 2     | Wallet initialization and deployment        | Wallet inventory and operational evidence |
| ITB Onboarding and Basic Conformance           | 3     | ITB onboarding                              | Access confirmation                       |
| ITB Onboarding and Basic Conformance           | 4     | ITB Basic Conformance (CS-01, CS-02)        | Applicable test cases and results         |
| Trust and Role-Specific Conformance            | 5     | WEBUILD Trust List Registration             | Applicable registrations/certificates     |
| Trust and Role-Specific Conformance            | 6     | Trust conformance (CS-Trust)                | Selected cases and results                |
| Trust and Role-Specific Conformance            | 7     | Role-specific conformance                   | Selected CS-Issuer, CS-Signature, etc.    |
| Prerequisites Provisioning and MVP Execution   | 8     | Role-specific prerequisite provisioning     | Credentials, schemas, DCQL, test data     |
| Prerequisites Provisioning and MVP Execution   | 9     | MVP interoperability execution and sign-off | Test runs, evidence, defects, approval    |

**Execution dependencies:** Stage numbers establish a consistent reporting structure, not a strictly sequential timeline. Credentials and trust prerequisites may need to be prepared before a later-numbered stage is formally reached. The use-case lead approves dependencies and any exceptions.

## Scenario instantiation workflow

1. WP4 maintains the generic onboarding guidance and tracker template.
2. The use-case lead copies the tracker template **to the use case's own repository, not to this repository**: open [Tracking_template.md](Tracking_template.md), click **Raw**, copy the content and create a new file such as `onboarding/MVP_<UseCase>-<Scenario>_Tracker_Baseline.md` in the use case repository. The lead then defines roles, applicability, test cases, credentials, acceptance criteria and dependencies.
3. Create a partner tracker from the approved baseline for each partner and technical role combination.
4. Partners record status, dates, evidence, blockers and results. The use-case lead reviews exceptions and signs off the scenario.

Example naming: `MVP_PA3-S1_Bosch_Supplier_Holder.md` or '`MVP_PA3-S1_Freelance_Customer_Holder.md`  
Use `+` for combined technical roles and keep filenames free of spaces. Example names do not establish actual partner assignments.

## Tracking and status rules

Statuses: `Not started`, `In progress`, `Done`, `Blocked`, `Not applicable`, `To confirm`. For Stage 9 execution runs use `Not run`, `Pass`, `Fail`, `Blocked` and `Retest pending`.

- Mark `Done` only when the exit criteria are met and supporting evidence is recorded.
- Record a reason for every `Not applicable` decision and an owner for every blocker.
- Keep scenario requirements separate from actual results; never assume example tests are mandatory.
- A multi-role partner must cover all applicable roles and wallet instances.
- Do not infer MVP completion from conformance alone; Stage 9 requires recorded end-to-end interoperability evidence and use-case lead sign-off.

## Generic applicability guidance

| Role                           | Typical wallet                 | Stage 5                               | Stages 6–7                            | Stage 8                                  |
|--------------------------------|--------------------------------|---------------------------------------|---------------------------------------|------------------------------------------|
| Holder <br/> (natural person)  | EUDI Wallet                    | Holder exception where pure Holder    | As required by scenario               | Obtain relevant credentials              |
| Holder <br/> (legal person)    | EBW                            | Holder exception where pure Holder    | As required by scenario               | Obtain relevant credentials              |
| Verifier / RP                  | EBW or verifier implementation | Based on credential type and scenario | Trust/verification tests as specified | Import schemas and prepare DCQL requests |
| Issuer                         | Issuer implementation / EBW    | Based on attestation type             | CS-Issuer and other applicable tests  | Configure schema, data and issuance      |
| Intermediary / Wallet Provider | As specified                   | Scenario-dependent                    | Scenario-dependent                    | Scenario-dependent                       |

## Link, don't copy

The guide links to the sources maintained by other WP4 groups. In your use case documentation, **link to the same sources instead of copying their content**, so there is one place to update. If a source is missing or out of date, raise an issue in that group's repository.

| Topic | Source |
|---|---|
| Choosing a wallet | [Wallets directory](https://wallets.webuildconsortium.eu/) |
| Interoperability Test Bed | [ITB user guide](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/user-guide-interoperability-test-bed.md), [Use case testing](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/use-case-testing.md) |
| Trusted lists, Wallet Providers | [Wallet Provider onboarding](https://github.com/webuild-consortium/wp4-wallets-group/blob/main/guidance/trusted-list-onboarding/README.md) |
| Trusted lists, PID and EBWOID Providers | [Guidance for PID and EBWOID issuers](https://github.com/webuild-consortium/wp4-pid-ebwoid-group/blob/main/Guidance%20PID%20EBWOID%20Issuance.md) |
| PID and EBWOID issuers | [List of issuers](https://github.com/webuild-consortium/wp4-pid-ebwoid-group/blob/main/List%20of%20issuers.md) |
| Attestation rulebooks | [Rulebooks catalog](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks) |
| Conformance specifications | [WBCS](../conformance-specs/README.md) |
