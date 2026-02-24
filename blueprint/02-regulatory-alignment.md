# Regulatory and Foundational Alignment
The WE BUILD project is anchored in a  legal framework designed to reduce administrative burdens and strengthen the Single Market. Our architectural choices are driven by two key mandates: [Regulation (EU) 2024/1183](https://eur-lex.europa.eu/eli/reg/2024/1183/oj/eng) for natural persons and the [European Business Wallet proposal](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A52025PC0838) for economic operators.

Technical development follows mandatory rules such as the Article 5 revocation requirements and the "Business-Wallet-by-Default" principle, ensuring our infrastructure supports future initiatives. 

## EUDIW Framework

The WE BUILD consortium will anchor its work in the eIDAS legal framework - [Regulation (EU) No 910/2014](https://eur-lex.europa.eu/eli/reg/2014/910/oj/eng), as amended by [Regulation (EU) 2024/1183](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1183) (jointly referred to as “the Regulation”), which establishes the European Digital Identity Framework and defines the legal basis for the EU Digital Identity Wallet (EUDIW) ecosystem. This means WE BUILD’s use case designs, governance and assurance approach will be aligned to the Regulation’s requirements for a Wallet that is mutually recognised across the EU and usable in both public and private sector service contexts.

In practical terms, WE BUILD will rely on the EUDIW framework’s core policy commitments: enabling users to authenticate and present identity and attributes in a legally recognised manner, while ensuring that users retain control over data sharing (including selective disclosure and user consent as the operating principle). 


The Regulation is operationalized through several packages of Commission implementing regulations that harden the technical and governance requirements into enforceable rules. 

** Core wallet architecture and technical framework **
  - [2024/2979 – Integrity and core functionalities](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402979)
  - [2024/2982 – Protocols and interfaces](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402982)
  - [2024/2981 – Certification framework](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402981)
  - [2024/2980 – Notification obligations within the Wallet ecosystem](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402980)

** Person Identification Data (PID) and Electronic Attestations of Attributes (EAA) **
  - [2024/2977 – PID and electronic attestations of attributes](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402977)
  - [2025/1569 – Electronic attestations of attributes](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501569)

** Wallet ecosystem governance and relying parties **
  - [2025/848 – Registration of wallet-relying parties](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500848)
  - [2025/849 – Submission of information on certified European Digital Identity Wallets](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500849)
  - [2025/847 – Reactions to Wallet security breaches](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500847)
  - [2025/846 – Cross-border identity matching for natural persons](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500846)

** Trust services and QSCD framework **
  - [2025/1566 – Verification of identity and attributes (QTSs)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501566)
  - [2025/1567 – rQSCD management](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501567)
  - [2025/1570 – Notification of certified or cancelled QSCDs](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501570)
  - [2025/1572 – QTSP initiation, notification and verification](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202501572)


## EUBW Framework

The European Business Wallet framework is introduced through the European Commission’s [Digital Package proposal](https://digital-strategy.ec.europa.eu/en/news/simpler-eu-digital-rules-and-new-digital-wallets-save-billions-businesses-and-boost-innovation) published as part of its 2025 Work Programme. The [proposed Regulation on the establishment of European Business Wallets](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0838) aims to establish the EU Business Wallet as a harmonised digital solution to ease the administrative burden and to enable companies and public sector bodies to identify, to authenticate and to exchange data in a secure and user-friendly way, with full legal effect across the European Union.

The EUBW framework aims to complement the EUDI Framework by offering functionalities tailored to the needs of public sector bodies and economic operators, including the digital management of representation rights and mandates, and a secure channel for exchanging official documents and attestations supported by a common directory, while simultaneously ensuring full interoperability with the EUDIW.

The EUBW Regulation and the proposed regulatory framework are designed to ensure that European Business Wallets (EUBWs) support core functionalities such as the management and use of Electronic Attestation of Attributes (EAA), including owner identification data, with capabilities for selective disclosure. They establish requirements for authenticating owners and users through (Qualified) EAAs, enabling links between EAAs and other attestations, and ensuring that relying parties may access EAAs based on proper authorization.

The framework also foresees support for Qualified Electronic Signatures (QES), Qualified Electronic Seals (QESeals), and Qualified Electronic Time Stamps. The EUBW regulatory framework also aims to ensure the provision of a secure communication channel for transmitting and receiving electronic documents and data through Qualified Electronic Registered Delivery Services (QERDS), supporting confidentiality and integrity across the Union. This is envisioned as a single, standardised solution interoperable throughout Member States, with technical requirements to be defined in an implementing act. In parallel, the framework introduces a European Digital Directory maintained by the European Commission as a trusted and secure internal system for Business Wallet providers and users, where service providers notify relevant information. The directory is also intended to support digital addressing, with detailed specifications set out via implementing regulation.

To accommodate use by multiple authorized users, the regulation introduces provisions for a role-based access mechanism. It also facilitates secure data exchange between EUBWs, EUDI Wallets, and EUBW-relying parties, while allowing additional functionalities as long as core features remain unaffected.

From a technical perspective, the framework promotes the use of common protocols for sharing attestations, including identification data, and requires secure onboarding through eID means with a Level of Assurance (LoA) of at least substantial. It also mandates interoperability with other EUBWs and EUDI Wallets, secure communication interfaces, and robust mechanisms for validation and revocation.
Implementing regulations will further detail the requirements and functionalities of the EUBW.

The WE BUILD consortium will treat the proposed European Business Wallet (EUBW) regime as a primary regulatory and architectural reference point for business-focused digital identity and data-exchange scenarios: in designing and piloting its use cases, WE BUILD will rely on the EUBW model’s harmonised legal effect, interoperability with the EUDI Wallet ecosystem, and the prescribed trust services and attestation flows (EAAs, representation/mandates, secure delivery, directory-based trust), and will strongly consider the forthcoming implementing acts as the baseline for ensuring that its pilots remain future-proof, compliant-by-design, and readily scalable across Member States.


## Standardization and Technical Specifications
The WE BUILD consortium will rely upon several technical specifications and standards.

The European Commission in collaboration with the European Digital Identity Cooperation Group has published the EUDI Wallet Architecture and Reference Framework (ARF) and the related Technical Specifications.

- **The EUDI Wallet Architecture and Reference Framework (ARF):** The [EUDIW ARF](https://eudi.dev/latest/architecture-and-reference-framework-main/) is written by the EUDI Wallet Expert Group, supervised by the EU Commission DG-CNCT, and specifies the following aspects of the EUDI Wallet ecosystem: main functionalities, roles and responsibilities, architecture and design principles, attestation formats and protocols, trust model, certification, risk management.
- **The EUDI Wallet Technical Specifications:** The [EUDI Wallet Technical Specifications](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/tree/main/docs/technical-specifications) are created by the EU Commission, in collaboration with the European Digital Identity Cooperation Group and the European Standards Organizations (ESO), and specify more technical details of selected topics derived from the ARF. The technical specifications describe various topics such as Relying Party registrations, zero-knowledge proofs, attestion rulebooks, schemas and catalogues, etc.

Furthermore, there are several standardization organizations that contribute with standards for the EUDIW eco-system.

- **ETSI ESI:** [ETSI ESI](https://www.etsi.org/committee/esi) is a European Standardization Organization that creates technical standards and European Norms for electronic identity and signatures supporting the eIDAS regulation. ETSI ESI has published approximately 80 standards for QTSP conformity assessment, protocols and formats for digital signatures, as well as protocols and formats for the EUDI Wallet. ETSI ESI has also got the standardization request [STF 705](https://portal.etsi.org/STFs/ToR/ToR705_EUDIW-Stan-project_with_Annexes.docx) from the EU Commission to create and/or update several standards for the EUDI Wallet eco-system.
- **CEN TC224:** [CEN Technical Committee 224 (TC224)](https://standards.cencenelec.eu/ords/f?p=205:7:::::FSP_ORG_ID:6205&cs=1F02AD409B602B96990A87E2638AAA212) is a European Standardization Organization that has published several standards related to identification and devices with secure elements. More specifically, CEN TC224 WG17 are standardizing Common Criteria protection profiles of QSCD/WSCA, CEN TC224 WG18 are writing standards related to biometric solutions, whilst CEN TC224 WG20 are creating standards related to EUDI Wallet on-boarding and access control.
- **ISO/IEC:** ISO is an international standardization organization and International Electrotechnical Commission (IEC) develops international standards for electronic technologies. The international standardization activities related to digital identities are performed within [ISO/IEC Joint Technical Committee (JTC) 1](https://www.iso.org/committee/45020.html) "Information Security". More specifically, several ISO/IEC standards are applicable to Common Criteria certification, conformity assessment and evaluation of the EUDI Wallet solutions. Furthermore, ISO/IEC has standardized the mobile driving license (ISO mDL) in ISO 18013-5, which is a PID format for the EUDI Wallet.
- **IETF:** The Internet Engineering Task Force (IETF) create technical standards that comprise the internet protocol suites. More specifically, [IETF PKIX](https://datatracker.ietf.org/wg/pkix/about/) cover data secure exchanges and formats in the area of electronic signatures, PKI and trust services. Most notably, IETF has published standards for PKIX X.509 certificate and CRL profiles, OCSP, TLS and SD-JWT, which are relevant for the EUDI Wallet eco-system. Furthermore, some of the IETF standards are used as basis by ETSI ESI, which have have created European profiles of Qualified Certificates, AdES signature formats, SD-JWT VC, etc.
- **OpenID Foundation:** The [OpenID Foundation](https://openid.net/foundation/) is an industrial standardization organization that develops open standards for identity, federation and security. The following OpenID standards are relevant for the EUDIW technical architecture: OpenID Connect Core (OIDC), OpenID For Verifiable Credential Issuance (OID4VCI), OpenID For Verifiable Presentations (OID4VP), and OpenID High Assurance Interoperability Profile (HAIP). OID4VP, OID4VCI and HAIP are used as the foundation for the ETSI TS 119 472 standardization of EUDI Wallet protocols.
- **W3C:** The [World Wide Web Consortium (W3C)](https://www.w3.org/) is an international standardization organization. The following W3C standards are relevant to the EUDI Wallet technical architecture: W3C Verifiable Credentials Data Model, W3C Web Authentication (WebAuthn), and W3C Digital Credentials API. More specifically, the W3C Verifiable Credentials Data Model is referenced as basis for a ETSI TS 119 472 EAA profile.
 - **Cloud Signature Consortium (CSC):** The [Cloud Signature Consortium (CSC)](https://cloudsignatureconsortium.org/) is an internation standardization organization focusing on compliant digital signature creation in the cloud. The  CSC specification "CSC API v2 - Architectures and protocols for remote signature applications" is referenced by the EUDI Wallet architecture and is used as basis for the ETSI TS 119 432 standard.
 
In addition to the aforementioned standardization organizations, the [European Cybersecurity Agency (ENISA)](https://www.enisa.europa.eu/) is developing the [EUDI Wallet Certification Scheme](https://certification.enisa.europa.eu/browse-topic/eudi-wallet_en), which will be published as an implementing regulation under the Cybersecurity Act. The purpose of the EUDI Wallet Certification Scheme is to harmonize the national certifications of the EU Member States' EUDI Wallets.

## Architectural Principles
- **Interoperability:** This is our primary goal, ensuring that different wallet providers, issuers, and verifiers can communicate seamlessly across borders and different sectors. 
- **Reusability:** WE BUILD is designed to maximize efficiency by building upon existing EU digital infrastructures and successful results from previous Large Scale Pilots. 
- **Security-by-design:** Security is integrated into the architecture from the start, aiming at following the strict mandates for Level of Assurance (LoA) High for citizens and Substantial for business transactions. 
- **Privacy-by-design:** While business interactions require transparency and traceability, we need to ensure that users maintain sole control over their data. 

