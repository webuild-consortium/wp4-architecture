# 1         Abstract

Relying Party Intermediaries serve as trusted intermediaries between Relying Parties and Wallet Holders, simplifying the integration of EUDIW capabilities while maintaining security and trust guarantees.

There are a number of critical technical challenges for RPI implementation, particularly around dual identification (distinguishing between the intermediary and the actual RP) and embedded disclosure policy evaluation. In order to ensure that the EUDIW implementations will allow for Intermediaries to play their role, Intermediaries should be tested in WE BUILD. These challenges require availability of certain infrastructure components and testing scenarios within the WE BUILD large scale pilot.

# 2         Background

## 2.1       Context

eIDAS 2 [1] explicitly recognizes the role of Relying Party Intermediaries in Article 5b 10: “Intermediaries acting on behalf of relying parties shall be deemed to be relying parties and shall not store data about the content of the transaction”. This role is also acknowledged in the ARF [i.2] and further detailed in sections 3.11.3 and 6.6.5.

## 2.2       The RP Intermediary Role

As defined in draft ETSI TR 119 479-1, an RP Intermediary is:

“A party that provides a service to Relying Parties related to the handling of the interaction with wallets (a.o. EUDIWs) or other solutions for identification, authentication or attribute attestation of persons.”

RP Intermediaries are also commonly referred to as “identity brokers” in existing electronic identification schemes. Their role is to abstract the complexity of wallet interactions, protocol implementations, and attestation validation, providing a unified interface for Relying Parties.

# 3         Importance of Interemediaries to the EUDIW ecosystem

Draft ETSI TR 119 479-1 identifies four key benefits that RP Intermediaries bring to the EUDIW ecosystem:

## 3.1       Inclusion

Small and medium enterprises (SMEs) and organizations without dedicated identity specialists will struggle to implement EUDIW integration independently. RP Intermediaries enable these organizations to participate in the digital identity ecosystem without requiring specialized in-house expertise.

**Impact:** Without RP Intermediaries, a significant digital divide would emerge between organizations with substantial IT resources and those without, limiting the reach and effectiveness of the EUDIW initiative.

## 3.2       Speed of Adoption

The scarcity of identity and cybersecurity specialists creates a bottleneck for EUDIW implementation. Organizations already integrated with an RP Intermediary can begin using EUDIW capabilities immediately once their intermediary supports it, rather than queuing for specialist resources.

**Impact:** RP Intermediaries break the “chicken and egg” problem by enabling rapid scaling of Relying Party adoption, which in turn increases wallet holder incentives to obtain and use EUDIWs.

## 3.3       Cost Efficiency

Building and maintaining interfaces and configurations for 27+ national EUDIW implementations represents substantial development and operational costs. RP Intermediaries amortize these costs across multiple Relying Parties.

**Cost Analysis:**

- **Direct integration**: Each RP must implement and maintain connections to all relevant wallet providers
  
- **Intermediated integration**: One-time integration with RPI, which maintains connections to all wallet providers
  
- **Economies of scale**: Shared infrastructure, expertise, and compliance costs
  

## 3.4       Security and Privacy

Organizations lacking identity specialists may implement EUDIW integration with suboptimal security and privacy controls, especially when under regulatory deadline pressure. RP Intermediaries can provide:

- Proven, audited implementation patterns
  
- State-of-the-art security controls
  
- Expert guidance and support
  
- Consistent privacy protection mechanisms
  

**NOTE**: Although Intermediaries have the potential to deliver these benefits, there is no guarantee that they will. Although the will have a crucial role regarding trust and security, there is currently no obligation for intermediaries to follow security best practices, let alone that they would be audited by independent auditors. Draft ETSI TR 119 479-1 recognizes this issue and proposes ETSI to develop a standard for Policy
and Security Requirements for Relying Party Intermediaries.

# 4         Architectural Patterns

## 4.1       Interaction Model

The RPI acts as a complete proxy between the Relying Party and the wallet:

Wallet Holder → EUDIW → RPI → Relying Party

**Characteristics:**

- RPI handles protocol negotiation with wallet
  
- RPI performs attestation validation
  
- RPI transforms attributes to RP-specific format
  
