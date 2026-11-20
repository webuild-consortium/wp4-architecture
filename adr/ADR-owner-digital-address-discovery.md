# ADR-NNN: Business Wallet Registration with Digital Address and Endpoint Discovery

**Authors:**

- Boris Lingl, Datev, Germany
- Alexander Manecke, Deutsche Telekom, Germany

## Context

### Legal baseline

The European Commission proposal COM(2025) 838 is the legal basis for this ADR. It is not yet adopted and the positions of the Council and the Parliament may change the provisions cited below.

- **Art. 5(1)(j):** The provider assigns to each European Business Wallet (EBW) owner at least one unique digital address. The address is used for the qualified electronic registered delivery service and for the European Digital Directory (Art. 10).
- **Art. 8(3) and 8(5):** Owner identification data is issued by a qualified trust service provider, a public sector body responsible for an authentic source, or the Commission. Its minimum content is the official name and the unique identifier (Art. 9, EUID where available). The list is a minimum ("at least").
- **Art. 8(7) and 10(6):** Implementing acts may set requirements for owner identification data and standards for unique digital addresses. Neither act has been adopted, so the address format is not yet defined.
- **Art. 10(4):** Access to the Directory is limited to owners, their authorised representatives and providers. The text does not define how a Relying Party or an issuer obtains an owner's digital address.

**Assumption:** The EBW provider deposits the digital address with the Registrar, the register where the company is registered and where it obtains its EBWOID. The Registrar is therefore the authoritative source for the address.

In this ADR, the **Registrar** is the entity that issues the owner identification data (EBWOID) and maintains the owner's register entry.

**Assumption:** The Registrar issues the EBWOID. COM(2025) 838 assigns issuance to qualified trust service providers, public sector bodies responsible for an authentic source, or the Commission (Art. 8(3)). It does not name a registrar role. The assumption must be confirmed before the ADR is accepted.

### Existing WE BUILD decision

The ADR *Credential offer endpoint registry and lookup* decides that endpoints are registered by the Business Wallet Provider with the owner's opt-in. Issuers resolve endpoints through a permissioned lookup service. Resolution does not grant delivery rights, and the endpoint MUST enforce a consent or allow-list check at delivery time. The stated reason is that openly reachable endpoints would expose every wallet to spam and phishing.

### Problem

The discovery workshop identified a missing contract between a verified buyer identity and the wallet endpoint that can receive a credential offer. Current approaches rely on manually maintained mappings between traffiqx IDs, Peppol participant IDs and EBWOIDs. Each mapping is a maintenance burden and a source of error, and none of them proves that an endpoint belongs to the intended owner.

A company's Business Wallet must be reachable without manual mappings, and its endpoints must not be usable by unauthorised parties.

### Decision drivers

In priority order:

1. **Security:** Only authorised senders can deliver to an endpoint. Discovery cannot be used for enumeration.
2. **Scalability:** The number of issuers and Relying Parties must not create load on a single service.
3. **Privacy:** Public data is minimal.
4. **Simplicity:** Standard web and OAuth mechanisms, one authentication method.
5. **Conformance:** Consistent with COM(2025) 838 and the existing WE BUILD decisions.

### Alternatives considered

| Option | Advantages | Disadvantages |
| --- | --- | --- |
| A. Permissioned lookup only (existing ADR) | No public exposure. Owner controls access. | Central dependency for every issuer. Onboarding effort grows with the number of issuers. |
| B. Central metadata service (Commission Directory or WE BUILD service) | Single source of truth. Easy to audit. | Central bottleneck. The operator observes all queries. Art. 10(4) does not give issuers access. |
| C. Endpoint delivered in an OpenID4VP presentation at checkout | No discovery step. Fresh data. No public exposure. | Works only when the owner is present. Does not cover online invoices. |
| D. DNS-based discovery, as in Peppol SMP | Established pattern. | Requires new DNS infrastructure and a new registry. Less flexible than signed JSON. |
| E. Domain in the register entry with signed well-known metadata (**chosen**) | Works without the owner present. Scales through web infrastructure. Uses standard OAuth authentication. | Public metadata. Requires domain verification and key management. |

Option C is not adopted as an endpoint carrier. This ADR uses the presentation only as a source of the EBWOID (Discovery flow, step 1a). The endpoint itself comes from the signed metadata, so that endpoints are not tied to a single session. A follow-up ADR may still evaluate C as an additional path.

Pairing (source 1b) is an identity source, not a discovery option. It covers the case where the owner is not present, such as online invoices. It is not listed in the table above, because it does not compete with the discovery mechanisms.

## Decision

1. **Business wallet registration.** A company registers its Business Wallet with the Registrar. The register entry MUST contain:
   - the unique identifier of the owner (EUID, or the alternative identifier under Art. 9),
   - the wallet identifier,
   - the digital address (Decision 2),
   - the public keys used to verify the signature of the endpoint metadata (Decision 4) and to authenticate the wallet as a client (Decision 5).

   Private keys never leave the wallet. Issuers are not registered separately. An issuer authenticates with a key of a business wallet that is registered in its own name.

