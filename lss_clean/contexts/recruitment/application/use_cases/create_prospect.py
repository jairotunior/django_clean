from lss_clean.contexts.recruitment.domain.entities import Prospect
from lss_clean.contexts.recruitment.application.repositories.prospect import ProspectRepository
from lss_clean.contexts.recruitment.application.dtos.prospect import (
    CreateProspectRequest,
    CreateProspectResponse,
)
from lss_clean.contexts.recruitment.domain.exceptions import ValidationError
from lss_clean.common.results import Result, Error


class CreateProspectUseCase:

    def __init__(self, prospect_repository: ProspectRepository):
        self.prospect_repository = prospect_repository

    def execute(self, request: CreateProspectRequest) -> Result:
        params = request.to_execution_params()
        prospect = self.prospect_repository.get_by_email(params.get('email'))
        if prospect:
            return Result.failure(Error.business_rule_violation("Prospect with this email already exists"))

        try:
            prospect = Prospect.create(**params)
            prospect = self.prospect_repository.save(prospect)
            response = CreateProspectResponse.from_entity(prospect)
            return Result.success(response)
        except ValidationError as e:
            return Result.failure(Error.validation_error(e))
