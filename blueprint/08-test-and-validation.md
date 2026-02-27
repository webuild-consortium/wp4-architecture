# Proving It Works - Testing & The ITB

## Testing Strategy 
The Architecture Group coordinates the architectural building blocks and ensures alignment with the use cases. They collaborate with other WP4 groups to provide the specifications needed for testing.

The Testing Group develops test cases and test suites for:
- Generic test cases based on Conformance Specifications (CS).
- Functional test cases for required features (based on CS and, when needed, rulebooks and/or data schemas).
- End-to-end and piloting test cases for WP2/WP3 use cases (based on existing CS, rulebooks and data schemas).

To implement tests in the ITB, the Testing Group needs the specification artefacts: CS, rulebooks, data schemas, namespaces, and related metadata. The Architecture Group supports by ensuring these artefacts are complete and consistent with the overall architecture, and can assist WP4 groups and WP2/WP3 use cases in providing the required input.

Most specification artefacts are produced across WP4:
- The Semantics Group: attestations (data schemas, namespaces, and relevant rulebook parts).
- The Wallet, PID/EBWOID & QTSP Group: Conformance Specifications and commitment to implement them.
- The Architecture Group: Architecture Decision Records (ADRs) that define the allowed scope for CS.
- The Trust Infrastructure Group: validation and verification requirements to be reflected in test cases.

For piloting-specific test suites, the Testing Group collaborates directly with the involved use case(s). The Architecture Group acts as a facilitator to ensure consistency across the involved specifications.

## The Requirements Checklist 
Test cases are derived from the Conformance Specifications.

Conformance Specifications must stay within the scope defined by the published ADRs. If a CS needs functionality beyond that scope, it requires an ADR discussion. Testing focuses on features that are implemented by multiple parties, since interoperability testing depends on multi-party implementations.

Conformance Specifications are discussed by implementing participants together with the use cases that require the functionality.

The ITB is bootstrapped with two credential-agnostic test suites:
- [Issuing (based on OpenID4VCI v1.0)](../conformance-specs/cs-01-credential-issuance.md)
- [Verifying (based on OpenID4VP v1.0)](../conformance-specs/cs-02-credential-presentation.md)

If a use case requires different functionality, it can propose a new or adapted (draft) CS. Once the CS and required supporting artefacts are available, the Testing Group can implement corresponding test cases in the ITB.

Some test cases require additional artefacts beyond the CS, such as rulebooks for attestation-specific requirements, and the corresponding data schemas, namespaces, and metadata.

When the required artefacts are available, the Testing Group will implement the test cases in the ITB and communicate availability to the consortium.

## Read More - How testing is done

[The ITB on GitHub](https://github.com/webuild-consortium/wp4-interop-test-bed) 

A [user guide](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/user-guide-interoperability-test-bed.md) on how to onboard and execute tests. 

[Documentation on the ITB and integrations](https://github.com/webuild-consortium/wp4-interop-test-bed/blob/main/docs/reference-implementation-interoperability-test-bed.md)
