# Replace LPID with EBWOID

**Authors:**
- Erwin Nieuwlaar, KVK, Netherlands

## Context:
In webuild-consortium/eudi-wallet-rulebooks-and-schemas#24, the LPID (Legal Person Identification Data) rulebook was removed in favour of the EBWOID (European Business Wallet Owner Identification Data) rulebook. It was unclear whether this represented a consortium decision. Hence, an ADR to discuss support/objections and document this decision is clearly.
The PID/EBWOID working group agreed to proceed with this change during a weekly discussion session.

## Decision
WE BUILD will use the EBWOID rulebook as the basis for identification of business wallet owners and deprecate LPID within WE BUILD:
- No new WE BUILD specifications should reference LPID
- Existing WE BUILD references to LPID should be migrated to EBWOID

## Consequences
Positive: 
- One clear rulebook for implementers
- Reduced duplication

Negative/Risks: 
- Migration effort from LPID to EBWOID
- EBWOID originates from the Business Wallet proposal, which is not yet in force. There will be an interim period in which eIDAS 2.0 is applicable while the Business Wallet framework is not, creating a risk of misalignment in identifying legal persons

## Advice
