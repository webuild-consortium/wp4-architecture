# Support Role-Based and Service-Based Authorization Models

**Authors:**

- Consortium Architecture Working Group AMS Track 4

- Boris Lingl, boris.lingl@datev.de
- Alexander Manecke, a.manecke@telekom.de
- Ignacio Ripoll, ignacio.ripoll@corpme.es
- Iris Speiser, iris.speiser@datev.de
- Marlene Urbschat, marlene.urbschat@datev.de

## Context

There is a structural mismatch between:

- how businesses grant powers (typically role-based), and
- how service providers authorize access to their services (typically service-based).

Mandating only one authorization model would exclude important use cases and stakeholders.

The core trade-off is between simplicity (a single model) and flexibility/interoperability (supporting both models).

## Decision

The consortium will support both of the following authorization models:

- **Role-Based Authorization**
- **Service-Based Authorization**

Service providers may choose the model they support based on their risk assessment and authorization requirements.

In addition, BU3 will create and maintain a **service register/list** to enable the discovery and mapping of service-based authorizations.

## Consequences

### What becomes easier?

- Better alignment with established business practices.
- Greater flexibility for service providers.
- Improved adoption across different sectors.
- Support for a broader range of authorization scenarios.

### What becomes more difficult?

- Mapping between role-based and service-based permissions.
- Ensuring consistent interpretation of authorization scopes.
- Discovery and governance of service definitions.

### How do we address the risks introduced by this change?

- Create and maintain a consortium-wide service register/list.
- Define governance rules for service registration and discovery.
- Allow service providers to perform their own risk assessment regarding acceptance of role-based powers.
- Continuously refine mappings between roles, faculties, and services.

## Advice

- 2026-06-11: Consortium Working Group: Support both models to maximize interoperability and adoption.
- 2026-06-11: Service Providers: Acceptance of role-based powers should depend on whether the associated faculties are sufficient and on the provider's risk assessment.
- 2026-06-11: BU3: A service register and discovery mechanism are required for operational deployment.
