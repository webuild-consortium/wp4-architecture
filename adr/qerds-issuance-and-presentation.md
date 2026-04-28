# Use QERDS for credential issuance and presentation interactions

**Authors:**

- Alejandro Nieto, DigitelTS, Spain

## Context

The WE BUILD conformance specifications for:

- credential issuance (`conformance-specs/cs-01-credential-issuance.md`, section “6. High-level Flows”), and
- credential presentation (`conformance-specs/cs-02-credential-presentation.md`, section “5. Protocol Overview”, step “4. Holder consents” and subsequent steps)

assume largely synchronous interactions (as it should because those are the most common) between a Wallet Unit (WU) and external parties (Issuer / Authorisation Server for issuance; Verifier for presentation), with wallet invocation mechanisms such as `openid-credential-offer://` and `openid4vp://`.

However, several WE BUILD scenarios can benefit from:

- asynchronous and/or automated interactions (agent-driven or back-office driven),
- reliable delivery with strong evidence of sending and receiving (registered delivery semantics),
- an ecosystem-aligned mechanism to route messages based on discovery functions (Digital Directory / capability discovery),

which are primary drivers for using a Qualified Electronic Registered Delivery Service (QERDS / “QeRDS”) in the European Business Wallet (EBW) context.

The QTSP group has defined a high-level QeRDS architecture and functional decomposition, including message submission/retrieval and evidence creation/retrieval, as well as interactions with common services (e.g. European Digital Directory) in `wp4-qtsp-group` documentation (“QERDS architecture”).

This ADR records how WE BUILD intends to apply QeRDS to credential issuance and presentation interactions, without changing the existing protocol profiles (OpenID4VCI + HAIP for issuance; OpenID4VP + HAIP for presentation) defined in the conformance specifications.

The QeRDS reference architecture used for this decision is: [QERDS architecture](https://github.com/webuild-consortium/wp4-qtsp-group/blob/main/docs/qerds/architecture.md).

## Decision

WE BUILD adopts QeRDS as an **optional, interoperable transport and evidence layer** for *credential issuance and presentation interactions* that benefit from registered delivery semantics (evidence) and/or cross-organisational routing needs.

This decision does **not** change the OpenID4VCI/OpenID4VP security models where the Wallet Unit (WU) establishes sender‑constrained channels to Issuer/Verifier endpoints.
In particular, WE BUILD does **not** (in this ADR) standardise sending the *issued credential* itself “through QeRDS” as a replacement for the OpenID4VCI Credential Endpoint response, because that would require additional profiling to avoid breaking assumptions around:

- sender-constrained access tokens and proof-of-possession at the Credential Endpoint,
- confidentiality/privacy controls and data minimisation (whether QeRDS carries the **credential payload** itself, or only a **reference**) 
- replay protection, binding, and lifecycle (e.g. ensuring a QeRDS-delivered credential is uniquely bound to the issuance transaction, has clear expiry/one-time semantics where applicable, and is not replayable out of context),

Specifically:

- **Issuance**:
  - QeRDS MAY be used to deliver a Credential Offer (or a reference to a Credential Offer) to a Wallet Unit, as an alternative to QR code / direct link delivery.
  - QeRDS MAY be used to deliver issuance-related notifications (e.g. “credential ready”, “issuance failed”, “action required”), including in deferred issuance scenarios in CS-01.
  - The underlying OpenID4VCI/HAIP HTTP endpoints (PAR, Authorisation Endpoint, Token Endpoint, Credential Endpoint, Deferred Credential Endpoint, metadata) remain unchanged; QeRDS is used as a delivery mechanism for *invocation* and *notifications* and to provide evidence.
  - Where use cases require **registered-delivery evidence** also for the *non-deferred* (immediate) issuance case, implementations MAY additionally use QeRDS to transmit a **receipt-style notification** (e.g. “credential issuance completed for transaction X”) so that both parties can retrieve QeRDS evidence of sending and receipt, while the credential itself is still delivered over the OpenID4VCI Credential Endpoint response.

- **Presentation**:
  - QeRDS MAY be used to deliver a Presentation Request (or a reference to it) to the Wallet Unit in scenarios where direct invocation (`openid4vp://`) is not suitable (e.g. automated/business flows or cross-organisational routing).
  - QeRDS MAY be used to deliver a Presentation Response (or a reference to it) back to the Verifier, when the presentation is performed in an asynchronous interaction pattern.
  - The wallet-side requirements in CS-02 remain unchanged for request validation and holder consent; QeRDS only changes how requests/responses are transported and evidenced.

- **Evidence and discovery**:
  - QeRDS providers MUST support evidence retrieval for send/receive events, so Wallet Units (and participating parties) can obtain timestamped, sealed evidence of transmission.
  - Identifier/service discovery and capability discovery SHOULD align with the Digital Directory assumptions in the QeRDS architecture, to route issuance/presentation messages to the correct recipient and endpoints.

This decision is intentionally scoped as a **transport pattern**: it does not redefine credential formats, trust models, or OpenID4VCI/OpenID4VP protocol details already covered by WE BUILD conformance specifications.

## Consequences

What becomes easier?

- Reliable, auditable delivery of issuance and presentation interactions across organisational boundaries, with evidence aligned to QeRDS semantics.
- Support for asynchronous issuance and presentation scenarios (including deferred issuance) without inventing ad-hoc notification channels.
- Applying common discovery/routing patterns (Digital Directory + capability discovery) to issuance/presentation interactions when the parties are not co-located or when direct invocation is impractical.

What becomes more difficult?

- Increased architectural and operational complexity: additional roles (QeRDS provider/QTSP), interfaces, and evidence lifecycle.
- Interoperability needs cross-group coordination (Wallet Providers, QTSP, Trust Registry Infrastructure, Testing) and conformance testing beyond “pure OpenID” flows.
- Potential duplication/confusion with existing invocation patterns unless profiles clearly specify when QeRDS is used and what content is transported (payload vs references).
- If WE BUILD later decides to transport the issued credential payload via QeRDS, additional profiling will be needed to preserve OpenID4VCI guarantees (token binding, confidentiality, replay protection) and to avoid creating a “push credential” variant that wallets/issuers implement inconsistently.
- Metadata footprint is broaden compared to the direct WU-to-Issuer/Verifier model, potentially making this model less unlinkable. 

How do we address the risks introduced by this change?

- Profile QeRDS usage as an *optional* pattern with clear applicability criteria (e.g. asynchronous/agent flows, registered delivery requirements).
- Use conformance testing to validate end-to-end behavior (delivery, evidence retrieval, replay protection, request validation, holder consent, response verification).
- Ensure implementations preserve the CS-01 / CS-02 security properties (e.g. sender-constrained tokens, signed requests, nonce/audience checks) regardless of transport.
- Use end-to-end encryption to prevent leaking the content being notified.

## Advice

Once merged, this is our consortium’s decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- 2026-04-28, Sander Dijkhuis, Cleverbase, Netherlands: Pointed out end-to-end encryption as a privacy preserving means for the notified content, aligned with the QeRDS EBW proposal.
- 2026-04-28, Lal Chandran, iGrant.io, Sweden: "Adding any relay between WU and Issuer/Verifier, QTSP-grade or otherwise, introduces a party that observes the interaction and is obliged to retain evidence about it."
