from typing import Protocol

from lss_clean.contexts.recruitment.domain.entities import Prospect


class ProspectServicePort(Protocol):

    def reserve_items(self, prospect: Prospect) -> None:
        pass