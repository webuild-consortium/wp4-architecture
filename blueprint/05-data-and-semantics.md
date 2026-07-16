# Information Inside the Wallet

While the previous chapter describes how wallets interact with services, this chapter describes the data and semantic structures used inside the wallet and in the exchanged attestations.

## Semantic Model of the European Business Wallet

The semantic model is organised into three layers:

1. Terminology – defines terms and their abstract concepts and establishes relationships between them.
2. Vocabulary – defines classes, properties, and individuals linked to the terminology.
3. Attestation mapping – maps vocabulary terms to the elements used in attestations.

The terminology and vocabulary layers are independent of attestation formats, while the mapping layer depends on the format used.

Currently, only W3C VCDM 2.0 supports machine-readable semantic mappings directly within credentials. For mDoc and SD-JWT-VC, the meaning of data fields must instead be defined in attestation rulebooks. In these cases, semantic interoperability between attestations is not automatically enforced.

### WE BUILD Terminology 
[The WE BUILD terminology](https://sanastot.suomi.fi/en/terminology/webuild) is published online and serves as a reference model for the terminology of the European Digital Identity Framework. The terminology is defined using the [Simple Knowledge Organisation System (SKOS)](https://www.w3.org/2004/02/skos/).

### European Business Wallet Vocabulary
The European Wallet vocabulary is maintained in [GitHub](https://github.com/webuild-consortium/wp4-semantics-group/tree/main/vocab).
It is defined using the [Web Ontology Language (OWL)](https://www.w3.org/OWL/), which specifies classes, properties and individuals of the vocabulary.  

To support semantic interoperability, credential subjects used within the EBW framework are modelled in the vocabulary. These vocabulary terms are then mapped to the corresponding elements used in attestations.

If the credential format supports machine-readable semantic contexts, the mapping between credential data and the vocabulary can be embedded in the credential itself. Otherwise, the meaning of the data fields must be defined in attestation rulebooks, and the rulebook owner is responsible for mapping those fields to the vocabulary definitions.

**Reuse of existing vocabularies** 
The EBW vocabulary defines the domain-specific vocabulary used in the WE BUILD attestations. Existing vocabularies are reused where possible, including those for credential metadata, proof mechanisms, security, decentralised identifiers, and credential status. Domain vocabularies from other sectors may also be reused (for example, digital product passports, supply chains, education, railway and data spaces).

## Attestation Rulebooks and Credential Schemas
WE BUILD defines rulebooks and credential data schemas for the attestations used in the project’s use cases. Rulebooks describe requirements, roles, processes, and conformance criteria for specific attestations. They also define how credential data fields relate to the semantic vocabulary used in the project.

Credential schemas define the structure of credential data and support implementers in producing interoperable credentials and validating that the data follows the agreed format.

Rulebook descriptions are currently provided by the use cases using a common template and are maintained in the project collaboration portal. As part of the ongoing work to formalise rulebooks and credential schemas, these descriptions will be consolidated in a shared repository such as the [WE BUILD Attestation Rulebooks repository](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/tree/main/rulebooks), including rulebooks for key credentials such as PID and EBWOID.
