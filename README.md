# Clean Architecture (contexts only)

This project uses DDD bounded contexts under `lss_clean/contexts/`, and it applies the Clean Architecture idea inside each context:

- `domain`: the business rules (things that must stay true regardless of UI, database, or transport)
- `application`: the use cases that orchestrate the business rules
- explicit boundaries via “ports” (interfaces/`Protocol`s) so application code does not depend on infrastructure details

## `recruitment/` bounded context

`lss_clean/contexts/recruitment/` is the only context currently present.

### `domain/` (Entities and Rules)

In Clean Architecture terms, everything in `domain/` is the core. It should:

- model the business (entities/aggregates and their invariants)
- express domain language (enums like `ApplicationStatus`, value concepts like `Availability`, etc.)
- own domain behavior (methods like `Prospect.create(...)`, `Prospect.profile(...)`, `Application.reject(...)`)
- describe domain outcomes as facts (domain events) and domain errors (exceptions)

Concretely in your code:

- `domain/entities/`
  - `entity.py`: base `Entity` with identity semantics (`id`)
  - `entities.py`: `Prospect`, `Application`, and related domain objects (`Position`, `Requisition`, etc.)
  - domain behavior example:
    - `Prospect.profile(...)`: checks rules (`can_be_profiled`), creates an `Application`, and records a `ProspectProfiledEvent`
    - `Application.reject(...)`: validates state (`can_be_rejected`), updates status, and records an `ApplicationRejectedEvent`
- `domain/enums.py`: domain enums (status, availability, country)
- `domain/events.py`: domain event dataclasses
- `domain/exceptions.py`: domain error hierarchy (`DomainError`, etc.)
- `domain/services/`: reserved for domain-level services; currently empty

Key rule of thumb: `domain` must not import `application` (or anything that depends on outside concerns).

### `application/` (Use Cases and Orchestration)

In Clean Architecture terms, `application/` holds what the system does in response to requests. It typically:

- accepts inputs via command DTOs (`dtos/`)
- loads and persists aggregates through abstractions (repository `Protocol`s)
- invokes domain methods to enforce business invariants
- returns domain results back to the caller

Concretely:

- `application/dtos/`: immutable command inputs
  - `prospect_command.py` -> `CreateProspectCommand`
  - `profiling_command.py` -> `ProfilingCommand`
  - `reject_application_command.py` -> `RejectApplicationCommand`
- `application/use_cases/`: use cases with `async execute(command)`
  - `create_prospect.py`: builds a `Prospect` using domain logic, then saves through a repository port
  - `profiling_prospect.py`: loads a `Prospect`, calls `prospect.profile(...)` (domain rule), then saves the resulting `Application`
  - `reject_application.py`: loads an `Application`, calls `application.reject(...)`, then saves it
- `application/repositories/`: repository ports (persistence abstractions as `Protocol`s)
  - `prospect.py`: `ProspectRepository` (`save`, `get`)
  - `application.py`: `ApplicationRepository` (`save`, `get`)
- `application/services/`: optional service ports; currently contains `ProspectServicePort`

Key rule of thumb: `application` depends on `domain`, but it should depend on infrastructure only through ports (`Protocol`s). This keeps business logic testable.

### Dependency Direction (conceptual)

Conceptually the dependency flow inside `recruitment/` should be:

`Use Case (application) -> Ports (Protocol interfaces) -> Infrastructure (not in this README)`,

and separately:

`Use Case (application) -> Domain (entities/events/enums)`,

with `domain` remaining independent.

### Small note about “ports” location

Your repository ports (`ProspectRepository`, `ApplicationRepository`) currently live under `application/repositories/`.

But `reject_application.py` imports them from `lss_clean.contexts.recruitment.domain.ports` (which is empty right now). Conceptually, you probably want those imports to point to where the repository ports actually live, so the dependency direction stays consistent.