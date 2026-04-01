from dataclasses import dataclass
from lss_clean.contexts.recruitment.application.use_cases.reject_application import RejectApplicationUseCase
from lss_clean.contexts.recruitment.application.dtos.reject_application import RejectApplicationRequest
from lss_clean.contexts.recruitment.interfaces.presenters.base import ApplicationPresenter
from lss_clean.contexts.recruitment.interfaces.view_models.base import OperationResult
from lss_clean.contexts.recruitment.domain.exceptions import ValidationError


@dataclass
class ApplicationController:

    reject_application_use_case: RejectApplicationUseCase
    application_presenter: ApplicationPresenter

    def handle_reject(self, prospect_id: int, requisition_id: int, position_id: int, availability: str) -> OperationResult:
        try:
            request = RejectApplicationRequest(prospect_id, requisition_id, position_id, availability)
            result = self.create_application_use_case.execute(request)
            if not result.is_success:
                error_vm = self.application_presenter.present_error(result.error.message, str(result.error.code.name))
                return OperationResult.failure(error_vm.message, error_vm.code)

            view_model = self.application_presenter.present_application(result.value)
            return OperationResult.success(view_model)
        except ValidationError as e:
            error_vm = self.application_presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.failure(error_vm.message, error_vm.code)