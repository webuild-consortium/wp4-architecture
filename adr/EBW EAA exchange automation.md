# EBW EAA exchange automation

**Authors:**

- Toennis Jonas, Puria Dyne, Rune Kjørlaug, Angel, Ssander Dijkhuis, Evmorfili Bbairamidou, Ivan.faltus@bankid.cz, Felix Rosenberg-Gruszczynski, Martin Westerkamp, Nklomp@sphereon.com, filippo@dyne.org, lld@netsmart.gr, Filip Hladky, ANDRIANA PRENTZA, Muhamed Turkanović
- Track 3 - Workshop (AMS, 9,10th June)

## Context

For M2M scenarios, there is a need to be able to automate attestation exchanges. The general discussion indicated that this would ideally be a different protocol than OpenID4vc, but that this would not be feasible within WeBuild timescope. 
Automation through a automatic approval list or a full policy engine were nominated as the potential solution

## Decision
EBWs MUST support a minimum layer of automation for M2M credential exchanges. 
* A wallet MUST allow a wallet owner to define a combination of recipient and credential types to be shared or received automatically without human approval if requested on the wallet's credential endpoint. 
* A wallet COULD ask after a VC flow if the credential and recipient combination should be added to the automatic approval list.
* All defined rules in the automatic approval list MUST be visible to the wallet owner, and MUST be under the control of the wallet owner. 

## Consequences
* A VP process MUST consult the approval list before answering a VP request or escalating to the user per default OpenID4VCP flow. 
* A VCI process COULD consult the approval list before receiving a credential instead of human approval.
* European Business Wallet providers MUST implement at least a rudimentary automatic approval list for a given Attesation/revciver or issuer combination


## Advice

* A wallet SHOULD allow rules to be defined in a portable, compatible way, so that e-services who request long lived access (e.g. government services) can define these necessary rules for easy import into the business wallet.
