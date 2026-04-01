from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from lss_clean.contexts.recruitment.domain.enums import ApplicationStatus
from lss_clean.contexts.recruitment.domain.entities.entities import Application


@dataclass(frozen=True)
class RejectApplicationResponse:
    
    id: int
    uuid: UUID
    status: ApplicationStatus
    created_at: datetime

    @classmethod
    def from_entity(cls, application: Application) -> 'RejectApplicationResponse':
        return cls(
            id=application.id,
            uuid=application.uuid,
            status=application.status,
            created_at=application.created_at,
        )


@dataclass(frozen=True)
class RejectApplicationRequest:

    application_id: UUID
    reason: str
    notes: str

    def to_execution_params(self) -> dict:
        return {
            'application_id': self.application_id,
            'reason': self.reason,
            'notes': self.notes,
        }