from dataclasses import dataclass
from lss_clean.contexts.recruitment.application.repositories.prospect import ProspectRepository
from lss_clean.contexts.recruitment.application.repositories.application import ApplicationRepository
from lss_clean.contexts.recruitment.application.repositories.requisition import RequisitionRepository
from lss_clean.contexts.recruitment.application.repositories.position import PositionRepository
from lss_clean.contexts.recruitment.interfaces.presenters.base import ProspectPresenter
from lss_clean.contexts.recruitment.interfaces.presenters.base import ApplicationPresenter
from lss_clean.contexts.recruitment.application.use_cases.create_prospect import CreateProspectUseCase
from lss_clean.contexts.recruitment.application.use_cases.profiling_prospect import ProfilingProspectUseCase
from lss_clean.contexts.recruitment.application.use_cases.reject_application import RejectApplicationUseCase
from lss_clean.contexts.recruitment.interfaces.controllers.prospect import ProspectController
from lss_clean.contexts.recruitment.interfaces.controllers.application import ApplicationController
from infrastructure.repository_factory import create_repository



@dataclass
class Application:

    prospect_repository: ProspectRepository
    application_repository: ApplicationRepository
    requisition_repository: RequisitionRepository
    position_repository: PositionRepository
    prospect_presenter: ProspectPresenter
    application_presenter: ApplicationPresenter

    def __post_init__(self):

        self.create_prospect_use_case = CreateProspectUseCase(
            prospect_repository=self.prospect_repository,
        )
        self.profiling_prospect_use_case = ProfilingProspectUseCase(
            prospect_repository=self.prospect_repository,
            application_repository=self.application_repository,
            requisition_repository=self.requisition_repository,
            position_repository=self.position_repository,
        )
        self.reject_application_use_case = RejectApplicationUseCase(
            application_repository=self.application_repository,
        )

        # Wire up the controllers
        self.prospect_controller = ProspectController(
            create_prospect_use_case=self.create_prospect_use_case,
            profiling_prospect_use_case=self.profiling_prospect_use_case,
            prospect_presenter=self.prospect_presenter,
            application_presenter=self.application_presenter,
        )

        self.application_controller = ApplicationController(
            reject_application_use_case=self.reject_application_use_case,
            application_presenter=self.application_presenter,
        )


def create_application(prospect_presenter: ProspectPresenter, application_presenter: ApplicationPresenter) -> Application:
    prospect_repository, application_repository, requisition_repository, position_repository = create_repository()

    return Application(
        prospect_repository=prospect_repository,
        application_repository=application_repository,
        requisition_repository=requisition_repository,
        position_repository=position_repository,
        prospect_presenter=prospect_presenter,
        application_presenter=application_presenter,
    )