EBWOID Identifiers

Authors:
Ronald König, Spherity, Germany (Spherity co-lead of scenarios in BU1)
Miriam Weber, Procivis, Austria (Procivis co-lead of a scenario in PA3)

Context:

In some business cases, the verifier (relying party) requires verifiable data on both the legal person and the natural person acting on its behalf. 
For example, in order to open a corporate account, the bank requires comprehensive KYC data about both the legal person (company) and the natural person (legal representative) applying for the account on behalf of the company. 
Furthermore, the bank requires proof that the natural person is authorised to act on behalf of the company.
 
In general, there are two ways in which the verifier can collect the data:
1. The verifier can request the natural person data from the EUDI-wallet of the legal representative and the KYC data from the European business wallet of the company.
2. This approach has various implications:
2.1 In particular, the verifying bank would need to perform attribute matching across wallets to ensure that the identities represented in credentials issued to different wallets refer to the same individual. 
2.2 A combined proof across wallets  — asking different attributes of attestations held (e.g PID & EUCC) —  is not possible.
2.3 Employees of a company would be required to have and use their individual EUDI wallet to complete the flow.
on an upside: based on the discussion in PA3, companies & Banks' trust in a PID is high.

4. The EU business holds the company's identity (e.g. EUCC) as well as the identities of all individuals who need to act on its behalf.
The identities of natural persons are derived from the PID and issued in the EBW. This approach has the following advantages
3.1 The identities of natural persons can be cryptographically bound to the company's identity.
3.2 There is strict separation between the private and business identities of the natural person.
However:
3.3 However there may be implications in light of existing and upcoming regulations (e.g. to be verified if derived identities are allowed in context of AML, what are requirements in an upcoming EUBW regulation, etc…)
