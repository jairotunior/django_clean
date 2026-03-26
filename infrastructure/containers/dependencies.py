from sqlalchemy.orm import AsyncSession

from lss_clean.contexts.recruitment.application.use_cases.create_prospect import CreateProspectUseCase
from infrastructure.framework.lss.apps.recruitment.repositories.prospect import ProspectRepositoryDjango


def get_create_prospect_use_case() -> CreateProspectUseCase:
    prospect_repository = ProspectRepositoryDjango()
    return CreateProspectUseCase(
        prospect_repository=prospect_repository,
    )