- No direct wallet-to-RP communication
  

**Trust Implications:**

- RPI processes privacy-sensitive information
  
- RP trusts RPI validation results
  
- Article 5b 10 prohibits RPIs from storing attribute data
  

## 4.2       Interaction Flows

### 4.2.1        Presentation Request Flow

1. **RP initiates authentication/attestation request**
  

- Specifies required attributes and policies
  
- Provides session context
  

2. **RPI generates wallet presentation request**
  

- Interacts with the user to initiate the EUDIW communication
  
- Translates RP requirements to wallet protocol (OpenID4VP, etc.)
  

3. **Wallet holder accepts EUDIW communication**
  

- Indicates the EUDIW to use
  
- Opens EUDIW and accepts request
  

4. **Wallet holder authorizes disclosure**
  

- Reviews requested attributes
  
- Consents to disclosure
  
- Wallet generates presentation
  

5. **RPI receives and validates presentation**
  

- Verifies cryptographic proofs
  
- Validates issuer trust status
  
- Checks revocation status
  
- Checks that the EAA / PID conforms to an EAA Policy that is acceptable for the given use case
  
- Applies EAA Policy rules and possibily additional
  

6. **RPI delivers attributes to RP**
  

- Formats attributes per RP requirements
  
- Provides validation assurance
  
- Includes audit information
  

### 4.2.2        Data Minimization and Privacy

RP intermediaries need to treat a high amount of privacy sensitive information. According to eIDAS 2 they are not allowed to store that data.

**Key Requirements:**

- **No Persistent Storage**: Attribute data must be processed in-memory only
  
- **Selective Disclosure**: RPI should request and forward only required attributes
  
- **Pseudonymization**: Support for user pseudonyms to limit correlation
  
- **Audit Logging**: Maintain non-repudiable audit trails without storing PII
  
- **Encryption in Transit**: All communications must use encryption
  

## 4.3       Trust and Security Requirements

### 4.3.1        Trust Service Provider Status

Draft ETSI TR 119 479-1 Annex B states that RP intermediaries have an important trust role, and as such should be considered similar to a Trust Service Provider. This recognition suggests that RPIs should at least meet security and policy requirements comparable to other TSPs. ETSI EN 319 401 (General Policy Requirements for Trust Service Providers) is a minimal basis. WE BUILD could deliver additional requirements adapted to the specific case of RPIs to ETSI for inclusion in a standard on the topic.

### 4.3.2        Validation Responsibilities

When an RPI validates attestations on behalf of an RP, it must:

1. **Verify Cryptographic Integrity**
  

- Validate digital signatures or seals
  
- Verify proof of possession (key binding)
  
- Check credential format compliance
  

2. **Assess Trust Status**
  

- Verify issuer is a trusted QTSP or recognized EAASP
  
- Validate certificate chains
  
- Check issuer authorization for attestation type
  

3. **Check Revocation Status**
  

- Query status lists or revocation services
  
- Respect validity periods
  
- Handle gracefully when status unavailable
  

4. **Apply Policy Rules**
  

- Verify compliance with EAA Policy requirements
  
- Check attribute quality requirements (what EAA Policies are acceptable to the RP)
  
- Validate attestation scheme conformance
  

5. **Provide Assurance Information**
  

- Communicate validation results clearly
  
- Flag any limitations or warnings
  

### 4.3.3        Liability Considerations

The introduction of RPIs into the trust chain raises questions about liability:

- **Contractual Liability:** Between RPI and RP
  
- **Regulatory Liability:** Under eIDAS 2 framework
  
- **Third-party Liability:** Toward wallet holders or attribute subjects
  

Clear liability frameworks and appropriate insurance coverage are essential for ecosystem confidence.

# 5         Technical Challenges for RPI Implementation

Real-world RPI implementations face several critical technical challenges that must be addressed for successful deployment. These challenges require testing and validation within the WE BUILD large scale pilot.

## 5.1       Dual Identification Challenge

**Challenge:** RPIs must manage and present two distinct identities in transactions: their own identity as the intermediary, and the identity of the actual Relying Party on whose behalf they are acting. Wallets must be able to correctly identify both entities and understand their relationship.

