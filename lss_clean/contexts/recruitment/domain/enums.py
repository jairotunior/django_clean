from enum import Enum
from typing import List


class ApplicationStatus(Enum):

    CANDIDATE = "candidate"
    FIRST_INTERVIEW = "first_interview"
    APPROVED = "approved"
    TO_HIRE = "to_hire"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    TERMINATED = "terminated"
    ON_HOLD = "on_hold"

    @classmethod
    def terminal_statuses(cls) -> List["ApplicationStatus"]:
        return [cls.REJECTED, cls.WITHDRAWN, cls.TERMINATED]


class CountryCode(Enum):

    COLOMBIA = "CO"
    MEXICO = "MX"
    GUATEMALA = "GT"
    PHILIPPINES = "PH"


class CountryName(Enum):

    COLOMBIA = "Colombia"
    MEXICO = "Mexico"
    GUATEMALA = "Guatemala"
    PHILIPPINES = "Philippines"


class Availability(Enum):

    FULL = "full"
    FULL_BD = "full_bd"
    OVN = "ovn"
    