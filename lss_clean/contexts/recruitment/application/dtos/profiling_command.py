from dataclasses import dataclass
from uuid import UUID
from lss_clean.contexts.recruitment.domain.enums import Availability
from lss_clean.contexts.recruitment.domain.entities.entities import Requisition, Position


@dataclass(frozen=True)
class RequisitionCommand:
    
    id: int
    uuid: UUID


@dataclass(frozen=True)
class PositionCommand:
    
    id: int
    uuid: UUID
    name: str



@dataclass(frozen=True)
class ProfilingCommand:

    prospect_id: int
    requisition: RequisitionCommand
    position: PositionCommand
    availability: Availability