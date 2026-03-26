from typing import Optional, Protocol
from uuid import UUID

from lss_clean.contexts.recruitment.domain.entities import Prospect, Application


class ProspectRepository(Protocol):

    async def save(self, prospect: Prospect) -> None: ...
    async def get(self, prospect_id: UUID) -> Optional[Prospect]: ...
    async def get_by_email(self, email: str) -> Optional[Prospect]: ...