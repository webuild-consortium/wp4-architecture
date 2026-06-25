# Relying Party Intermediary (RPI) Implementation Scenarios

## Overview

This document describes three implementation scenarios for Relying Party Intermediaries (RPI) where only the first one is the only compliant with the requirements defined in **ETSI TS 119 612 clause 5.5.1** and the **eIDAS 2.0 regulation** (Article 5b(10)).

## Terminology

| Term | Definition |
|------|------------|
| **RPI** | Relying Party Intermediary - registered as RP, acts on behalf of other RPs |
| **Subordinate RP** | A Relying Party using RPI services to interact with Wallet Instances |
| **Access Certificate** | Certificate for RP authentication to Wallet Units |
| **Registration Certificate** | Certificate containing RP registration data and intended use |

---

## Scenario 1: RPI Transparent Frontend (eIDAS Model)

**Real-world example:** Private organization providing aggregation services and interoperability solutions.

This scenario mets the following requirement:

> **Intermediaries acting on behalf of relying parties shall be deemed to be relying parties and shall not store data about the content of the transaction.**


### Description

The RPI is **transparent** to the Wallet Instance. Both the RPI and its Subordinate RPs are visible to the User.

### Requirements (per ARF HLRs)

| Entity | Access Certificate | Registration Certificate |
|--------|-------------------|-------------------------|
| **RPI** | ✅ Own certificate (RPI_01) | ✅ Own certificate (indicates intermediary role) |
| **Subordinate RP** | ❌ Not required | ✅ Own certificate (issued via RPI per RPI_03, contains association to RPI per RPRC_04) |

> **Clarification (per ARF HLLs):**
> - **RPI_01**: An intermediary SHALL register as a Relying Party, obtaining an access certificate containing its own name and unique identifier.
> - **RPI_03**: An intermediary SHALL register each intermediated Relying Party and receive a registration certificate for each registered intended use.
> - **RPI_06**: The intermediary SHALL include its own access certificate (RPI_01) and the registration certificate of the intermediated RP (RPI_03) in the presentation request.
> - **RPRC_04**: The registration certificate contains the 'association to the intermediary' (name and identifier) per CIR 2025/848 Annex I (15).
>
> Source: [ARF Annex 2.02 - Topic 52: Relying Party Intermediaries](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/main/docs/annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2330-topic-52-relying-party-intermediaries)

### High-Level Flow

```mermaid
graph TB
    subgraph "Trust Infrastructure"
        REG[Registrar]
        TL[Trusted List]
    end
    
    subgraph "RPI Provider"
        RPI[RPI<br/>Access Cert + Reg Cert]
    end
    
    subgraph "Subordinate RPs"
        SRP1[Subordinate RP 1<br/>Reg Cert only]
        SRP2[Subordinate RP 2<br/>Reg Cert only]
    end
    
    WI[Wallet Instance]
    
    REG -->|issues certs| RPI
    REG -->|issues reg certs via RPI| SRP1
    REG -->|issues reg certs via RPI| SRP2
    TL -->|trust anchor| WI
    
    SRP1 -->|request via| RPI
    SRP2 -->|request via| RPI
    RPI <-->|presentation| WI
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant WI as Wallet Instance
    participant RPI as RPI (Transparent)
    participant SRP as Subordinate RP
    participant REG as Registrar
    
    Note over SRP,RPI: Pre-registration (RPI_03, RPI_04)
    SRP->>RPI: Contract for intermediary services
    RPI->>REG: Register Subordinate RP + evidence
    REG-->>RPI: Subordinate RP Registration Certificate
    
    Note over User,SRP: Presentation Flow (OpenID4VP)
    
    User->>SRP: Request protected resource
    SRP->>SRP: Authentication required
    SRP-->>User: Redirect to RPI (authorization endpoint)
    Note right of SRP: Includes: state, client_id,<br/>intended use reference
    
    User->>RPI: Follow redirect
    RPI->>RPI: Build presentation request (RPI_05, RPI_06)
    Note right of RPI: Assemble: RPI Access Cert +<br/>Subordinate RP Reg Cert
    
    RPI->>WI: OID4VP Authorization Request
    Note right of RPI: request_uri or request object<br/>signed with RPI key
    
    WI->>WI: Fetch/parse request
    WI->>WI: Verify RPI Access Cert
    WI->>WI: Verify Subordinate RP Reg Cert
    WI->>WI: Check intermediary association (RPRC_04)
    
    WI->>User: Display BOTH names (RPI_07)
    Note right of WI: "RPI Name" acting for<br/>"Subordinate RP Name"
    
    User->>WI: Approve
    WI-->>RPI: VP Token (response_uri)
    RPI->>RPI: Verify VP, extract attributes
    RPI-->>SRP: Attributes (no storage per Art 5b(10)) using a format known to the SRP
    SRP-->>User: Access granted + session
```

---

## Scenario 2: RP Proxy Frontend

**Real-world example:** Private or Public organization with hundreds of services under same domain, same data regulation/handling, no cross-domain interactions.

### Description

The RPI is registered as a **pure RP**. Subordinate RPs are **NOT transparent** to the Wallet Instance - the User only sees the proxy RP identity.

### Certificate Requirements

| Entity | Access Certificate | Registration Certificate |
|--------|-------------------|-------------------------|
| **RP Proxy** | ✅ Own certificate | ✅ Own certificate (covers all services) |
| **Subordinate Services** | ❌ None | ❌ None (internal services) |

