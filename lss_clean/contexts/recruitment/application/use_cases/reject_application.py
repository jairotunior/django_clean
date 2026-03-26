from lss_clean.contexts.recruitment.domain.ports.repositories import ApplicationRepository
from lss_clean.contexts.recruitment.application.dtos.reject_application_command import RejectApplicationCommand
from lss_clean.contexts.recruitment.domain.entities import Application


class RejectApplicationUseCase:

    def __init__(self, application_repository: ApplicationRepository):
        self.application_repository = application_repository

    async def execute(self, command: RejectApplicationCommand) -> Application:
        application = await self.application_repository.get(command.application_id)
        if not application:
            raise ValueError("Application not found")
        
        application.reject(command.reason, command.notes)
        await self.application_repository.save(application)
        return application