from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from lss_clean.contexts.recruitment.domain.entities.entities import Requisition


@dataclass(frozen=True)
class RequisitionRequest:
    
    id: int
    uuid: UUID

    def to_execution_params(self) -> dict:
        params = {
            'id': self.id,
            'uuid': self.uuid,
        }
        return params

   
@dataclass(frozen=True)
class RequisitionResponse:

    uuid: UUID
    id: int
    name: str
    description: str
    created_at: datetime

    @classmethod
    def from_entity(cls, requisition: Requisition) -> 'RequisitionResponse':
        return cls(
            uuid=requisition.uuid,
            id=requisition.id,
            name=requisition.name,
            description=requisition.description,
            created_at=requisition.created_at,
        )