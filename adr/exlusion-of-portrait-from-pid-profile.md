# Exclusion of Portrait from the WE BUILD PID Profile

## Context

Commission Implementing Regulation (EU) 2026/1731 introduces _portrait_ as mandatory person identification data, applicable from 11 August 2028. The regulation specifies requirements for the portrait itself, but does not define the source from which the PID Provider should obtain it.

Including a portrait therefore requires each PID Provider to identify an appropriate authoritative source and establish a process for retrieving and binding the portrait to the PID.

For WE BUILD, implementing such processes across participating countries would require significant effort. The process is not currently standardised and the remaining implementation time within WeBuild is limited.

## Decision

WE BUILD SHALL exclude the portrait attribute from the PID profile implemented and tested within the project.

The WE BUILD PID profile will therefore intentionally deviate from the future mandatory PID dataset defined by Implementing Regulation (EU) 2026/1731 with regard to the portrait attribute.

## Rationale

The purpose of WE BUILD is to implement and test the relevant wallet infrastructure and cross-border use cases within the available project timeframe.

Supporting portrait would require work beyond simply adding an attribute to the PID schema. Each PID Provider would need to establish a trusted source and an appropriate issuance process for the portrait.

Since this process is not standardised and does not contribute sufficiently to the functionality being tested in WE BUILD, the implementation effort is not justified within the project timeframe.

## Consequences

_portrait_ will not be part of the WE BUILD PID profile.

WE BUILD implementations will not demonstrate full compliance with the future PID dataset regarding this attribute.

Portrait support may be added later when national PID issuance processes and authoritative sources are available.

The decision is a WE BUILD scope limitation, not a recommendation to exclude portrait from production EUDI Wallet implementations.

## Advice

Once merged, this is our consortium's decision. This does not mean all participants agree it is the best possible decision. In the decision making process, we have heard the following advice.

2026-10-02 PID/EBWOID Group has agreed that this is the way forward. 
