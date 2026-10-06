# Testing and the Interoperability Testbed (ITB)

Once architectural decisions and specifications are defined, interoperability must be verified in practice. This chapter describes how interoperability is verified through the WE BUILD testing strategy and the Interoperability Testbed (ITB).

## Testing Strategy 
The Architecture Group coordinates the architectural building blocks and ensures alignment with the project use cases.

The Testing Group develops test cases and test suites for:
- Generic test cases based on WBCS.
- Functional test cases for required features (based on WBCS and, when needed, rulebooks and/or data schemas).
- End-to-end and piloting test cases for WP2/WP3 use cases (based on existing WBCS, rulebooks and data schemas).

To implement tests in the ITB, the Testing Group needs the specification artefacts: WBCS, rulebooks, data schemas, namespaces, and related metadata. The Architecture Group ensures that these artefacts are complete and consistent with the overall architecture and supports WP4 groups and WP2/WP3 use cases in providing the required input.

Most specification artefacts are produced within WP4:
- The Semantics Group: attestations (data schemas, namespaces, and relevant rulebook parts).
- The Wallet, PID/EBWOID and QTSP Group: WBCS and commitment to implement them.
- The Architecture Group: Architecture Decision Records (ADRs) that define the allowed scope for WBCS.
- The Trust Infrastructure Group: validation and verification requirements to be reflected in test cases.

For piloting-specific test suites, the Testing Group collaborates directly with the relevant use case(s). The Architecture Group acts as a facilitator to ensure consistency across the involved specifications.

## Test Requirements
Test cases are derived from the WBCS.

WBCS must stay within the scope defined by the published ADRs. If a WBCS needs functionality beyond that scope, it requires an ADR discussion. Testing focuses on features implemented by multiple parties, since interoperability requires multi-party implementations.

Implementing participants discuss WBCS together with the use cases that require the functionality.

If a use case requires different functionality, it can propose a new or adapted (draft) WBCS. Once the WBCS and required supporting artefacts are available, the Testing Group implements the corresponding test cases in the ITB.

Some test cases require additional artefacts beyond the WBCS, such as rulebooks for attestation-specific requirements, and the corresponding data schemas, namespaces, and metadata.

When the required artefacts are available, the Testing Group implements the test cases in the ITB and communicates their availability to the consortium.

## Test Case Structuring 
The ITB is set up with the following structure:

* Base Protocols
  * Conformance Test Suites supporting the generic, mandatory conformance specifications relevant to all use cases
  * Covering basic issuing/presentation (OID4VC) and the trust validation mechanisms (such as TL verification and WUA)
* Domain-Specific Functionalities and Generic Use Cases
  * Supporting standards and functionalities that are covering specific domain-requirements that are not part of all use cases
  * Examples are support for QES or DC APIs
* Business Use Cases
  * Test Suites that are composed of existing test cases covering the specific use case scenarios in the business use cases
  * Each use case has their own test suite
* Supply Chain Use Cases
  * Test Suites that are composed of existing test cases covering the specific use case scenarios in the supply chain use cases
  * Each use case has their own test suite
* Payment Use Cases
  * Test Suites that are composed of existing test cases covering the specific use case scenarios in the payment use cases
  * Each use case has their own test suite
* Reference Implementations
  * Test Suites covering individual implementations for specific test purposes
  * Examples are some individual Member State PID issuers and technology-providers that support relying parties

All test suites are versioned in their name (as well as in the description). Major versions are new releases of ITB test suites and will be mapped to WBCS releases on GitHub. Minor versions are ITB bugfixes. Versions are dated in the description.

## Showing Conformance

Participants can acquire a conformance report after running the test cases in a test suite. The Testing Group collects these conformance reports and publishes [a conformance overview](https://webuild-consortium.github.io/wp4-interop-test-bed/docs/conformance-overview.html). This overview currently lists conformance against Conformance Test Suite 1.0 (base protocols) and will be elaborated to cover the other test suites in the next few months.

## Additional Documentation

All information on testing is available with [the ITB on GitHub](https://github.com/webuild-consortium/wp4-interop-test-bed) 
This includes a user guide and other [documentation on testing and the ITB](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/overview.md)

