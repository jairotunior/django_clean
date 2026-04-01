from typing import Protocol
from uuid import UUID
from typing import Optional
from lss_clean.contexts.recruitment.domain.entities import Position


class PositionRepository(Protocol):

    async def get(self, position_id: UUID) -> Optional[Position]: ...
    async def save(self, position: Position) -> None: ...
    async def get_by_id(self, position_id: int) -> Optional[Position]: ...
