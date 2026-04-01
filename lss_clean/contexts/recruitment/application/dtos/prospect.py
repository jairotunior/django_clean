from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID
from lss_clean.contexts.recruitment.domain.enums import CountryName, Availability, ApplicationStatus
from lss_clean.contexts.recruitment.domain.entities import Prospect


@dataclass(frozen=True)
class CreateProspectRequest:

    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    country: str
    user_id: int
    availability: str

    def to_execution_params(self) -> dict:
        params = {
            'first_name': self.first_name.strip(),
            'last_name': self.last_name.strip(),
            'email': self.email.strip(),
            'phone': self.phone.strip(),
            'address': self.address.strip(),
            'city': self.city.strip(),
            'state': self.state.strip(),
            'zip': self.zip,
            'user_id': self.user_id,
        }

        if self.availability:
            params['availability'] = Availability[self.availability.upper()]
        
        if self.country:
            params['country'] = CountryName[self.country.upper()]
        
        return params


@dataclass(frozen=True)
class CreateProspectResponse:

    user_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    country: CountryName
    availability: Availability
    created_at: datetime
    uuid: Optional[UUID] = None
    id: Optional[int] = None

    @classmethod
    def from_entity(cls, prospect: Prospect) -> 'CreateProspectResponse':
        return cls(
            uuid=prospect.uuid,
            id=prospect.id,
            user_id=prospect.user_id,
            first_name=prospect.first_name,
            last_name=prospect.last_name,
            email=prospect.email,
            phone=prospect.phone,
            address=prospect.address,
            city=prospect.city,
            state=prospect.state,
            zip=prospect.zip,
            country=prospect.country,
            availability=prospect.availability,
            created_at=prospect.created_at,
        )