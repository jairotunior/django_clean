from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from lss_clean.contexts.recruitment.domain.entities.entities import Position


@dataclass(frozen=True)
class PositionRequest:
    
    id: int
    uuid: UUID
    name: str


@dataclass(frozen=True)
class PositionResponse:

    uuid: str
    id: int
    name: str
    description: str

    @classmethod
    def from_entity(cls, position: Position) -> 'PositionResponse':
        return cls(
            uuid=str(position.uuid),
            id=position.id,
            name=position.name,
            description=position.description,
        )