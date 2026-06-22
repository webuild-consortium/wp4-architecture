# EBW's EAA Extension for the EDD

**Authors:**

- Toennis Jonas, Puria Dyne, Rune Kjørlaug, Angel, Ssander Dijkhuis, Evmorfili Bbairamidou, Ivan Faltus, Felix Rosenberg-Gruszczynski, Martin Westerkamp, Nklomp@sphereon.com, filippo@dyne.org, lld@netsmart.gr, ANDRIANA PRENTZA, Muhamed Turkanović
- Track 3 - Workshop (AMS, 9,10th June)

## Context

Working on the context defined in adr/build-edd-identification-discovery-connection.md and having as the focus the EBW-EDD connection. 

For M2M scenarios, there is a need to be able to identify and address EBWs directly for information exchange.
This could be in cases where an EAA gets re-issued, and a relying party can send a request for sharing of the new EAA, instead of initiating direct customer contact.
It would also make it possible to address attestation to given wallets, reducing the potential for interception in issuance service. (Might become less relevant with Openid4VCI 1.1)


## Decision
Every wallet MUST provide a Credential offer endpoint and a Credential Issuance endpoint to be published in the EDD.
 * This COULD be the same endpoint, as long as both functionalities are supported.
 * The endpoint MUST be unique per wallet, and not require an active browser session.
 * The endpoint COULD be protected behind a secret mechanism. In that case, the secret must be shareable by the Business owner. This secret does not indicate consent to receive/share a credential. Its main purpose is to prevent SPAM attacks against these endpoints from third parties.

## Consequences

* EDD functionality needs to be provided by WP4
* EBW comformance tests need to be adjusted to include the endpoints for the EDD


## Advice

 * Focus should also be made towards classical business documents, i.e., non-EAA (credentials/attributes) 
 * Considering differences in protocols based on EAA or non-EAA, these should be covered in the EAA discovery and connection part 
 
