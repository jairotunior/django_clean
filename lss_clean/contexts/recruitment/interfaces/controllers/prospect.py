from dataclasses import dataclass
from lss_clean.contexts.recruitment.application.use_cases.create_prospect import CreateProspectUseCase
from lss_clean.contexts.recruitment.application.dtos.prospect import CreateProspectRequest
from lss_clean.contexts.recruitment.application.dtos.profiling import ProfilingRequest
from lss_clean.contexts.recruitment.application.use_cases.profiling_prospect import ProfilingProspectUseCase
from lss_clean.contexts.recruitment.interfaces.presenters.base import ProspectPresenter
from lss_clean.contexts.recruitment.interfaces.presenters.base import ApplicationPresenter
from lss_clean.contexts.recruitment.interfaces.view_models.base import OperationResult
from lss_clean.contexts.recruitment.domain.exceptions import BusinessRuleViolation, ValidationError


@dataclass
class ProspectController:

    create_prospect_use_case: CreateProspectUseCase
    profiling_prospect_use_case: ProfilingProspectUseCase
    prospect_presenter: ProspectPresenter
    application_presenter: ApplicationPresenter

    def handle_create(self, first_name: str, last_name: str, email: str, phone: str, address: str, city: str, state: str, zip: str, country: str, user_id: int, availability: str) -> OperationResult:
        try:
            request = CreateProspectRequest(first_name, last_name, email, phone, address, city, state, zip, country, user_id, availability)
            result = self.create_prospect_use_case.execute(request)
            if not result.is_success:
                error_vm = self.prospect_presenter.present_error(result.error.message, str(result.error.code.name))
                return OperationResult.failure(error_vm.message, error_vm.code)
            
            view_model = self.prospect_presenter.present_prospect(result.value)
            return OperationResult.success(view_model)
        except ValidationError as e:
            error_vm = self.prospect_presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.failure(error_vm.message, error_vm.code)

    def handle_profiling(self, prospect_id: int, requisition_id: int, position_id: int, availability: str) -> OperationResult:
        try:
            request = ProfilingRequest(prospect_id, requisition_id, position_id, availability)
            result = self.profiling_prospect_use_case.execute(request)
            if not result.is_success:
                error_vm = self.application_presenter.present_error(result.error.message, str(result.error.code.name))
                return OperationResult.failure(error_vm.message, error_vm.code)
            view_model = self.application_presenter.present_application(result.value)
            return OperationResult.success(view_model)
        except BusinessRuleViolation as e:
            error_vm = self.application_presenter.present_error(e.message, str(e.code.name))
            return OperationResult.failure(error_vm.message, error_vm.code)
        except ValidationError as ve:
            error_vm = self.application_presenter.present_error(ve.message, str(ve.code.name))
            return OperationResult.failure(error_vm.message, error_vm.code)
