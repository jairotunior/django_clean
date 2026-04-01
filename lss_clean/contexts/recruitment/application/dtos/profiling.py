from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from lss_clean.contexts.recruitment.domain.enums import Availability, ApplicationStatus
from lss_clean.contexts.recruitment.domain.entities.entities import Application
from lss_clean.contexts.recruitment.application.dtos.requisition import RequisitionResponse
from lss_clean.contexts.recruitment.application.dtos.position import PositionResponse
from lss_clean.contexts.recruitment.application.dtos.requisition import RequisitionRequest
from lss_clean.contexts.recruitment.application.dtos.position import PositionRequest



@dataclass(frozen=True)
class ProfilingRequest:

    prospect_id: int
    requisition_id: str
    position_id: str
    availability: str

    def to_execution_params(self) -> dict:
        return {
            'prospect_id': self.prospect_id,
            'requisition_id': self.requisition_id,
            'position_id': self.position_id,
            'availability': self.availability,
        }

        if self.availability:
            params['availability'] = Availability[self.availability]
        return params


@dataclass(frozen=True)
class ProfilingResponse:

    uuid: UUID
    id: int
    status: ApplicationStatus
    created_at: datetime
    requisition: RequisitionResponse
    position: PositionResponse
    availability: Availability

    @classmethod
    def from_entity(cls, application: Application) -> 'ProfilingResponse':
        return cls(
            uuid=application.uuid,
            id=application.id,
            status=application.status,
            created_at=application.created_at,
            requisition=RequisitionResponse.from_entity(application.requisition),
            position=PositionResponse.from_entity(application.position),
            availability=application.availability,
        )