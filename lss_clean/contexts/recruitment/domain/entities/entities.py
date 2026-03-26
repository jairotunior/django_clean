from __future__ import annotations

from uuid import UUID, uuid4
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, List

from lss_clean.contexts.recruitment.domain.enums import ApplicationStatus, Availability, CountryName
from lss_clean.contexts.recruitment.domain.events import (
    ApplicationRejectedEvent,
    ProspectProfiledEvent,
)

from lss_clean.contexts.recruitment.domain.entities.entity import Entity
from lss_clean.contexts.recruitment.domain.exceptions import BusinessRuleViolation


@dataclass
class Position:

    name: str
    description: str
    is_active: bool
    id: int = field(default=None, init=True)
    uuid: UUID = field(default_factory=uuid4, init=True)


@dataclass
class Requisition:
    
    name: str
    description: str
    created_at: datetime
    id: int = field(default=None, init=True)
    uuid: UUID = field(default_factory=uuid4, init=True)
    is_active: bool = field(default=True)
    details: List[RequisitionDetail] = field(default_factory=list)


@dataclass
class RequisitionDetail:
    
    position: Position
    is_active: bool


@dataclass
class Prospect:
    
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    id: int = field(default=None, init=True)
    uuid: UUID = field(default_factory=uuid4, init=True)
    country: Optional[CountryName] = field(default=None)
    state: Optional[str] = None
    zip: Optional[str] = None
    user_id: int = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    availability: Optional[Availability] = None
    current_application: Optional[Application] = None
    applications: List[Application] = field(default_factory=list)
    _events: list = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        if self.availability not in Availability:
            raise ValueError(f"Invalid availability: {self.availability}")
        if self.country not in CountryName:
            raise ValueError(f"Invalid country: {self.country}")
        if self.user_id is None:
            raise ValueError("User ID is required")
        if self.uuid is None:
            self.uuid = uuid4()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def has_current_application(self) -> bool:
        return self.current_application is not None

    @property
    def can_be_profiled(self) -> bool:
        return not self.current_application or self.current_application.status == ApplicationStatus.CANDIDATE
    
    @property
    def can_be_reapplied(self) -> bool:
        return (
            self.current_application and
            self.current_application.status in ApplicationStatus.terminal_statuses() and
            self.current_application.created_at < datetime.now() - timedelta(days=90)
        )

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        state: str,
        zip: str,
        country: CountryName,
        user_id: int,
        availability: Availability,
    ) -> Prospect:
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip=zip,
            country=country,
            user_id=user_id,
            availability=availability,
        )

    def profile(self, requisition: Requisition, position: Position, availability: Availability) -> None:
        if not self.can_be_profiled:
            raise BusinessRuleViolation("Prospect cannot be profiled. It already has a current application.")
        
        self.current_application = Application(
            prospect_id=self.id,
            requisition=requisition,
            position=position,
            availability=availability,
        )

        self.current_application._events.append(
            ProspectProfiledEvent(
                prospect_id=self.id,
                status=self.current_application.status,
                requisition_id=requisition.id,
                position_id=position.id,
                availability=availability,
                profiled_at=self.current_application.created_at,
            )
        )
        return self.current_application


@dataclass
class Application:
    
    prospect_id: int = field(default=None, init=True)
    id: int = field(default=None, init=True)
    uuid: UUID = field(default_factory=uuid4, init=True)
    status: Optional[ApplicationStatus] = ApplicationStatus.CANDIDATE
    created_at: datetime = field(default_factory=datetime.now)
    requisition: Optional[Requisition] = None
    position: Optional[Position] = None
    availability: Optional[Availability] = None

    _events: list = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        if self.uuid is None:
            self.uuid = uuid4()

    def can_be_rejected(self) -> bool:
        return self.status not in ApplicationStatus.terminal_statuses()

    def reject(self, reason: str, notes: str) -> None:
        if not self.can_be_rejected():
            raise BusinessRuleViolation("Application cannot be rejected")

        self.status = ApplicationStatus.REJECTED
        self._events.append(
            ApplicationRejectedEvent(
                self.id, datetime.now(), reason, notes
            )
        )
