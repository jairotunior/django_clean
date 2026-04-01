from dataclasses import dataclass


@dataclass(frozen=True)
class ApplicationViewModel:

    id: int
    uuid: str
    status: str
    created_at: str
    requisition: int
    position: int
    availability: str