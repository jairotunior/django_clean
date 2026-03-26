from typing import Protocol
from uuid import UUID
from typing import Optional
from lss_clean.contexts.recruitment.domain.entities import Application


class ApplicationRepository(Protocol):

    async def save(self, application: Application) -> None: ...
    async def get(self, application_id: UUID) -> Optional[Application]: ...