## Appendix E. Wallet Implementation and Deployment Considerations in WE BUILD

This appendix provides a short overview of wallet implementation and deployment approaches observed among WE BUILD wallet providers. It does not repeat the architectural classifications defined in the ARF, but highlights aspects that are relevant for the WE BUILD pilots.

Different wallet implementations exist in the ecosystem, reflecting different user groups, device capabilities, and deployment environments. In practice, implementations often combine different approaches depending on the supported use cases.

### Wallet Types Relevant for WE BUILD

From a deployment perspective, wallet implementations in the WE BUILD ecosystem can broadly be grouped into three practical categories, distinguished by where the wallet runs and where its keys are protected. The same three categories are used in the Wallet Types section of chapter 3.

| Wallet Type | Typical Deployment | Primary Use Cases |
|---|---|---|
| On-device | Wallet Instance on the user's device, keys protected by a WSCD on that device | Natural person wallets and offline use cases |
| Remote / server-side | Wallet service in backend infrastructure, keys protected by a server-side WSCD, typically an HSM | Legal person wallets, managed services and large-scale deployments |
| Hybrid | Combination of a device WSCD and a server-side WSCD | Mixed use cases requiring both scalability and offline capability |

The conformance specifications draw the same line on the cryptographic side: CS-04 describes a device WSCD in which the Wallet Unit generates keys and from which the private key never leaves, while CS-05 describes a cloud- or organisation-controlled HSM acting as a server-side WSCD for business wallets. The security properties of a given deployment are established per wallet unit through the Key Attestation rather than inferred from the wallet type.

The user interface is a separate question. The ARF notes that a Wallet Instance can also be a web application, so a browser-based interface can sit on top of any of the three approaches.

These categories reflect common deployment patterns observed across wallet implementations. The concrete architecture used by a wallet provider depends on the supported use cases, operational requirements, and device capabilities.

### Deployment Patterns Observed Among WE BUILD Wallet Providers

The WE BUILD Wallet Provider Group conducted a stocktaking questionnaire covering **31 wallet providers** participating in the project. Providers described the deployment models they currently support.

The questionnaire was carried out in March 2026. The Wallet Providers Group has grown since then, so the figures below are a snapshot of that point in time rather than current coverage of the group.

The results show a clear split between natural person and enterprise wallet deployments.

| Deployment Option | Share of Providers |
|---|---|
| Mobile wallet (iOS/Android app) | 77% |
| Server wallet on cloud | 55% |
| Server wallet on-premise | 42% |
| Multi-device or white-label wallet | 6% |
| Wallet functionality via API or SDK | 6% |

Many providers support multiple modes, typically combining a mobile wallet for natural persons, and a cloud or server-based wallet for legal persons.

### Architectural Trends in the WE BUILD Ecosystem

The stocktaking exercise highlights several trends relevant for the WE BUILD pilots.

The most common architecture combines a mobile wallet for natural persons with a server-based wallet for enterprise or legal person scenarios. This reflects the broader EUDI ecosystem, where personal identity use cases are mobile-centric while organisational use cases often require backend infrastructure.

Several providers indicate the use of remote HSM infrastructure for enterprise wallet deployments. This approach supports large-scale operations and key recovery but requires continuous network connectivity. Beyond that, the questionnaire gives limited visibility of the cryptographic layer: responses mainly describe the application layer, and only a small number of providers state the type of secure cryptographic device used, whether secure hardware on the device or remote HSM infrastructure.

Architectures supporting legal person wallets are still evolving. Many providers indicate that their legal person wallet solutions will be further developed during the WE BUILD project in alignment with emerging European Business Wallet proposals. As a result, the architectures described in the stocktaking responses should be understood as initial implementation approaches rather than final designs.
