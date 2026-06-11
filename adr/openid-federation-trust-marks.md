# Extend TS11 credential metadata with OpenID Federation Trust Marks

**Authors:**

- Leif Johansson, SIROS Foundation, Sweden

**Obsoletes:** N/A

**Obsoleted by:** N/A

## Context

The consortium has decided to [publish consortium trusted lists](trusted-lists.md) based on ETSI TS 119 612. The TS11 credential metadata specification already supports three trust framework types in the `trustedAuthorities` array: `aki`, `etsi_tl`, and `openid_federation` (per OID4VP Section 6.1.1).

However, the current TS11 `TrustAuthority` model only carries a framework type and a value (trust anchor identifier). For OpenID Federation, this is insufficient: knowing the Trust Anchor entity identifier tells a verifier *where* to resolve a trust chain, but not *what authorization* the issuer must demonstrate for the specific credential type. OpenID Federation Trust Marks ([OpenID Federation 1.0, Section 7](https://openid.net/specs/openid-federation-1_0.html#section-7)) provide this missing binding — a Trust Mark is a signed assertion by a Trust Mark Issuer that an entity satisfies specific criteria.

ETSI Trusted Lists solve this binding internally through service type identifiers within the list itself. OpenID Federation has no equivalent built-in mechanism for tying a trust chain to a specific credential type authorization. Trust Marks fill this gap.

Without this extension, a verifier evaluating an `openid_federation` trust authority can confirm the issuer has a valid trust chain to a Trust Anchor, but cannot determine whether the issuer is actually authorized to issue the specific credential type in question.

## Decision

### Extend the TS11 `TrustAuthority` model

The `TrustAuthority` object is extended with two optional fields that apply when `frameworkType` is `openid_federation`:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `frameworkType` | string | yes | (existing) Trust framework type. One of `aki`, `etsi_tl`, `openid_federation`. |
| `value` | string | yes | (existing) Trust Anchor entity identifier (URI). |
| `isLOTE` | boolean | no | (existing) Set `true` for ETSI List of Trusted Lists. Only applicable when `frameworkType` is `etsi_tl`. |
| `trustMarkId` | string | no | URI identifying a Trust Mark that the issuer MUST hold. Only applicable when `frameworkType` is `openid_federation`. |
| `trustMarkIssuers` | array of strings | no | URIs of Trust Mark Issuers whose Trust Marks are accepted. If omitted, the Trust Mark MAY be issued by any entity trusted by the Trust Anchor. Only applicable when `trustMarkId` is present. |

### Example

The following example shows a credential type with two `TrustAuthority` entries — one referencing an ETSI Trusted List and one referencing an OpenID Federation Trust Anchor with a Trust Mark constraint:

```json
{
  "trustedAuthorities": [
    {
      "frameworkType": "etsi_tl",
      "value": "https://tl.example.eu/tl.xml",
      "isLOTE": true
    },
    {
      "frameworkType": "openid_federation",
      "value": "https://trust-anchor.example.org",
      "trustMarkId": "https://trust-mark-issuer.example.org/trust-marks/pid-issuer",
      "trustMarkIssuers": [
        "https://trust-mark-issuer.example.org"
      ]
    }
  ]
}
```

### Semantics

1. When a `TrustAuthority` entry has `frameworkType: openid_federation` and a `trustMarkId` is present, a verifier evaluating this trust authority MUST confirm that:
   - The issuer has a valid trust chain to the Trust Anchor identified by `value`, **and**
   - The issuer holds a valid Trust Mark with the identifier specified by `trustMarkId`.

2. If `trustMarkIssuers` is present, the Trust Mark MUST have been issued by one of the listed Trust Mark Issuers. If `trustMarkIssuers` is absent, the Trust Mark MAY be issued by any entity; the verifier applies its own policy for Trust Mark Issuer acceptance.

3. When a credential type lists multiple `TrustAuthority` entries (potentially across different framework types), a verifier MUST satisfy **at least one** of them. This OR-semantic applies regardless of framework type — a verifier may evaluate an `etsi_tl` entry, an `openid_federation` entry, or both, depending on its capabilities and policy.

4. Trust Mark identifiers and Trust Mark Issuer identifiers are URIs defined by the respective Trust Mark Issuers. They are not namespaced to any specific registry operator.

5. The `trustedAuthorities` array is published as-is in the credential type metadata. Trust chain evaluation and Trust Mark validation are the responsibility of the consuming verifier, not of the registry or any specific implementation.

### Updated `TrustAuthority` JSON Schema

The TS11 `TrustAuthority` definition (Section 4.3.3) is extended with the new optional fields:

```json
{
  "TrustAuthority": {
    "title": "TrustAuthority",
    "description": "Applicable trust model/framework type and identifier for attestation type",
    "type": "object",
    "properties": {
      "frameworkType": {
        "description": "Trust framework type from OID4VP Section 6.1.1",
        "type": "string",
        "enum": ["aki", "etsi_tl", "openid_federation"]
      },
      "value": {
        "description": "Trust anchor identifier (URI or base64url-encoded, according to framework type)",
        "type": "string"
      },
      "isLOTE": {
        "description": "Set true for ETSI List of Trusted Lists. Only applicable when frameworkType is etsi_tl.",
        "type": "boolean"
      },
      "trustMarkId": {
        "description": "URI of a Trust Mark the issuer must hold. Only applicable when frameworkType is openid_federation.",
        "type": "string",
        "format": "uri"
      },
      "trustMarkIssuers": {
        "description": "Accepted Trust Mark Issuers for the specified Trust Mark. If absent, any issuer trusted by the Trust Anchor is accepted. Only applicable when trustMarkId is present.",
        "type": "array",
        "items": {
          "type": "string",
          "format": "uri"
        }
      }
    },
    "required": ["frameworkType", "value"],
    "additionalProperties": false
  }
}
```

## Consequences

### What becomes easier

- Credential type metadata can express fine-grained issuer authorization for OpenID Federation trust frameworks, on par with what ETSI Trusted Lists provide through service type identifiers.
- Verifiers can determine, from the registry metadata alone, what Trust Mark an issuer must hold — without out-of-band knowledge.
- Multi-framework deployments (ETSI + OIDF) can coexist in the same credential type definition with clear OR-semantics.

### What becomes more difficult

- Verifiers that support `openid_federation` trust authorities must now also implement Trust Mark validation if `trustMarkId` is present.
- The JSON Schema for `TrustAuthority` gains additional optional fields, which may require a schema version update in implementations that enforce `additionalProperties: false`.

### Risks and mitigations

- **Interoperability risk:** Different verifier implementations may interpret Trust Mark validation differently. Mitigation: the semantics are defined normatively above (valid trust chain AND valid Trust Mark).
- **Trust Mark Issuer discovery:** Verifiers need to discover and validate Trust Mark Issuers. This is handled by OpenID Federation's existing Trust Mark Issuer metadata and trust chain mechanisms — no new discovery protocol is needed.
- **Backward compatibility:** The new fields are optional. Existing `openid_federation` entries without `trustMarkId` remain valid and are evaluated as before (trust chain only, no Trust Mark requirement).

## Advice

Once merged, this is our consortium's decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

