# Context

What is forcing us to make this decision? What was the tradeoff?

1. Perspective of the Holder, Relying Party, Wallet Provider roles

Perspective of the EBW owner in the Holder role:

An EBW Owner in the Holder role stores highly confidential data in his EBW (e.g. UBO, Control Structure,...) that need to trated confidential and securely. Therefore a EBW Relying Party request for confidential data will be answered by the holder EBW only after the requesters identity and authorization and also the requesting software authenticity and validity (e.g. based on the WUA, if the request is made by an EBW) was validated by the Holders EBW.  

According to EU Business Wallet regulation Article 14/2/b"...Wallet units shall enable authentication and validation of the wallet unit components by presenting the wallet unit attestations…". 

The wallet unit attestations therefore increases trust in the integrity of the requesting software and significantly reduces the risk of impersonation of the requesting Relying Party. The wallet unit attestation revocation status also shows that the wallet is not revoked (e.g. due to compromise, ...)

From an holder security, confidentiality and legal perspective the requesters identification should be based on the EBWOID and the requesting software authenticity and components validity should be based on the WUA. Currently an EBWOID and a WUA are issued only to EBWs. Therefore a request made by a software component that is not part of the EBW like for example an "EUDI Wallet Relying Party Component" or an “EBW Relying Party Component" requesting confidential attestations will be ignored by EBW owners due to confidentiality, security and legal concerns. A Relying Party software component is less secure than an EBW. 

Perspective of the EBW Relying Party role:

Legal entities that already use a Relying Party component software (as defined by eIDAS2.0) for transactions with the EUDI wallet for natural person are interested that also EBW owners answer requests made to an EBW by a Relying Party component.  These legal entities are also interested to use the same component as a “EBW Relying Party component”

Perspective of the Wallet Providers:

Wallet providers may be interested to offer verification services based o a software component that has no Holder funtionality and does not contain attestations like the EBWOID and the WUA. Therefore they may be interested that identification of the verification component can be done also based on x.509 certificates comparable to the Access Certificate. However such a certificate is not a wallet bound issued certificate and therefore less secure from holder perspective and does not has the same legal value as the EBWOID.

2. Currently it is not defined how mutual identification between EBWs without human interaction is performed and the "OpenID for Verifiable Presentations (OID4VP) Specification" specifies:

- "The verifierInfo parameter allows the verifier to provide additional context or metadata as part of the authorization request. The verifierInfo parameter is optional. Wallets MAY use them to make authorization decisions or to enhance the user experience, but they SHOULD ignore any unrecognized or unsupported Verifier Info types."
We need a new verifierInfo type that includes at least the EBWOID and the WUA. This verifierInfo object SHOULD be used to request confidential attestations.

We may need additional verifierInfo types based on x.509 certificates that can be used

The  verifierInfo parameter MUST be made mandatory to avoid unnecessary denies from holder EBWs due to missing verifierInfo objects. 
- We need an interaction specification between relying party and holder EBW backends during a presentation request that does not require human interaction and that includes mutual authentication based on the above new verifierInfo object

The rulebook for mutual identification and consent handshake referencing also the rulebook for basic attestation verification describes the proposed solution: [https://github.com/flo0x/webuild-attestations/blob/main/rulebooks/rb-base/holder-authorization-handshake.md]
Note: The version available under the above link contains BU1 feedback and will replace the released version currently available under [https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/blob/main/rulebooks/rb-base/holder-authorization-handshake.md].
The two rulebooks describe mutual identification steps and basic verification steps required for all attestations and are part of the BU1 rulebooks.

# Decision:

What change did we agree to?

1. A new verifierInfo type will be defined [Where?]. The new verifierInfo type MUST contain an EBWOID and a WUA  attestations. The verifierInfo parameter in an authorization request MUST become a mandatory parameter.
An attestation request for confidential attestations from a Relying Party software MAY be answered or denied by the EBW owner based on his internal policies.

2. The Wallet Provider group will update the corresponding conformance specification [https://github.com/webuild-consortium/wp4-architecture/blob/main/conformance-specs/cs-02-credential-presentation.md] if the requirements resulting from the above rulebooks and this ADR are not fully included. Key requirements and goals are that a presentation can be performed without human interaction and that a presentation request includes mutual identification based on the above new verifierInfo object and the above rulebooks.

3. The above rulebooks should be included also in other attestation rulebooks


# Consequences

What becomes easier?

1. EBW owner will accept to present requested confidential attestations if the request is received from an EBW wallet with the new verfierInfo object according to their internal policies. They will not deny a request simply because the request is made via a Relying Party software.

2. Attestation request to an EBW backend based on OID4VCP protocols can be received and answered without natural person interaction. That is a mandatory prerequisite for BU use cases for the integration of the EBW in internal systems

3. We avoid that different rulebooks create different basic attestation rulebooks. The basic verification rulebook also explains how attestation chaining can be used to verify EAAs also after Web Build end.

What becomes more difficult?

1. Legal entities that use a Relying Party component will not be able to create the new verifierInfo object because they do not have the EBWOID, the WUA and also no wallet bound attestations. As a consequence several Holder EBW  will deny requests for confidential data made through the Relying Party software due to confidentiality, security and legal concerns (e.g. impersonation risk). The same EBW owner probably will answer a request made through an EBW by the same legal entity.

2. Without a common understanding between use case participants in different role (for example banks that want to use the EUDI Relying party component and their customers) the KyC and also PA3 use case can not be scaled.

How do we address the risks introduced by this change?

- The “EBW Relying Party component” is enabled by their providers to receive and store “EBW Relying Party component “ bound attestations like EBWOID and WUA and therefore able to create the verifierInfo object during a request for confidential data. That can be implemented by providing also the holder component to a verifier service, even if the customer of the Wallet Provider uses only the RP component.
- Additional verifierInfo object are defined based on other attestations and certificates that may be accepted by EBW holders for requests that do not require the presentation of confidential data.
- The fact that the use of an EBW wallet for requesting confidential data reduces the risk for the EBW holder must be explained and actively communicated to the RP legal entities that want to (re)use exclusively EUDI Relying Party components