### High-Level Architecture

```mermaid
graph TB
    subgraph "Public Organization Domain"
        PROXY[RP Proxy<br/>Access Cert + Reg Cert]
        
        subgraph "Internal Services"
            S1[Service 1]
            S2[Service 2]
            S3[Service N...]
        end
        
        IAM[IAM System]
    end
    
    WI[Wallet Instance]
    REG[Registrar]
    
    REG -->|issues certs| PROXY
    WI <-->|presentation| PROXY
    PROXY <--> IAM
    IAM <--> S1
    IAM <--> S2
    IAM <--> S3
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant WI as Wallet Instance
    participant PROXY as RP Proxy
    participant IAM as IAM System
    participant SVC as Internal Service
    
    SVC->>IAM: User needs authentication
    IAM->>PROXY: Initiate wallet presentation
    
    PROXY->>WI: Presentation Request
    Note right of PROXY: Only Proxy's Access Cert<br/>(single registered RP)
    
    WI->>WI: Verify Proxy Access Cert
    WI->>User: Display Proxy RP name only
    Note right of WI: User sees: "Organization Name"<br/>(not individual service)
    
    User->>WI: Approve
    WI-->>PROXY: VP Response
    PROXY-->>IAM: Validated attributes
    IAM-->>SVC: Session/token with claims
    
    Note over PROXY,SVC: All under same data<br/>governance domain
```

---

## Scenario 3: RPI Backend

**Real-world example:** RP outsources trust evaluation, credential verification, and signature validation to specialized backend service.

### Description

The RP is registered as a **pure RP** with its own endpoints in access certificates (SAN URI). The RP frontend handles wallet communication but delegates all trust evaluation to the RPI Backend API.

### Certificate Requirements

| Entity | Access Certificate | Registration Certificate |
|--------|-------------------|-------------------------|
| **RP (Frontend)** | ✅ Own certificate (with SAN URIs for OID4VP endpoints) | ✅ Own certificate |
| **RPI Backend** | ❌ Not visible to wallet | N/A (API service) |

### High-Level Architecture

```mermaid
graph TB
    subgraph "RP Infrastructure"
        RP["RP Frontend<br/>Access Cert with SAN URIs"]
        subgraph "OpenID4VP Endpoints"
            REQ["request_uri"]
            RESP["response_uri"]
        end
    end
    
    subgraph "RPI Backend Service"
        API["RPI API"]
        TRUST["Trust Evaluation"]
        REV["Revocation Check"]
        SIG["Signature Validation"]
        CONV["Format Converter"]
    end
    
    WI["Wallet Instance"]
    REG["Registrar"]
    
    REG -->|issues certs| RP
    WI <-->|OID4VP| RP
    RP <-->|API + Token Auth| API
    API --> TRUST
    API --> REV
    API --> SIG
    API --> CONV
    
    CONV -->|"JSON/XML/SAML/ID Token"| RP
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant WI as Wallet Instance
    participant RP as RP Frontend
    participant RPI as RPI Backend API
    participant IS as Issuer Status
    
    Note over RP,RPI: RP authenticated to RPI API (token/mTLS)
    
    RP->>RPI: Create presentation request
    RPI-->>RP: Signed request object
    
    RP->>WI: OID4VP Authorization Request
    Note right of RP: RP's Access Cert<br/>(SAN: request_uri, response_uri)
    
    WI->>WI: Verify RP Access Cert
    WI->>User: Display RP name
    User->>WI: Approve
    
    WI-->>RP: VP Token (response_uri)
    
    RP->>RPI: Forward VP Token
    Note right of RP: RP doesn't process VP
    
    RPI->>RPI: Parse credentials
    RPI->>IS: Check revocation status
    IS-->>RPI: Status
    RPI->>RPI: Verify issuer signatures
    RPI->>RPI: Evaluate trust (issuer in trusted list?)
    RPI->>RPI: Convert to RP format
    
    RPI-->>RP: Validated data
    Note right of RPI: JSON / XML / ID Token /<br/>SAML2 Response / etc.
    
    RP->>RP: Process business logic
```

---

## Comparison Matrix

| Aspect | Transparent Frontend | Proxy Frontend | Backend |
|--------|---------------------|----------------|---------|
| **Wallet sees** | RPI + Subordinate RP | Proxy RP only | RP only |
| **Subordinate RP registration** | Required (via RPI) | Not required | Not applicable |
| **Access cert holder** | RPI | Proxy RP | RP |
| **Trust evaluation** | Wallet + RPI | Wallet + Proxy | RPI Backend |
| **Data flow** | RPI passes through | Proxy distributes | RP receives processed |
| **Use case** | Multi-tenant aggregation | Single-org multi-service | Outsourced verification |
| **Complexity** | High | Medium | Medium |

---

## References

- **ETSI TS 119 612** - Trusted Lists, clause 5.5.1
- **eIDAS 2.0 Regulation** - Article 5b(8) on intermediaries
- **ARF HLLs**: RPI_01, RPI_03, RPI_04, RPI_05, RPI_06, RPI_07, RPI_07a, RPRC_04
- **OpenID4VP 1.0** - Presentation request/response endpoints
- **CIR 2025/848** - Annex I, V on registration information

