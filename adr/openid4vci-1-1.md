# Pre-flight adoption of OpenID4VCI 1.1

**Authors:**

- Leif Johansson, SIROS Foundation, Sweden

## Context

CS-01 profiles OpenID4VCI 1.0, which has been Final since 9 July 2025. A 1.1
revision is in progress at the OpenID Foundation. It exists as an editor's
draft and has not been published.

The delta is small and well bounded. The draft's own change log opens with
"Initial draft created with same text as 1.0 Final", and nothing in 1.0 was
withdrawn. What 1.1 adds is one substantial feature and four corrections:

**Interactive Authorization.** A mechanism, cut late from 1.0 and now
restored, that lets an Issuer qualify the Holder before issuing without
sending the Wallet out to a browser. The Authorisation Server publishes an
Authorization Challenge Endpoint. The Wallet posts to it, declaring which
interaction types it supports. The server either returns an authorisation
code or answers 403 naming the one interaction it requires: a credential
presentation, answered back to the same endpoint, or a web step opened in an
external user agent. An opaque `auth_session` carries state across the
exchange, bound to the DPoP key where DPoP is in use. The presentation must
be cryptographically bound to the Challenge Endpoint, which is what stops a
malicious server relaying another server's challenge. The nonce must be bound
to the `auth_session`, which is what stops session fixation. The mechanism is
profiled on OAuth 2.0 for First-Party Applications.

**A distinct error for a wrong Transaction Code.** In 1.0 a Wallet that
submits the wrong Transaction Code receives `invalid_grant`, which is also
what it receives for a code that has expired or already been used. 1.1 adds
`invalid_tx_code` for the wrong-code case and reserves `invalid_grant` for a
code that is genuinely finished, including one invalidated by too many failed
attempts.

**Credential metadata on the Credential Response.** An optional
`credential_metadata` object may accompany the issued credential, with
precedence over Issuer metadata and format-specific mechanisms.

**Path normalisation for the Credential Issuer Identifier.** Where the
identifier has a path, any terminating `/` is removed before inserting
`/.well-known/openid-credential-issuer`. So `https://issuer.example.com/tenant`
and `https://issuer.example.com/tenant/` resolve to the same metadata URL.

**Registered identifiers** for the interaction types, under an OpenID
Foundation URN namespace.

Two of these matter to WE BUILD more than their size suggests.

`invalid_tx_code` is not a marginal case in this profile. CS-01 requires a
Transaction Code on every Credential Offer that uses the Pre-Authorised Code
grant, and requires Issuers to count failed attempts and invalidate the code
when a limit is passed. A wrong Transaction Code is therefore the most common
error this profile will generate, and under 1.0 the Wallet cannot tell "that
PIN was wrong, try again" from "this offer is dead, ask for a new one". That
is a difference the Holder sees.

Interactive Authorization speaks to a weakness CS-01 already documents at
length. Notes CS01_03 and CS01_04 record that the Pre-Authorised Code has no
PKCE-like binding, that anyone who obtains a code can attempt to redeem it in
their own attested Wallet Unit, and that the Transaction Code is the single
mitigation the design facilitates. Interactive Authorization answers the same
problem differently: the Authorisation Server can require the Holder to
present an existing credential before it issues, which binds issuance to the
person rather than to a shared secret delivered over a second channel. It does
not replace the Transaction Code requirement, but it gives Issuers a stronger
option where the Holder already has a credential the Issuer trusts.

Against that, 1.1 is not published, and reading the editor's draft turns up
two internal contradictions that would cost interoperability if implemented
literally. They are recorded under Consequences.

## Decision

WE BUILD adopts OpenID4VCI 1.1 as a pre-flight profile, under the terms of
the [pre-flight CS ADR](pre-flight-CS.md). CS-01 is updated to reference 1.1
alongside 1.0 and to profile the four corrections. Interactive Authorization
is admitted as OPTIONAL for Issuers and Wallets, and is specified far enough
to be testable.

Nothing is made mandatory that 1.0 does not already mandate. A Wallet or
Issuer conforming to the 1.0 profile remains conformant.

The purpose is to get Interactive Authorization and `invalid_tx_code` into
ITB+ testing while the OpenID Foundation draft is still open, so that what we
learn can be fed back to the working group rather than discovered after the
specification is Final.

## Consequences

### What becomes easier?

Issuers gain a way to qualify the Holder before issuance that does not route
the Wallet through a browser, and that binds issuance to a credential the
Holder holds rather than to a code in a text message.

Wallets can tell a wrong Transaction Code from a dead offer and say so.

Multi-tenant Issuers stop being a coin toss. Two implementations reading 1.0
literally can disagree about where `https://issuer.example.com/tenant/`
publishes its metadata, and 1.1 settles it.

Testing starts now rather than after publication, which is the point of a
pre-flight profile.

### What becomes more difficult?

`invalid_tx_code` is visible on the wire. A Wallet that has not been updated
will treat it as an unrecognised error, so Issuers should not switch to it
silently.

Interactive Authorization depends normatively on OAuth 2.0 for First-Party
Applications, an IETF draft that can still change.

We are not aware of a Wallet that implements the Authorization Challenge
Endpoint today, so the first ITB+ runs for this feature will be against
whatever the consortium builds.

### How do we address the risks introduced by this change?

The draft contradicts itself on naming. Its change log records renaming the
binding prefix to `iae:`, the response mode to `iae_post`, and the metadata
parameters to `interactive_authorization_endpoint` and
`require_interactive_authorization_request`. The normative text does none of
these and uses `ia:`, `ia_post` and `ia_post.jwt`,
`authorization_challenge_endpoint` and `require_interactive_authorization`.
CS-01 follows the normative text and says so, and implementations keep these
names configurable until the working group resolves it.

The draft also specifies the presentation binding inconsistently across
credential formats. SD-JWT VC says the audience is the derived Origin of the
Challenge Endpoint while its own example shows the full endpoint URL. JWT VC
JSON and LDP VC say the endpoint URL. ISO mdoc says the endpoint URL with no
prefix at all. Origin and URL are different strings, and this is the value
that defends against request forwarding, so a mismatch is a verification that
silently fails or silently passes. CS-01 pins one interpretation for testing
and records that it is provisional.

Both are reported to the OpenID Foundation as specification defects
([811](https://github.com/openid/OpenID4VCI/issues/811),
[812](https://github.com/openid/OpenID4VCI/issues/812); a third, the mdoc
handover hash, is [814](https://github.com/openid/OpenID4VCI/issues/814)). Neither
is worked around in CS-01 beyond pinning a value for testing.

Per the pre-flight CS ADR, what ITB+ finds is reported back to WP4 and informs
the next version of CS-01. This ADR is revisited when OpenID4VCI 1.1 is
published. If the published text differs from what we pinned, CS-01 follows
the published text.

## Advice

Once merged, this is our consortium's decision. This does not mean all
participants agree it is the best possible decision. In the decision making
process, we have heard the following advice.

- yyyy-mm-dd, Name, Affiliation, Country: OK or summary of advice
