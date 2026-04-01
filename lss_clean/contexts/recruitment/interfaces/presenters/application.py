from lss_clean.contexts.recruitment.interfaces.presenters.base import ApplicationPresenter
from lss_clean.contexts.recruitment.application.dtos.profiling import ProfilingResponse
from lss_clean.contexts.recruitment.interfaces.view_models.application import ApplicationViewModel
from lss_clean.contexts.recruitment.interfaces.view_models.base import ErrorViewModel


class WebApplicationPresenter(ApplicationPresenter):

    def present_application(self, response: ProfilingResponse) -> ApplicationViewModel:
        return ApplicationViewModel(
            id=response.id,
            uuid=response.uuid,
            status=response.status,
            created_at=response.created_at,
            requisition=response.requisition.id,
            position=response.position.id,
            availability=response.availability,
        )
    
    def present_error(self, message: str, code: str) -> ErrorViewModel:
        return ErrorViewModel(message=message, code=code)


class CliApplicationPresenter(ApplicationPresenter):

    def present_application(self, response: ProfilingResponse) -> ApplicationViewModel:
        return ApplicationViewModel(
            id=response.id,
            uuid=response.uuid,
            status=response.status,
            created_at=response.created_at,
        )
    
    def present_error(self, message: str, code: str) -> ErrorViewModel:
        return ErrorViewModel(message=message, code=code)