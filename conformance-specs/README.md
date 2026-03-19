# WE BUILD Conformance Specifications (WBCS)

## About
The WE BUILD Conformance Specifications (WBCS) define how WE BUILD participants implement wallet interfaces and communication protocols between issuers, wallets, and relying parties. 
They ensure interoperability and conformance by translating ADR decisions into precise implementation requirements.

The ITB will be based on the WBCS as a starting point. The test suites in the ITB are relying predominantly on the WBCS. 

## Contributing

The Architecture group define the WBCS, with help from all implementing participants. Propose new WBCSs using the [template](_template.md).

## CS Process Summary for WE BUILD Large Scale Pilots (LSPs)

```mermaid
---
config:
  flowchart:
    defaultRenderer: 'elk'
    subGraphTitleMargin:
      bottom: 25
---

graph TB
%% flowchart

    subgraph "WP4 (Architecture)"
        Proposal -- Discuss --> Review
        Review -- Rejected --> Proposal
        Review -- Approved --> WBCS
    end

    subgraph "Participants from WP2, WP3 and WP4"
        Implementations["Implementations
        (wallets, issuers, verifiers)"]
    end

    subgraph "Testing Group"
        ITB["ITB"]
    end

    WBCS -- "Guiding" --> Implementations
    WBCS -- "Configure" --> ITB
    Implementations -- "Test" --> ITB

    Anyone -- "Create/adapt" --> Proposal
    SpecEfforts["Specification efforts"] -- "New wallet interface definitions" --> WBCS
    TestDev["Test development"] -- "New version test cases" --> ITB
```

### Approved WBCSs

| **WBCS #** | **WBCS Title**                                                                         |
| -------- | ------------------------------------------------------------------------------------ |
| CS-001   | [Credential Issuance - v1.0](cs-01-credential-issuance.md)         |
| CS-002   | [Credential Presentation - v1.0](cs-02-credential-presentation.md) |
|          |

### WBCSs Under Development

| **WBCS #** | **WBCS Title** |
| -------- | ------------ |
|          |              |

