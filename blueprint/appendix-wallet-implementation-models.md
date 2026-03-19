## Appendix E. Wallet Implementation and Deployment Considerations in WE BUILD

This appendix provides a short overview of wallet implementation and deployment approaches observed among WE BUILD wallet providers. It does not repeat the architectural classifications defined in the ARF, but highlights aspects that are relevant for the WE BUILD pilots.

Different wallet implementations exist in the ecosystem, reflecting different user groups, device capabilities, and deployment environments. In practice, implementations often combine different approaches depending on the supported use cases.

### Wallet Types Relevant for WE BUILD

From a deployment perspective, wallet implementations in the WE BUILD ecosystem can broadly be grouped into four practical categories.

| Wallet Type | Typical Deployment | Primary Use Cases |
|---|---|---|
| Mobile (on-device) | Smartphone application using device hardware security | Natural person wallets and offline use cases |
| Web / browser-based | Browser interface with backend cryptographic services | Desktop services and enterprise workflows |
| Cloud / HSM-based | Server-hosted wallet infrastructure backed by HSMs | Legal person wallets and managed services |
| Hybrid | Combination of local device security and remote HSM | Mixed use cases requiring both scalability and offline capability |

These categories reflect common deployment patterns observed across wallet implementations. The concrete architecture used by a wallet provider depends on the supported use cases, operational requirements, and device capabilities.

### Deployment Patterns Observed Among WE BUILD Wallet Providers

The WE BUILD Wallet Provider Group conducted a stocktaking questionnaire covering **31 wallet providers** participating in the project. Providers described the deployment models they currently support.

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

#### Mobile and cloud duality

The most common architecture combines:

- a **mobile wallet for natural persons**, and  
- a **server-based wallet for enterprise or legal person scenarios**.

This reflects the broader EUDI ecosystem, where personal identity use cases are mobile-centric while organisational use cases often require backend infrastructure.

#### Increasing use of HSM-backed infrastructure

Several providers indicate the use of remote HSM infrastructure for enterprise wallet deployments. This approach supports large-scale operations and key recovery but requires continuous network connectivity.

#### Limited visibility of WSCD implementation choices

The questionnaire responses mainly describe the application layer (mobile app, server, or web wallet), rather than the underlying cryptographic architecture.

Only a small number of providers explicitly describe the type of secure cryptographic device used (for example secure hardware on the device or remote HSM infrastructure).

#### Emerging architectures for legal person wallets

Architectures supporting legal person wallets are still evolving.  
Many providers indicate that their legal person wallet solutions will be further developed during the WE BUILD project in alignment with emerging European Business Wallet proposals.

As a result, the architectures described in the stocktaking responses should be understood as initial implementation approaches rather than final designs.
