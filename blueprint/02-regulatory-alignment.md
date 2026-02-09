# Regulatory and Foundational Alignment
The WE BUILD project is anchored in a  legal framework designed to reduce administrative burdens and strengthen the Single Market. Our architectural choices are driven by two key mandates: [Regulation (EU) 2024/1183](https://eur-lex.europa.eu/eli/reg/2024/1183/oj/eng) for natural persons and the [European Business Wallet proposal](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A52025PC0838) for economic operators.

Technical development follows mandatory rules such as the Article 5 revocation requirements and the "Business-Wallet-by-Default" principle, ensuring our infrastructure supports future initiatives. 

## Normative References
[To be added]
<!-- EUDI Wallet Mandate: Regulation (EU) 2024/1183, which mandates the issuance of wallets to natural persons at Level of Assurance (LoA) High. CIR still on its way, will be reopened.
EBW Proposal: COM(2025) 838 proposal. Explain that the EBW is intended for economic operators and public sector bodies to exchange data with full legal effect. CIR to come.
ARF
Standardisation work -->

### Standardization and Technical Specifications
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

## Compliance Expectations
How the Blueprint ensures alignment without duplicating specifications.
