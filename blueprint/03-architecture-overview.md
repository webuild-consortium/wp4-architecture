# Architecture Overview

## The Ecosystem at a Glance
The EU digital identity and EU business wallet ecosystem is an instance of the 3 party model for attestations. In this model there are 4 main actors:

1. The holder, aka the identity wallet that is controlled by either a natural or legal person
2. The issuer that relies on authentic sources of information to issue attestations to the holder/wallet
3. The verifier receives an attestation based on information present in the wallet.
4. The trust framework that in the EU ecosystems is based on ETSI TS 119604/119612 aka trust status lists populated by trust status providers that for some use cases are QTSPs


The EU ecosystem for the natural person wallet is described in more detail in [ARF]. The corresponding document for the EU legal person wallet is in progress.

Several sources exist for describing the more general 3rd-party model, including ongoing work in the IETF eg [https://datatracker.ietf.org/doc/draft-ietf-spice-vdcarch/]

## System Landscape

The diagram below illustrates the baseline trust topology of the EU wallet ecosystem. Issuers provide attestations to holders, holders present them to verifiers, and all parties anchor trust decisions against the EU trusted lists defined under ETSI TS 119 612 and ETSI TS 119 604 within the framework of the eIDAS Regulation.

```mermaid
%% Baseline trust topology of the EU wallet ecosystem
flowchart TB
    issuer["Issuer&nbsp;&nbsp;"]
    holder["Holder&nbsp;&nbsp;"]
    verifier["Verifier&nbsp;&nbsp;"]
    trust["WE BUILD Trusted Lists&nbsp;&nbsp;<br/><i>ETSI TS 119 612 / 604</i>"]

    issuer -->|"issues attestations<br/>(PID, EAA, QEAA)"| holder
    holder -->|"presents attestations<br/>(selective disclosure)"| verifier
    issuer -.->|"published in"| trust
    holder -.->|"validates issuer &<br/>verifier against"| trust
    verifier -.->|"validates<br/>credentials against"| trust

    %% Styling
    classDef primaryRole fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#000;
    classDef component fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#000;

    class issuer,holder,verifier primaryRole;
    class trust component;
```

---

In the WE BUILD project the focus is primarily on wallets for legal entities. In this case the regulation includes the use of qualified electronic registered delivery services to enable messaging services between entities in the ecosystem. Accordingly, the generic trust anchor is replaced by a Qualified Trust Service Provider operating a Qualified Electronic Registered Delivery Service (QTSP/QERDS), through which issuers, holders, and verifiers route their trust and messaging interactions. The European Digital Directory provides digital addressing for secure routing of documents and notifications. The diagram changes to this:

```mermaid
%% WE BUILD trust topology with QTSP/QERDS and European Digital Directory
flowchart TB
    issuer["Issuer&nbsp;&nbsp;"]
    holder["Holder&nbsp;&nbsp;"]
    verifier["Verifier&nbsp;&nbsp;<br/>(Relying Party)"]
    qtsp["QTSP / QERDS&nbsp;&nbsp;"]
    directory["European Digital<br/>Directory (Art. 10)"]

    issuer -->|"issues EBWOID &<br/>attestations"| holder
    holder -->|"presents attestations<br/>(selective disclosure)"| verifier
    issuer -.->|"signing/sealing certificates &<br/>revocation via QERDS"| qtsp
    holder -.->|"transmits/receives documents &<br/>signs/seals (Art. 5)"| qtsp
    verifier -.->|"sends/receives<br/>notifications via QERDS"| qtsp
    qtsp -->|"routes via<br/>digital addresses"| directory
    holder -.->|"registers<br/>digital address"| directory

    %% Styling
    classDef primaryRole fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#000;
    classDef component fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#000;
    classDef governance fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#000;

    class issuer,holder,verifier primaryRole;
    class qtsp component;
    class directory governance;
```

## Common Rules for Everyone
Security, error handling, auditability, portability.

## Wallet Implementation Models 
To be authored by Wallet Group. Describes the techn stacks, such as cloud-based vs. device-based solutions, and the differences between EUDIW for Natural Person and European Business Wallets for  economic operators.

### The EUDI Wallet for Natural Person

The diagram below provides a concept-level view of the EUDI Wallet ecosystem for natural persons (informative, non-normative).

```mermaid
%% EUDI Wallet concept model for natural persons
  flowchart TB
      %% --- Roles ---
      subgraph roles ["Roles"]
          direction LR
          H["Holder&nbsp;&nbsp;"]
          RP["Relying Party&nbsp;&nbsp;"]
          I["Issuer&nbsp;&nbsp;"]
          R["Role&nbsp;&nbsp;"]
      end

      %% --- Users & Identity ---
      subgraph identity ["Users & Identity"]
          direction LR
          U["User&nbsp;&nbsp;"]
          NP["Natural Person&nbsp;&nbsp;"]
          LP["Legal Person&nbsp;&nbsp;"]
          PP["PID Provider&nbsp;&nbsp;"]
          PID["PID&nbsp;&nbsp;"]
      end

      %% --- Wallet Solution ---
      subgraph solution ["Wallet Solution"]
          direction LR
          WP["Wallet Provider&nbsp;&nbsp;"]
          WS["Wallet Solution&nbsp;&nbsp;"]
          WCC["Wallet Core Component(s)&nbsp;&nbsp;"]
          WA["Wallet Application&nbsp;&nbsp;"]
      end

      %% --- Wallet Runtime ---
      subgraph runtime ["Wallet Runtime"]
          direction LR
          WIC["Wallet Instance&nbsp;&nbsp;"]
          WIT["Wallet Instance (External)&nbsp;&nbsp;"]
          WIA["WIA / WTE&nbsp;&nbsp;"]
      end

      %% Type relationships (solid)
      H -->|is type of| R
      RP -->|is type of| R
      I -->|is type of| R
      I -->|is type of| PP

      %% User relationships (solid)
      R -->|has| U
      U -->|is a| NP
      U -->|is a| LP
      U -->|controls| WIC

      %% Issuance (solid, thick)
      PP ==>|issues| PID
      WP ==>|issues| WIA
      WP -->|provides| WS

      %% Authentication & validation (dashed)
      U -.->|authenticated by| PID
      WIC -.->|defines type and validates| PID
      WIA -.->|validates| WIC

      %% Wallet structure (solid)
      WIC -->|instance of| WS
      WS -->|consists of| WCC
      WS -->|consists of| WA
      WCC -->|integrates with| WA

      %% Cross-wallet communication (dotted)
      WIT -->|communicates with| WIC

      %% Styling
      classDef primaryRole fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#000;
      classDef component fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#000;
      classDef walletPart fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#000;

      class H,RP,I,NP,LP primaryRole;
      class R,U,PP,PID component;
      class WP,WS,WCC,WA,WIC,WIT,WIA walletPart;

      %% Subgraph styling
      style roles fill:none,stroke:#d6b656,stroke-width:1px,stroke-dasharray: 5 5
      style identity fill:none,stroke:#9673a6,stroke-width:1px,stroke-dasharray: 5 5
      style solution fill:none,stroke:#b85450,stroke-width:1px,stroke-dasharray: 5 5
      style runtime fill:none,stroke:#b85450,stroke-width:1px,stroke-dasharray: 5 5
```
_Concept diagram for discussion and alignment. Terminology and role labels should be interpreted in line with the EUDIW ARF and the corresponding WE BUILD architecture artefacts._

### The Business Wallet for Economic Operators and Public Sector Bodies
The Business Wallet is described in further detail in [Appendix D](https://github.com/webuild-consortium/wp4-architecture/blob/main/blueprint/appendix-ebw-definition.md)

The diagram below provides a concept-level view of the European Business Wallet ecosystem for economic operators (informative, non-normative).

```mermaid
%% European Business Wallet concept model for economic operators
  flowchart TB
      %% --- Roles ---
      subgraph roles ["Roles"]
          direction LR
          H["Holder&nbsp;&nbsp;"]
          RP["Relying Party&nbsp;&nbsp;"]
          I["Issuer&nbsp;&nbsp;"]
          R["Role&nbsp;&nbsp;"]
      end

      %% --- Ownership & Identity ---
      subgraph identity ["Ownership & Identity"]
          direction LR
          O["Owner&nbsp;&nbsp;"]
          EO["Economic Operator&nbsp;&nbsp;"]
          U["User&nbsp;&nbsp;"]
          NP["Natural Person&nbsp;&nbsp;"]
          EP["EBWOID Provider&nbsp;&nbsp;"]
          EID["EBWOID&nbsp;&nbsp;"]
      end

      %% --- Wallet Solution ---
      subgraph solution ["EBW Solution"]
          direction LR
          EBP["EBW Provider&nbsp;&nbsp;"]
          EBW["EBW&nbsp;&nbsp;"]
          WCC["Wallet Core Component&nbsp;&nbsp;"]
          WA["Wallet Application&nbsp;&nbsp;"]
      end

      %% --- Wallet Runtime ---
      subgraph runtime ["Wallet Runtime"]
          direction LR
          EBI["EBW Instance&nbsp;&nbsp;"]
          EUDI["EUDIW Instance&nbsp;&nbsp;"]
          BW["BWUA&nbsp;&nbsp;"]
      end

      %% Type relationships (solid)
      H -->|is type of| R
      RP -->|is type of| R
      I -->|is type of| R
      I -->|is type of| EP

      %% Ownership relationships (solid)
      R -->|has| O
      O -->|is an| EO
      U -->|is a| NP
      O -->|controls| EBI

      %% Issuance (solid, thick)
      EP ==>|issues| EID
      EBP ==>|issues| BW
      EBP -->|provides| EBW

      %% Authentication & validation (dashed)
      O -.->|authenticated by| EID
      O -.->|is subject in| EID
      EBI -.->|validates| EID
      BW -.->|validates| EBI
      WCC -.->|validates| EBI

      %% Wallet structure (solid)
      EBI -->|instance of| EBW
      EBW -->|consists of| WCC
      EBW -->|consists of| WA
      WCC -->|integrates with| WA

      %% User & cross-wallet interaction (solid)
      U -->|accesses| WA
      EBI -->|communicates with| WA
      EUDI -->|communicates with| EBI

      %% Styling
      classDef primaryRole fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#000;
      classDef component fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#000;
      classDef walletPart fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#000;

      class H,RP,I,EO,NP primaryRole;
      class R,O,EP,EID,U component;
      class EBP,EBW,WCC,WA,EBI,EUDI,BW walletPart;

      %% Subgraph styling
      style roles fill:none,stroke:#d6b656,stroke-width:1px,stroke-dasharray: 5 5
      style identity fill:none,stroke:#9673a6,stroke-width:1px,stroke-dasharray: 5 5
      style solution fill:none,stroke:#b85450,stroke-width:1px,stroke-dasharray: 5 5
      style runtime fill:none,stroke:#b85450,stroke-width:1px,stroke-dasharray: 5 5
```
_Concept diagram for discussion and alignment. It illustrates a WE BUILD-style business wallet landscape_
