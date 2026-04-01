from lss_clean.contexts.recruitment.application.repositories.application import ApplicationRepository
from lss_clean.contexts.recruitment.application.dtos.reject_application import RejectApplicationRequest, RejectApplicationResponse
from lss_clean.common.results import Result, Error
from lss_clean.contexts.recruitment.domain.exceptions import BusinessRuleViolation, ValidationError


class RejectApplicationUseCase:

    def __init__(self, application_repository: ApplicationRepository):
        self.application_repository = application_repository

    async def execute(self, request: RejectApplicationRequest) -> Result:
        params = request.to_execution_params()
        application = await self.application_repository.get(params.get('application_id'))
        if not application:
            return Result.failure(Error.not_found("Application not found"))
        
        try:
            application.reject(params.get('reason'), params.get('notes'))
            self.application_repository.save(application)
            response = RejectApplicationResponse.from_entity(application)
            return Result.success(response)
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(e.message))
        except ValidationError as e:
            return Result.failure(Error.validation_error(e.message))