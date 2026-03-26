from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RejectApplicationCommand:

    application_id: UUID
    reason: str
    notes: str