# Regulatory and Foundational Alignment

The WE BUILD architecture aligns with two key regulatory instruments: [Regulation (EU) No 910/2014](https://eur-lex.europa.eu/eli/reg/2014/910/oj/eng), as amended by [Regulation (EU) 2024/1183](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1183) (commonly referred to as the amended eIDAS Regulation), and the proposed [European Business Wallet proposal](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A52025PC0838) for economic operators.

## The EUDI Framework

WE BUILD aligns with the legal and technical framework for EUDI wallets. Users can authenticate and present identity and attribute information while retaining control over what data is shared through selective disclosure and explicit consent.

The amended eIDAS Regulation is supported by several implementing acts defining the technical and governance framework for the EUDI Wallet ecosystem, most importantly:

**Core Wallet Architecture and Technical framework**

  - [2024/2979 – Integrity and core functionalities](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402979)
  - [2024/2982 – Protocols and interfaces](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402982)
  - [2024/2981 – Certification framework](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402981)
  - [2024/2980 – Notification obligations within the Wallet ecosystem](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402980)

**Person Identification Data (PID) and Electronic Attestations of Attributes (EAA)**

  - [2024/2977 – PID and electronic attestations of attributes](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402977)
  - [2025/1569 – Electronic attestations of attributes](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501569)

**Wallet Ecosystem Governance and Relying Parties**

  - [2025/848 – Registration of wallet-relying parties](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500848)
  - [2025/849 – Submission of information on certified European Digital Identity Wallets](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500849)
  - [2025/847 – Reactions to Wallet security breaches](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500847)
  - [2025/846 – Cross-border identity matching for natural persons](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500846)

**Trust Services and QSCD Framework**

  - [2025/1566 – Verification of identity and attributes (QTSs)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501566)
  - [2025/1567 – rQSCD management](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501567)
  - [2025/1570 – Notification of certified or cancelled QSCDs](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501570)
  - [2025/1572 – QTSP initiation, notification and verification](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501572)

### Standardisation and Technical Specifications
The European Commission, together with the European Digital Identity Cooperation Group, has published:

- The [ARF](https://eudi.dev/latest/architecture-and-reference-framework-main/) specifies main functionalities, roles and responsibilities, architecture and design principles, attestation formats and protocols, trust model, certification, and risk management of the EUDI Wallet ecosystem.
- The [Technical Specifications](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/tree/main/docs/technical-specifications) specify more technical details of selected topics derived from the ARF. The technical specifications describe various topics such as Relying Party registration, zero-knowledge proofs, attestation rulebooks, schemas and catalogues.

Furthermore, there are several standardisation organisations that contribute with standards for the EUDIW ecosystem.

- **ETSI ESI:** [ETSI ESI](https://www.etsi.org/committee/esi) is a European Standardisation Organisation (ESO) that creates technical standards and European Norms for electronic identity and signatures supporting the eIDAS regulation. ETSI ESI has published approximately 80 standards for QTSP conformity assessment, protocols and formats for digital signatures, as well as protocols and formats for the EUDI Wallet. ETSI ESI has received the standardisation request [STF 705](https://portal.etsi.org/STFs/ToR/ToR705_EUDIW-Stan-project_with_Annexes.docx) from the EU Commission to create and/or update several standards for the EUDI Wallet ecosystem.
- **CEN TC224:** [CEN Technical Committee 224 (TC224)](https://standards.cencenelec.eu/ords/f?p=205:7:::::FSP_ORG_ID:6205&cs=1F02AD409B602B96990A87E2638AAA212) is an ESO that has published several standards related to identification and devices with secure elements. More specifically, CEN TC224 WG17 are standardizing Common Criteria protection profiles of QSCD/WSCA, CEN TC224 WG18 develop standards related to biometric solutions, whilst CEN TC224 WG20 are creating standards related to EUDI Wallet onboarding and access control.
- **ISO/IEC:** ISO is an international standardisation organisation and the International Electrotechnical Commission (IEC) develops international standards for electronic technologies. The international standardisation activities related to digital identities are performed within [ISO/IEC Joint Technical Committee (JTC) 1](https://www.iso.org/committee/45020.html) "Information Security". More specifically, several ISO/IEC standards are applicable to Common Criteria certification, conformity assessment and evaluation of the EUDI Wallet solutions. Furthermore, ISO/IEC has standardised the mobile driving license (ISO mDL) in ISO 18013-5, which is a PID format for the EUDI Wallet.
- **IETF:** The Internet Engineering Task Force (IETF) creates technical standards that comprise the internet protocol suites. More specifically, [IETF PKIX](https://datatracker.ietf.org/wg/pkix/about/) covers secure data exchanges and formats in the area of electronic signatures, PKI and trust services. Most notably, IETF has published standards for PKIX X.509 certificate and CRL profiles, OCSP, TLS and SD-JWT, which are relevant for the EUDI Wallet ecosystem. Furthermore, some of the IETF standards are used as basis by ETSI ESI, which have created European profiles of Qualified Certificates, AdES signature formats, SD-JWT VC, etc.
- **OpenID Foundation:** The [OpenID Foundation](https://openid.net/foundation/) is an industrial standardisation organisation that develops open standards for identity, federation and security. The following OpenID standards are relevant for the EUDIW technical architecture: OpenID Connect Core (OIDC), OpenID For Verifiable Credential Issuance (OID4VCI), OpenID For Verifiable Presentations (OID4VP), and OpenID High Assurance Interoperability Profile (HAIP). OID4VP, OID4VCI and HAIP are used as the foundation for the ETSI TS 119 472 standardisation of EUDI Wallet protocols.
- **W3C:** The [World Wide Web Consortium (W3C)](https://www.w3.org/) is an international standardisation organisation. The following W3C standards are relevant to the EUDI Wallet technical architecture: W3C Verifiable Credentials Data Model, W3C Web Authentication (WebAuthn), and W3C Digital Credentials API. More specifically, the W3C Verifiable Credentials Data Model is referenced as basis for an ETSI TS 119 472 EAA profile.
 - **Cloud Signature Consortium (CSC):** The [Cloud Signature Consortium (CSC)](https://cloudsignatureconsortium.org/) is an international standardisation organisation focusing on compliant digital signature creation in the cloud. The  CSC specification "CSC API v2 - Architectures and protocols for remote signature applications" is referenced by the EUDI Wallet architecture and is used as basis for the ETSI TS 119 432 standard.
 
In addition to the aforementioned standardisation organisations, the [European Cybersecurity Agency (ENISA)](https://www.enisa.europa.eu/) is developing the [EUDI Wallet Certification Scheme](https://certification.enisa.europa.eu/browse-topic/eudi-wallet_en), which will be published as an implementing regulation under the Cybersecurity Act. The purpose of the EUDI Wallet Certification Scheme is to harmonise the national certifications of the EU Member States' EUDI Wallets.

## The EBW Framework

The EBW framework is introduced through the European Commission’s [Digital Package proposal](https://digital-strategy.ec.europa.eu/en/news/simpler-eu-digital-rules-and-new-digital-wallets-save-billions-businesses-and-boost-innovation) as part of its 2025 Work Programme. The proposal aims to establish the EBW as a harmonised digital solution that reduces administrative burden and allows companies and public authorities to identify, authenticate and exchange data with legal effect across the European Union.

While the proposal is still in negotiation, every statement in this document may still change in the future. Below is the current history of the proposal we are building on:

- The Commission adopted the proposal, COM(2025) 838, on 19 November 2025.
- The Council adopted its negotiating position (general approach) at the TTE (Telecommunications) Council on 9 June 2026.
- The European Parliament has not yet adopted its position. The ITRE rapporteur's draft report PE785.244 was published on 20 March 2026, followed by further committee amendments and opinions from IMCO and JURI.
- Negotiations between the institutions (trilogues) are expected next. The Council Presidency has stated a target of political agreement by the end of 2026.

The EBW framework complements the EUDI framework by addressing the needs of economic operators and public authorities. It supports the digital management of representation rights and mandates, provides a secure channel for exchanging official documents and attestations, and includes support for a common directory. Interoperability with the EUDI Wallet is a core requirement.

The proposal supports the management and use of EAA, including owner identification data with selective disclosure. It defines requirements for authenticating owners and authorised users through (Q)EAAs and enables links between EAAs and other attestations. Access to EAAs by relying parties requires proper authorisation.

The framework relies on existing eIDAS trust services such as qualified electronic signatures, seals, timestamps and registered delivery services.

The proposal also introduces a European Digital Directory maintained by the Commission. The directory functions as a trusted internal system where EBW providers notify relevant service information and where digital addressing can be supported. Detailed requirements will be defined in future implementing acts.

The regulation supports role-based access so that multiple authorised users can operate a wallet. It also enables secure data exchange between EBWs, EUDI Wallets and relying parties, while allowing additional functionalities provided that core features remain unaffected.

From a technical perspective, the framework promotes the use of common protocols for sharing attestations. It requires secure onboarding using eID with a LoA of at least Substantial and mandates interoperability, secure communication interfaces, and mechanisms for validation and revocation. Further requirements will be defined in implementing acts.

Within WE BUILD, the proposed EBW framework is treated as a primary regulatory and architectural reference for business-focused identity and data exchange scenarios. Use case design and pilot activities align with the EBW model’s legal structure, interoperability requirements and trust-service framework, while taking forthcoming implementing acts into account.

### The principle of equivalence

The Regulation establishes a **principle of equivalence**:

> Where a wallet owner or authorised wallet user makes use of any of the qualified trust services forming part of core functionalities of a European Business Wallet referred to in Article 5(1), the resulting action has the same legal effect as if the action had been lawfully carried out in person, in paper form, or via any other means or processes compliant with applicable legal, administrative or procedural requirements.

The same applies where a self-employed person or sole trader uses the QERDS secure communication channel as a standalone service.

The principle has clear limits:

- It applies only to actions resulting from the use of core functionalities that are **functionally equivalent** to their traditional counterparts and serve the same purpose — for example qualified electronic signatures, seals and attestations of attributes. Council general approach specifies that the principle related only to **qualified trust services forming part of core functionalities** of the wallet.
- **National procedural requirements still apply.** Additional safeguards or verifications that are part of an administrative procedure and are not supported by the wallet's core functionalities must still be fulfilled.
- **Requirements on electronic formats remain applicable.** Where EU or national law requires an administrative step or a document in a particular electronic form, that requirement is observed.
- At the same time, such requirements may not be applied in a way that excludes the use of the wallet's core functionalities **solely because of their digital nature**.

Related principles: information validly transmitted via an EBW should not have to be submitted again through physical or alternative digital means, and vice versa; the Regulation is without prejudice to the once-only right of legal persons and to existing systems for exchanges between competent authorities; and Member States should not add national requirements on matters within the Regulation's scope.

### European Business Wallet Owner Identification Data (EBWOID) 
To uniquely bootstrap and identify an economic operator, the WE BUILD architecture formally replaces the concept of Legal Person Identification Data (LPID) with **European Business Wallet Owner Identification Data (EBWOID)**. The EBWOID consists of a stable, minimal set of identity attributes (primarily the official company name and its European Unique Identifier, EUID). For economic operators not covered by EUID/BRIS, such as sole traders and self-employed persons, national registration codes are used as the identifier baseline to ensure inclusive representation across use cases.