2. **Digital address.** The digital address is the domain of the owner's European Business Wallet (EBW). It is a DNS domain. It is either controlled by the company, or a subdomain under the provider's domain that is assigned to the company (for example `<wallet-id>.provider.example`). The Registrar MUST verify control of the domain before recording it, and MUST verify it again at each renewal. The verification method is to be specified (Open Points).

3. **Owner identification data.** The owner identification data issued by the Registrar MUST contain the digital address or a reference to the register entry that contains it. This extends the minimum attributes of Art. 8(5) and requires an implementing act under Art. 8(7).

4. **Endpoint metadata.** The wallet publishes signed metadata at `/.well-known/ebw-configuration`. The document is a JWS, signed with a key registered in the register entry, and its `kid` identifies that key. Its payload contains only the following:
   - `iss`: the digital address,
   - `wallet_id`,
   - `iat` and `exp`, with a validity period of at most 24 hours,
   - `token_endpoint`,
   - `endpoints`: for each endpoint, its `purpose`, the `credential_configuration_ids` it accepts, and the purpose-specific fields below.

   The defined purposes are:
   - `receive_credential_offer`: the wallet receives credential offers. Fields: `url` and `protocol_profile`, the latter a value from the protocol profile registry (Decision 10).
   - `credential_issuer`: the owner acts as an issuer. Field: `issuer_metadata_url`, which points to `/.well-known/openid-credential-issuer` on the same domain. The content of that document is defined by OpenID4VCI 1.0 and is not defined by this decision.

   The payload MUST NOT contain the owner's official name or the EUID. The binding to the owner is established through the register entry and the owner identification data, not through the public document.

   Illustrative payload (the JWS wrapper is omitted):

   ```json
   {
     "iss": "buyer-gmbh.example",
     "wallet_id": "buyer-wallet-001",
     "iat": 1799000000,
     "exp": 1799086400,
     "token_endpoint": "https://buyer-gmbh.example/token",
     "endpoints": [
       {
         "purpose": "receive_credential_offer",
         "url": "https://buyer-gmbh.example/offers/7f3c9a1e",
         "protocol_profile": "openid4vci-1.0",
         "credential_configuration_ids": ["ebw_einvoice_eaa", "ebw_ereceipt_eaa"]
       },
       {
         "purpose": "credential_issuer",
         "issuer_metadata_url": "https://buyer-gmbh.example/.well-known/openid-credential-issuer",
         "credential_configuration_ids": ["ebw_company_attestation"]
       }
     ]
   }
   ```

5. **Access control.** The endpoints are addressable, but they cannot be used without authentication. Each wallet MUST implement the following:
   1. **Token endpoint.** The issuer authenticates with OAuth 2.0 `private_key_jwt` (RFC 7523) using the `client_credentials` grant. The `client_id` is the issuer's registered wallet identifier. The client assertion has the following claims:
      - `iss` and `sub`: the `client_id`,
      - `aud`: the token endpoint URL,
      - `iat` and `exp`: `exp` at most 60 seconds after `iat`,
      - `jti`: a unique identifier.

      The assertion is signed with the issuer's private key. The wallet verifies the signature with the public key from the register entry. It MUST reject an assertion whose `jti` has already been used.
   2. **Access token.** The access token has a lifetime of at most 5 minutes, its audience is the offer endpoint, and its scope names the credential configurations.
   3. **Allow-list.** The owner holds an allow-list keyed by `client_id` and credential configuration. It is not published and is not based on IP addresses. Only the authorisation for an authenticated `client_id` is checked here.
   4. **Errors.** Unauthorised, unknown and unavailable requests MUST return the same status code and response body, and they MUST take a similar time to process, so that the existence of an owner or endpoint is not confirmed.
   5. **Rate limits.** Token requests and offer requests are rate-limited per `client_id` and per source.

6. **Discovery flow.**
   1. The issuer obtains the owner identification data (EBWOID) from one of two sources:
      - **a. Presentation at the point of sale.** The issuer requests an OpenID4VP presentation of the EBWOID from the buyer's wallet. The presentation MUST be bound to the key of the presenting wallet, so that a copied credential cannot be used.
      - **b. Pairing (for example for online invoices).** The owner has presented its EBWOID once in a pairing step. The issuer stores the digital address for a limited validity period. After expiry, the issuer MUST repeat the pairing or use source a.
   2. The issuer verifies the Registrar's signature on the EBWOID and, for source a, the holder binding of the presentation.
   3. The issuer reads the digital address from the EBWOID. The address is the domain of the owner's Business Wallet.
   4. The issuer retrieves `https://<digital address>/.well-known/ebw-configuration`, verifies the JWS signature against the register entry, and checks that `iss` equals the digital address, that `wallet_id` matches the register entry, and that `exp` has not passed.
   5. It selects the endpoint for the required purpose (`receive_credential_offer` or `credential_issuer`) and credential configuration.
   6. It obtains an access token using Decision 5.1, and delivers the credential offer with the access token.
   7. The wallet checks the allow-list and performs the consent check before it accepts the offer.

   On any failure the issuer MUST NOT reroute silently. It MUST fall back to an explicit alternative, such as a QR code, and log the failure.

