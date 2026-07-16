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

The ITB initially includes two credential-agnostic test suites:
- [Issuing (based on OpenID4VCI v1.0)](../conformance-specs/cs-01-credential-issuance.md)
- [Verifying (based on OpenID4VP v1.0)](../conformance-specs/cs-02-credential-presentation.md)

If a use case requires different functionality, it can propose a new or adapted (draft) WBCS. Once the WBCS and required supporting artefacts are available, the Testing Group implements the corresponding test cases in the ITB.

Some test cases require additional artefacts beyond the WBCS, such as rulebooks for attestation-specific requirements, and the corresponding data schemas, namespaces, and metadata.

When the required artefacts are available, the Testing Group implements the test cases in the ITB and communicates their availability to the consortium.

## Additional Documentation

[The ITB on GitHub](https://github.com/webuild-consortium/wp4-interop-test-bed) 

A [user guide](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/user-guide-interoperability-test-bed.md) on how to onboard and execute tests. 

[Documentation on the ITB and integrations](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md)
