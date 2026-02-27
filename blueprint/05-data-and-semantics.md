# The Information Inside the Wallet (Data & Content)

## Semantic Model of the European Business Wallet

The semantic model is defined across three layers.
1. The top layer is the terminology, which defines terms and their abstract concepts. This layer also establishes the relationships between these terms at an abstract level.
2. The second layer is the vocabulary. It defines classes, properties, and individuals. Each term in the vocabulary is linked to an abstract concept in the terminology.
3. The third layer involves mapping the vocabulary terms to the terms used in the attestations.

The top two layers are independent of the format of the attestations. The third layer, however, depends on the attestation format. Currently, only W3C VCDM 2.0 supports the mapping of semantic information into attestations. The meaning of the mDoc and SD-JWT-VC data fields needs to be provided in rulebooks. In this case, semantic interoperability between attestations isn't enforced.


## Webuild Terminology 
[The WE BUILD terminology](https://sanastot.suomi.fi/en/terminology/webuild) is hosted online and will serve as a blueprint for the final terminology of the European Digital Identity Framework.
The [Simple Knowledge Organisation System (SKOS)](https://www.w3.org/2004/02/skos/) is used to define the terminology.

## European Business Wallet Vocabulary
The European Wallet vocabulary is maintained in [github](https://github.com/webuild-consortium/wp4-semantics-group/tree/main/vocab).
The [Web Ontology Language (OWL)](https://www.w3.org/OWL/) is used to define classes, properties and individuals of the vocabulary. The terms of the vocabulary are linked to the concepts of the terminology to define their semantic.  

## Vocabulary mapping
To ensure semantic interoperability, all credentials subject used within the European Wallet Framework are model in the vocabulary. The terms defined in the vocabulary are mapped to the terms used in the attestations.
W3C VCDM 2.0 credentials support machine-readable semantic mapping. The context, which defines the mapping for this credential format, is referred in the published vocabulary and the credential data carry semantic information.
[JSON Linked Data](https://www.w3.org/TR/json-ld11/) is used to provide the mapping.

If the credential format does not support semantic information, the meaning of the data fields are described in attestation rulebooks. In this case, the rulebook owner is responsible for providing the mapping to the semantic definitions of the vocabulary.

## Reuse of existing vocabularies
The EBW vocabulary defines the domain-specific vocabulary of the WE BUILD attestations. Vocabularies for credential metadata, proof mechanisms, security, decentralised identifiers, and credential status already exist and are reused.
Furthermore, existing vocabularies for credential subjects of other domains are reused (e.g. digital product passports, supply chains, education, railway, dataspaces, etc.).
Reuse works straight away for W3C VCDM 2.0 credentials. However, for mDoc and SD-JWT-VC, the rulebook owner needs to map existing vocabularies to the attestations if applicable.

## Decentralised identifiers and identity binding
Linked data are based on unique identifiers. Cryptographic decentralised identifiers are used for identity binding. W3C credentials support holder binding and decentralised identities natively. They are an integral part of the semantic model. For other formats, identifiers and bindings are defined in the relevant rulebook by the rulebook owner.