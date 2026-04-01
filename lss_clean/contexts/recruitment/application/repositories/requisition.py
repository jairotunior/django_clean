from typing import Protocol
from uuid import UUID
from typing import Optional
from lss_clean.contexts.recruitment.domain.entities import Requisition


class RequisitionRepository(Protocol):

    async def get(self, requisition_id: UUID) -> Optional[Requisition]: ...
    async def save(self, requisition: Requisition) -> None: ...
    async def get_by_id(self, requisition_id: int) -> Optional[Requisition]: ...