We need to consider two different scenarios, since the member states are not obligated to issue registration certificates.

**Scenario 1: Member state issues Registration Certificates**

1. **RPI Identity:** The intermediary obtains an Access Certificate identifying itself
  
2. **RP Registration:** Each RP using the intermediary service is registered with the member state
  
3. **Registration Certificate:** Contains:
  

- Which attributes the RP is authorized to request
  
- The link between the RP and the intermediary
  
- Proof that the RP is using the intermediary’s services
  

    **Transaction Flow:**

    - EUDIW receives a presentation request via the RPI

    - EUDIW identifies the intermediary via its Access Certificate

    - EUDIW verifies the Registration Certificate to confirm:

        - The intermediary is authorized to request attributes on behalf of the RP

        - The specific attributes being requested are authorized

        - EUDIW displays to the user both the actual RP and the intermediary

**Scenario 2: Member state does not issue Registration Certificates**

According to the ARF, when registration certificates are not available:

1. **Request Augmentation:** The intermediary includes in the presentation request:
  

- User-friendly name of the actual RP
  
- Unique identifier of the actual RP
  
- URL of the Registrar for the RP
  
- Identifier of the intended use
  

2. **Online Verification:** The EUDIW contacts the Registrar (at the provided URL) in real-time to verify:
  

- The RP’s registration status
  
- The relationship between the RP
  and intermediary
  
- Authorized attribute access
  

**Critical Gap:** At the moment of writing, no standardized interface specification exists for EUDIW-to-Registrar online verification. This represents a significant interoperability challenge.

**Cross-Border Complexity:**

- RPs must be registered in their home member state
  
- RPIs with international operations must support registration mechanisms from multiple jurisdictions
  
- Each member state may implement different registration approaches on top of the choice whether to use Registration Certificates or not
  

## 5.2       Embedded Disclosure Policy Challenge

**Challenge:** Electronic Attestations of Attributes (EAAs) may include embedded disclosure policies that specify which types of RPs are authorized to receive the attributes. The wallet must correctly evaluate these policies against the actual RP, not the intermediary.

**Context:** Annex III of CIR 2024/2979 [i.9] specifies how embedded disclosure policies allow attribute issuers can limit what relying parties are allowed to receive attribute of the attestation:

1. No policy
  
2. only authenticated relying parties which are explicitly listed in the disclosure
  policy.
  
3. only authenticated wallet-relying parties with wallet-relying party access certificates derived from a specific root (or list of specific roots) or intermediate certificate(s).
  

The wallet verifies whether the wallet-relying party complies with the requirements of the embedded disclosure policy and informs the wallet user of the result.

NOTE: The last option is based on the access certificate, not on the registration certificate. Since in the case of an intermediary, the access certificate identifies the RP
intermediary and not the RP, it is already clear that this is an issue. WE BUILD should try an alternative that is based on the Registration Certificate / online registrar identification, to propose a solution that can work in the case of an intermediary.

**The RPI Complication:** If the wallet evaluates the disclosure policy based on the
intermediary’s Access Certificate (which identifies the intermediary as, e.g.,
an “authentication service provider”), it will produce incorrect warnings even
when the actual RP is of an authorized type (e.g., included in the list in the
embedded disclosure policy).

**Correct Implementation Requirements:**

- The EUDIW must extract the actual RP identity from either:
  
  - The Registration Certificate (linking RP to intermediary), or
    
  - The online Registrar verification response
    
- The disclosure policy evaluation must be performed against the actual RP compliance, not the intermediary’s
  
- User interface must clearly indicate both the RP and intermediary while showing policy compliance for the RP
  

**Risk:** Incorrect implementation would result in:

- False warnings discouraging
  
- Potential security failures if disclosure policies are bypassed
  
- User confusion about who will receive their attributes
  

## 5.3       Testing Requirements for WE BUILD

To adequately test RPI implementations and resolve these challenges, the WE BUILD large scale pilot must provide the following infrastructure components:

**1. Access Certificate Issuance Infrastructure**

- Capability to issue Access Certificates to both: standard Relying Parties as Intermediaries acting on behalf of multiple RPs
  
- Certificates must follow ARF specifications for identification
  

