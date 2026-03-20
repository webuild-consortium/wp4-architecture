# WE BUILD - Conformance Specification: <TITLE>

Version <VERSION>

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Scope](#2-scope)
- [3. Normative Language](#3-normative-language)
- [4. Roles and Components](#4-roles-and-components)
- [5. Protocol Overview](#5-protocol-overview)
- [6. High-level Flows](#6-high-level-flows)
- [7. Normative Requirements](#7-normative-requirements)
- [8. Interface Definitions](#8-interface-definitions)
- [9. Conformance](#9-conformance)
- [References](#references)

# 1. Introduction

This document defines the **WE BUILD Conformance Specification for <TITLE>**.

Its purpose is to describe how relevant actors within the WE BUILD ecosystem are expected to interoperate in a consistent and testable way.

This specification should:

- identify the relevant protocol or functional area
- clarify which actors are involved
- define the main requirements needed for interoperability
- support implementation and conformance testing

This specification is based on <BASE STANDARD / PROFILE / ADR> and should be read together with other applicable WE BUILD specifications where relevant.

# 2. Scope

This specification defines the conformance expectations for <DOMAIN / CAPABILITY>.

It should make clear:

- what this specification covers
- which roles are in scope
- which capabilities are required
- what is out of scope

Out-of-scope items should be listed where needed, especially if they are handled by other WE BUILD documents or external specifications.

# 3. Normative Language

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

These keywords indicate the strength of requirements for conforming implementations.

# 4. Roles and Components

This section identifies the roles and components relevant to this specification.

Only roles that matter for this specification should be included.

Examples may include:

- **Wallet Unit (WU):** software acting on behalf of the Holder
- **Holder:** person or organisation controlling the Wallet Unit
- **Issuer:** entity issuing credentials or attestations
- **Verifier:** entity requesting and validating presentations
- **Authorisation Server:** component supporting OAuth / OpenID interactions
- **Trust Provider:** component or service publishing trust-related information

# 5. Protocol Overview

This section gives a short explanation of how the protocol or function works at a high level.

It should help the reader understand:

- which standards or mechanisms are used
- how the main actors interact
- which security or trust features are important
- what the overall outcome of the interaction is

This section should stay concise. Detailed behaviour belongs in later sections.

# 6. High-level Flows

This section describes the main interaction flows between actors.

Flows should be written as step-by-step sequences that help implementers understand how the protocol operates.

Example subsections:

## 6.1 <Flow Name>

Describe:

- participating actors
- how the interaction begins
- the main sequence of actions
- the expected outcome

Example:

1. <STEP 1>
2. <STEP 2>
3. <STEP 3>

# 7. Normative Requirements

This section defines the normative requirements for implementations.

Requirements may be grouped in the way that best fits the specification, for example by:

- role
- component
- capability
- protocol step

Example structure:

## 7.1 <Role or Component>

<ROLE OR COMPONENT> **MUST**:

1. <REQUIREMENT 1>
2. <REQUIREMENT 2>

<ROLE OR COMPONENT> **SHOULD**:

1. <RECOMMENDATION 1>

<ROLE OR COMPONENT> **MUST NOT**:

1. <PROHIBITED BEHAVIOUR>

# 8. Interface Definitions

This section describes the technical interfaces used by the protocol.

Examples may include:

- HTTP endpoints
- wallet invocation URLs
- metadata endpoints
- credential request structures
- presentation responses
- trust registry queries

For each interface, describe:

- direction of communication
- transport method
- request parameters
- response structure

Example subsection:

## 8.1 <Interface Name>

*Direction:* <SENDER> → <RECEIVER>  
*Method:* <HTTP METHOD>

**Request**

- <FIELD 1>
- <FIELD 2>

**Response**

- <FIELD 1>
- <FIELD 2>

Example (illustrative only):

```text
<EXAMPLE REQUEST OR URL>
```
# 9. Conformance

An implementation **conforms to this specification** if it implements the requirements defined in this document for its role and supports the relevant interfaces and flows.

Where relevant, conformance may be stated separately for each role.

**Example**

An implementation conforms as a **<ROLE 1 CONFORMANCE CLASS>** if it:

1. implements the applicable requirements in Section 7  
2. supports the relevant interfaces and flows in Sections 6 and 8  
3. supports any required standards or formats referenced by this specification

Additional WE BUILD profiles may define stricter requirements for specific use cases. Such profiles **MUST NOT** weaken the mandatory requirements in this specification.

# References

[1] <ORGANISATION> (<YEAR>) <TITLE>. Available at: <URL> (Accessed: <DATE>).

[2] <ORGANISATION> (<YEAR>) <TITLE>. Available at: <URL> (Accessed: <DATE>).

[3] <ORGANISATION> (<YEAR>) <TITLE>. Available at: <URL> (Accessed: <DATE>).
