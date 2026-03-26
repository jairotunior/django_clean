from lss_clean.contexts.recruitment.domain.enums import ApplicationStatus, Availability

APPLICATION_STATUS_CHOICES = [
    (member.value, member.name.replace("_", " ").title()) for member in ApplicationStatus
]
AVAILABILITY_CHOICES = [
    (member.value, member.name.replace("_", " ").title()) for member in Availability
]