from lss_clean.contexts.recruitment.application.repositories.prospect import ProspectRepository
from lss_clean.contexts.recruitment.application.repositories.application import ApplicationRepository
from lss_clean.contexts.recruitment.application.dtos.profiling import ProfilingRequest, ProfilingResponse
from lss_clean.contexts.recruitment.application.repositories.requisition import RequisitionRepository
from lss_clean.contexts.recruitment.application.repositories.position import PositionRepository
from lss_clean.common.results import Result, Error
from lss_clean.contexts.recruitment.domain.exceptions import BusinessRuleViolation, ValidationError


class ProfilingProspectUseCase:

    def __init__(
        self, 
        prospect_repository: ProspectRepository,
        application_repository: ApplicationRepository,
        requisition_repository: RequisitionRepository,
        position_repository: PositionRepository,
    ):
        self.prospect_repository = prospect_repository
        self.application_repository = application_repository
        self.requisition_repository = requisition_repository
        self.position_repository = position_repository

    def execute(self, request: ProfilingRequest) -> Result:
        params = request.to_execution_params()
        prospect = self.prospect_repository.get(params.get('prospect_id'))
        if not prospect:
            return Result.failure(Error.not_found("Prospect not found"))

        requisition = self.requisition_repository.get(params.get('requisition_id'))
        if not requisition:
            return Result.failure(Error.not_found("Requisition not found"))

        position = self.position_repository.get(params.get('position_id'))
        if not position:
            return Result.failure(Error.not_found("Position not found"))

        try:    
            application = prospect.profile(
                requisition=requisition,
                position=position,
                availability=params.get('availability'),
            )
            application = self.application_repository.save(application)
            response = ProfilingResponse.from_entity(application)
            return Result.success(response)
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(e))
        except ValidationError as e:
            return Result.failure(Error.validation_error(e))