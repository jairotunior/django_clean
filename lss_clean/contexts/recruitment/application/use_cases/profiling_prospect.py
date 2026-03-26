from lss_clean.contexts.recruitment.application.repositories.prospect import ProspectRepository
from lss_clean.contexts.recruitment.application.repositories.application import ApplicationRepository
from lss_clean.contexts.recruitment.application.dtos.profiling_command import ProfilingCommand
from lss_clean.contexts.recruitment.domain.entities.entities import Application
from lss_clean.contexts.recruitment.domain.exceptions import NotFoundError


class ProfilingProspectUseCase:

    def __init__(
        self, 
        prospect_repository: ProspectRepository,
        application_repository: ApplicationRepository
    ):
        self.prospect_repository = prospect_repository
        self.application_repository = application_repository

    def execute(self, command: ProfilingCommand) -> Application:
        prospect = self.prospect_repository.get(command.prospect_id)
        if not prospect:
            raise NotFoundError("Prospect not found")

        application = prospect.profile(
            requisition=command.requisition,
            position=command.position,
            availability=command.availability,
        )
        self.application_repository.save(application)

        return application