7. **Relation to the existing registry decision.** This ADR amends the existing ADR in one point: endpoints are published in signed metadata, not only through the permissioned lookup. The remaining principles stay in force. Only opted-in endpoints are published, resolution does not grant delivery rights, and the endpoint performs a consent or allow-list check at delivery time.

8. **Relation to the European Digital Directory.** The Registrar's register entry is the authoritative source for the digital address. The Directory (Art. 10) mirrors it once its standards are adopted. The endpoint metadata is not held in the Directory.

9. **Scope.** This ADR covers the Business Wallets of companies and public sector bodies that send or receive credential offers. It does not cover Relying Party services or the Relying Party Register.

10. **Protocol profile registry.** The `protocol_profile` field identifies the protocol and profile that an endpoint supports. Its values are taken from a registry maintained by WE BUILD WP4. The initial registry contains one entry:

    | Value | Specification | Status |
    | --- | --- | --- |
    | `openid4vci-1.0` | OpenID for Verifiable Credential Issuance 1.0 | Active |

    Rules:
    - A value MUST follow the pattern `<protocol>-<version>`, using lowercase letters, digits and hyphens. A profile variant is registered as a new value, not as a parameter of an existing value.
    - A wallet MUST NOT publish a value that is not in the registry.
    - An issuer MUST reject an endpoint with an unknown value, fail closed, and log the event.
    - A new value is added by a new ADR or by a registry change approved by WP4. The change MUST reference the specification and a conformance test.
    - A deprecated value is marked as such with a sunset date. It is not removed while endpoints still use it.

## Consequences

### What becomes easier

- **Scalability.** Each wallet serves its own metadata. Issuers cache metadata, and the load does not grow with a central service. Issuers do not register separately, so onboarding does not require a central process for each issuer.
- **One authentication method.** Issuers authenticate with `private_key_jwt` at the token endpoint. No second mechanism is required.
- **Interoperability.** Issuers and wallets agree on a closed list of protocol profiles (Decision 10), so an unknown profile is rejected rather than negotiated.
- **Minimal public data.** The public metadata contains no owner name and no EUID.
- **Reuse of standards.** DNS, TLS, JWS and OAuth 2.0 are established and widely implemented.

### What becomes more difficult

- **Dependence on the Registrar.** The binding between digital address and owner is held by the Registrar. This is a central dependency per Registrar, although endpoint discovery itself is decentralised.
- **Public metadata.** The metadata reveals that an endpoint exists and which domain it belongs to. The concern behind the existing ADR is addressed by authentication at the endpoint, not by secrecy. Conformance tests must verify this.
- **Operational responsibility.** Each provider must operate its well-known endpoints, its token endpoint and its offer endpoint with high availability. Many domains mean many certificates.
- **Domain security.** A domain takeover or an expired domain redirects discovery. The Registrar MUST re-verify control at renewal. Issuers MUST reject metadata whose domain or certificate does not match the register entry.
- **Key lifecycle.** Keys must be rotated, and a compromised key must be revoked. A new key is published before the old one is retired. The Registrar removes a compromised key from the register entry, and the wallet re-signs its metadata. The maximum validity of 24 hours and of the access tokens bounds the exposure.
- **Provider change.** A provider change changes the domain (if it is a subdomain) and requires reissuance of the owner identification data. This is accepted as a design property.
- **Sole traders.** A sole trader's name and, where the domain is personal, the domain itself may be personal data. The legal basis for publishing this data must be assessed before the decision applies to sole traders.
- **Owners not present at checkout.** These owners are reached through pairing (source 1b). Pairing requires one presentation by the owner and has a limited validity period. Without a valid pairing and without a presentation, no discovery takes place, and the issuer falls back to the explicit alternative.
- **Issuers that are not EBW owners.** An issuing service that is not an EBW owner has no register entry of its own. Its operator's business wallet must hold the key, which must be confirmed.

### Threats addressed

| Threat | Mitigation |
| --- | --- |
| Domain takeover | Re-verification at renewal. Certificate check against the register entry. |
| Metadata manipulation | JWS signature with a key from the register entry. |
| Unauthorised delivery | `private_key_jwt`, allow-list, consent check. |
| Replay of client assertions | Short `exp` and single use of `jti`. |
| Enumeration of owners or endpoints | Identical errors and response times. Rate limits. |
| Denial of service | Rate limits. Caching of metadata within its validity period. |
| Key compromise | Revocation via the Registrar. Short validity periods. |

### Open points

1. **Domain verification method.** For example a DNS TXT record containing a value issued by the Registrar, and the renewal interval.
2. **Caching rule.** Issuers cache metadata for no longer than the time remaining until `exp` and at most 24 hours.
3. **Issuing services that are not EBW owners.** Which business wallet holds their keys, and how this is recorded.
4. **Sole traders.** The legal basis for publishing a sole trader's domain and endpoints.
5. **Well-known path.** Whether `/.well-known/ebw-configuration` is the final name.
6. **Follow-up ADR.** Option C (endpoint in the OpenID4VP presentation) and its relation to this ADR.

## Advice

No advice recorded yet.
