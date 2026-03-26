from dataclasses import dataclass
from uuid import UUID
from lss_clean.contexts.recruitment.domain.enums import CountryName, Availability, ApplicationStatus


@dataclass(frozen=True)
class CreateProspectCommand:

    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    country: CountryName
    user_id: int
    availability: Availability
