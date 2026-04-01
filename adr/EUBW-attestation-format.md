# Preferred EUBW attestation format

**Authors:**

- Ronald Koenig, Spherity, Germany

## Context

The Architecture and Reference Framework (ARF) currently focuses on the EUDI wallet for natural persons. The specific requirements of an EU business wallet (EUBW) for legal entities are not being thoroughly considered.

The ARF defines the following three attestation formats:

* `mDoc`: The format specified in [ISO/IEC 18013-5](https://www.iso.org/standard/69084.html) and generalised in [ISO/IEC 23220-2](https://www.iso.org/standard/86782.html),
* `SD-JWT-VC`: The format specified in 'SD-JWT-based Verifiable Credentials' [SD-JWT VC](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/),
* `W3C-VCDM`: The format specified in 'W3C Verifiable Credentials Data Model v2.0' [W3C VCDM 2.0](https://www.w3.org/TR/vc-data-model-2.0/).

It also states that the third format is optional and intended for non-qualified EAAs only. This means that the wallet ecosystem must use one of the first two options for PID, LPID and QEAAs.

Unfortunately, the first two options only allow the data structure of the attestation to be defined. They do not support mapping to globally defined semantic vocabularies. Global semantic interoperability cannot be achieved with these formats. This is accceptable for personal attestations with simple data structures (usually a flat list of data elements, e.g. mDL), which only require local semantic interoperability (e.g. defined within a local namespace, directly in the specification alongside the coding of the data [ISO/IEC 18013-5]( https://www.iso.org/standard/69084.html])). However, these formats are not suitable for use cases requiring deeply structured and linked attestations, such as expressing the share holder structure of a company for AML (anti-money laundering) compliance, or for attestations requiring semantic interoperability with globally defined vocabularies, e.g.:

* [eGoverment Core Vocabularies](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/e-government-core-vocabularies)
* [UN Transparency Protocol - UNTP Web Vocabularies](https://test.uncefact.org/vocabulary/untp/home)
* [European Union Agency for Railways](https://app.ontorail.org/ontorail)
* [Common data - schema.org](https://schema.org/)
* [DssC Dataspaces - Identity Credentials](https://dssc.eu/space/BVE2/1071254873/Building+on+Top+of+Foundational+Technical+Standards#2.1-Verifiable-Credentials)

Furthermore, modelling the complex attestations for the following WE BUILD use cases requires comprehensive conceptual modelling support. Neither the `mDoc` nor `SD-JWT-VC` format supports mapping to these models:

* BU1 'KYC/KYB/KYD/Due Diligence' regarding the semantic modeling of KYC credentials as well as complex authorisations schemes for natural persons acting on behalf of legal persons
* SC1 'Authentication and access for transport' regarding semantic alignment with public global vocabularies (e.g. railways)
* SC2 'Trusted data sharing for data spaces' regarding credentials to support authorization policies for the three phases of the DSP protocol (Catalog Query, Contract Negotiation and Data Transfer) as well as roles for automated actors and devices
* PA3 'Corporate banking and account opening': AML requires KYC and including delegation of authority

In addition to semantic interoperability at a business level, existing ecosystems also require semantic compatibility at a technical level:

* Verifiable credentials: [Verfiable Credentials Vocabulary](https://www.w3.org/2018/credentials/)
* Linked Data: [JSON-based Serialization for Linked Data](https://www.w3.org/TR/json-ld11/)
* Decentralized Identifiers: [DID](https://www.w3.org/ns/did/v1)

Finally, integration of complex attestations into existing business solutions require strong capabilities for handling and processing semantic data. JSON-LD, the serialisation format of `W3C-VCDM` Credentials, provides these capabilities:

* Global Linking of nodes of attestation data (e.g. share holder structures)
* Multi Key binding to nodes inside attestation data (e.g. list of legal representatvies)
* data transformation and canonicalisation (e.g. RDF Dataset Canonicalization)
* semantic data processing (e.g. semantic mapping of claims into existing master data) 
* data framing (e.g. selective disclosure and query of selected credentials and claims) 

Last but not least, `W3C-VCDM` credentials allows for:
* unambiguous interpretation of the data,
* giving stronger, legally sound transactions,
* more automation and reducing modelling (documentation) effort,
* supporting eco systems which already use `W3C-VCDM` credentials (e.g. data spaces, DPP, supply chains, etc.)

Restricting EUBW usage to `mDoc` and `SD-JWT-VC` would greatly reduce the range of supported ecosystems and implementation options. Furthermore, it becomes difficult or almost impossible to implement use cases requiring complex attestation, support for linked attestations, and interoperability with global semantic vocabularies.

## Decision

Define `W3C-VCDM` as the preferred attestation format for the EUBW.

Allow the use case owners to define the mandatory and optional attestation formats depending on the specific needs of their use cases.

Testing (ITB) needs to be conducted for all mandatory and optional attestation formats.

## Consequences

**What becomes easier?**

The range of supported use cases and ecosystems will increase significantly.

Reusing existing global vocabularies will improve cross-border interoperability and streamline the process of negotiating semantics across Europe, particularly with regard to finding common solutions to the different legal requirements of EU member states.

W3C provides a mature set of recommendations regarding verifiable credentials. Reusing these standards will significantly reduce the specification effort, provide a mature conceptual foundation, ensure clear separation of credential meta data and domain specific subject claims, achieve semantic interoperability and improve the quality of the solution.

**What will become more difficult?**

Supporting different attestation formats can result in extra mapping. Therefore, it is recommended that the preferred attestation format for EUBW (`W3C-VCDM`) is used to avoid extra mapping between formats.

JSON-LD adds additional semantic information to JSON data (`@context`, `@id` and `@type`). While this can introduce additional complexity for simple data, it improves semantic alignment and avoids extra mapping between local defined vocabularies. The use case owner should carefully select the most suitable attestation format, striking a balance between simplicity and interoperability. 

An interoperability profile based on existing standards (e.g. supported proof mechanisms, credential status methods, DID methods, etc.) should be defined to reduce complexity and testing effort. 

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