**2. Registration Certificate Infrastructure**

- Implement Registration Certificate issuance supporting intermediary scenarios
  
- Registration Certificates must explicitly encode:
  
  - The relationship between RP and intermediary
    
  - Authorized attributes for the RP
    
- Support for testing with multiple registration models
  

**3. Online Registrar Implementation**

- Deploy a Registrar service implementing the online verification interface
  
- Enable testing of the “no registration certificate” scenario
  
- Document the implemented interface as input to future standardization
  
- Support real-time queries by wallet implementations
  

**4. EAA Issuance with Embedded Disclosure Policies**

- EAASPs capable of issuing attestations with embedded disclosure policies
  
- Test attestations that specify allowed RPs:
  
  - As a list in the embedded disclosure policy
    
  - Based on access certificate derived
    from a specific root (or list of specific roots) or intermediate certificate(s)
    
  - An alternative for the option
    above that would have the same effect, but could work with intermediaries
    

**5. Multi-Jurisdiction Simulation**

- Simulate registration approaches from multiple member states
  
- Test RPIs operating across different registration regimes
  
- Validate handling of heterogeneous trust infrastructures
  

**Priority:** These testing capabilities are essential for validating RPI implementations and identifying specification gaps that must be addressed before production deployment of EUDIW with intermediaries.

# 6         Intermediary Pilot Objectives

The WE BUILD large scale pilot has a unique opportunity to validate RPI implementations under realistic conditions and address critical technical challenges before widespread deployment. The pilot objectives are organized by priority, with the technical challenges identified in Section 5 taking precedence.

## 6.1       Critical Priority: Technical Challenge Validation

**Objective:** Test and validate solutions to the dual identification and embedded disclosure policy challenges that are essential for RPI operation.

1. **Dual Identification Testing**
  

- **With Registration Certificates:**
  
  - Deploy complete certificate infrastructure linking RPs to intermediaries
    
  - Validate wallet capability to display both RP and intermediary identities
    
  - Test attribute authorization checking via Registration Certificates
    
- **Without Registration Certificates (Online Registrar):**
  
  - Implement and document Registrar API for real-time verification
    
  - Test EUDIW integration with online Registrar
    
  - Measure reliability of online verification
    
- **Cross-Border Scenarios:**
  
  - Simulate multiple member state registration approaches
    
  - Test RPI handling of heterogeneous trust infrastructures
    
  - Validate user experience with international RPs
    
  - Test handling of intermediary and RP located in different member states
    

2. **Embedded Disclosure Policy Testing**
  

- Deploy EAASPs capable of issuing attributes with restrictive disclosure policies
  
- Test wallet evaluation of policies with intermediated requests:
  
  - Verify policy evaluated against actual RP, not intermediary
    
  - Confirm correct user warnings/approvals
    
  - Validate user interface clarity regarding policy compliance
    
- Test failure modes:
  
  - Policy violation detection
    
  - User override capabilities (if any)
    
  - Audit trail of policy decisions
    

3. **Standards Gap Identification**

- Document missing specifications discovered during testing
  
- Propose API specifications for online Registrar interface
  
- Identify ambiguities in ARF regarding intermediary handling
  
- Contribute findings to ARF, ETSI and other standards bodies
  

**Success Criteria:**

- All test scenarios from Section 5 executed and results collected
  
  - Does the disclosure policy evaluation complete?
    
  - Does wallet correctly identify RP and intermediary?
    
  - Are the disclosure policies evaluated against correct entity (RP, not RPI)?
    
- Online Registrar interface documented and validated by multiple implementations
  

## 6.2       Secondary Priority: Operational Validation

**Objective:** Test and validate the complete operational implementation of RP intermediaries, including

1. **Multi-Wallet Support**

- Integration with multiple EUDIW implementations

- Handling of heterogeneous attestation formats (W3C VC, mDL)

2. **Trust and Validation Infrastructure**

- Connection to trusted lists (QTSP lists)

- Real-time revocation checking

3. **Privacy Preservation**

- Demonstrable data minimization

- Audit logging without PII retention

- Support for pseudonymous presentations

- Compliance with eIDAS 2 prohibition on attribute storage
