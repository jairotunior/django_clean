from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Entity:

    id: int
    uuid: UUID

    def __post_init__(self) -> None:
        if self.uuid is None:
            self.uuid = uuid4()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.uuid == other.uuid

    def __hash__(self) -> int:
        return hash(self.uuid)