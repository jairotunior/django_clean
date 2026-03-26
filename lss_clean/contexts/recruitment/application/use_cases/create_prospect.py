from lss_clean.contexts.recruitment.domain.entities import Prospect
from lss_clean.contexts.recruitment.application.repositories.prospect import ProspectRepository
from lss_clean.contexts.recruitment.application.repositories.application import ApplicationRepository
from lss_clean.contexts.recruitment.application.dtos.prospect_command import (
    CreateProspectCommand,
)
from lss_clean.contexts.recruitment.domain.exceptions import BusinessRuleViolation


class CreateProspectUseCase:

    def __init__(self, prospect_repository: ProspectRepository):
        self.prospect_repository = prospect_repository

    def execute(self, command: CreateProspectCommand) -> Prospect:
        prospect = self.prospect_repository.get_by_email(command.email)
        if prospect:
            raise BusinessRuleViolation("Prospect with this email already exists")

        prospect = Prospect.create(
            command.first_name, 
            command.last_name, 
            command.email, 
            command.phone, 
            command.address, 
            command.city, 
            command.state, 
            command.zip, 
            command.country,
            command.user_id,
            command.availability
        )

        self.prospect_repository.save(prospect)
        return prospect
