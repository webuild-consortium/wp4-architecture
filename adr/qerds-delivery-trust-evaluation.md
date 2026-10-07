# Verify QERDS Provider trust via Trusted Lists before and after delivery

**Authors:**

- Martin Micuch

## Context

A sending QERDS Provider delivers a message with legal effect (eIDAS Art. 43-44) to another QERDS Provider that serves the addressee. This ADR builds on [Deliver business wallet data using QERDS](build-qerds.md), which establishes the QERDS as the designated delivery channel.

How a sending party learns which QERDS Provider serves a given addressee (discovery/routing) is out of scope of this decision; it assumes the sending QERDS Provider already has the receiving QERDS Provider's endpoint and certificate by the time the checks below run.

This decision relies on:

- LoTL and the relevant Trusted List(s) being available and consumable, per the trust evaluation base and Trusted List discovery/consumption work in the WP4 Trust Registry Infrastructure group;
- QERDS Providers being onboarded onto a national/pilot Trusted List with a `.../Svctype/EDS/Q` entry, per the QERDS Provider onboarding Trusted List profile.

## Decision

A sending QERDS Provider performs two trust checks against the Trusted List entry for the counterparty, in addition to the delivery transport itself:

1. **Before sending** — verify the receiving QERDS Provider's certificate against a `ServiceDigitalIdentity` listed under a `.../Svctype/EDS/Q` entry with `ServiceStatus` `.../Svcstatus/granted` on the applicable Trusted List. If no such entry exists, or its status is not `granted`, the message SHALL NOT be sent to that endpoint.
2. **After delivery** — verify the signature on the delivery evidence returned by the receiving QERDS Provider against that same `.../Svctype/EDS/Q` Trusted List entry, before accepting the evidence as proof of delivery.

The receiving QERDS Provider identifies the addressee before delivering, per eIDAS Art. 44.

The relevant service type identifiers are:

| Purpose | Service type identifier | Status value | Source |
|---|---|---|---|
| Qualified electronic registered delivery service (QERDS) | `http://uri.etsi.org/TrstSvc/Svctype/EDS/Q` | `.../Svcstatus/granted` | ETSI TS 119 612 clause 5.5.1.1(e) |

`ServiceDigitalIdentity` (TS 119 612 clause 5.5.3) is used to uniquely and unambiguously identify the services.

## Consequences

This decision makes it easier to:

- Ensure a QERDS message is sent only to a genuinely qualified delivery service, and that the returned delivery evidence can be trusted as coming from a qualified provider.
- Reuse the same Trusted List consumption logic (LoTL → Trusted List → `EDS/Q` entry) for both the pre-send and post-delivery checks, since both validate against the same entry.

This decision does not, by itself, prove that the receiving endpoint is the QERDS Provider *authorised to serve this particular addressee* — only that it is *a* genuinely qualified QERDS. This is an authentic-vs-authoritative gap:

| Situation | Caught by the trust layer? | How |
|---|---|---|
| Receiving endpoint is a fake or unqualified service | Yes | Trust check 1 finds no `EDS/Q` entry with status `granted` |
| Receiving endpoint's certificate does not match a listed entry | Yes | Trust check 1 / trust check 2 fail signature validation |
| Receiving endpoint is a real qualified QERDS but not the one authorised to serve this particular addressee | No | The Trusted List proves the QERDS is qualified, not that it is the right one for this addressee |

Under eIDAS Art. 44, the receiving QERDS Provider identifies the addressee before delivering, which limits — but does not eliminate at the Trusted-List level — the risk of a message reaching a qualified but wrong provider. Discovery/routing (how the sender learns the correct endpoint for an addressee) is out of scope here and needs to be addressed elsewhere to close this gap.

To address the residual risk, use cases and implementers should not treat trust-check success as proof of addressee-correctness; that guarantee comes from eIDAS Art. 44 addressee identification and from whatever discovery/routing mechanism supplies the endpoint, not from the Trusted List check itself.

## Advice

Once merged, this is our consortium's decision. This does not mean all
participants agree it is the best possible decision. In the decision
making process, we have heard the following advice.

- Discussed in [wp4-trust-group#127](https://github.com/webuild-consortium/wp4-trust-group/issues/127).
