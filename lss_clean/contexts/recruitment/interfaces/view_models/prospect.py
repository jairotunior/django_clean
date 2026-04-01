from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class ProspectViewModel:

    id: int
    uuid: str
    user_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    country: str
    availability: str
    created_at: str