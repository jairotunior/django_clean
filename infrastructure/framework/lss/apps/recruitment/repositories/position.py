from lss_clean.contexts.recruitment.application.repositories.position import PositionRepository
from lss_clean.contexts.recruitment.domain.entities import Position
from uuid import UUID
from typing import Optional


def build_position(position) -> Position:
    return Position(
        id=position.id,
        uuid=position.uuid,
        name=position.name,
        description=position.description,
        is_active=position.is_active,
    )


class PositionRepositoryDjango(PositionRepository):

    def get(self, position_id: UUID) -> Optional[Position]:
        from apps.recruitment.models import Position as PositionModel
        position = PositionModel.objects.filter(id=position_id).first()
        if not position:
            return None
        return build_position(position)
    
    def save(self, position: Position) -> None:
        from apps.recruitment.models import Position as PositionModel
        PositionModel.objects.create(
            uuid=position.uuid,
            name=position.name,
            description=position.description,
            is_active=position.is_active,
        )
    
    def get_by_id(self, position_id: int) -> Optional[Position]:
        from apps.recruitment.models import Position as PositionModel
        position = PositionModel.objects.filter(id=position_id).first()
        if not position:
            return None
        return build_position(position)