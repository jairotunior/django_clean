from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from lss_clean.contexts.recruitment.domain.enums import ApplicationStatus, Availability


@dataclass
class ApplicationRejectedEvent:

    application_id: UUID
    rejected_at: datetime
    reason: str
    notes: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProspectProfiledEvent:

    prospect_id: UUID
    status: ApplicationStatus
    requisition_id: UUID
    position_id: UUID
    availability: Availability
    profiled_at: datetime
    occurred_at: datetime = field(default_factory=datetime.now)
