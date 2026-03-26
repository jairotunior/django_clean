from lss_clean.contexts.recruitment.application.repositories.application import ApplicationRepository
from lss_clean.contexts.recruitment.domain.entities import Application
from apps.recruitment.models import Application as ApplicationModel


class ApplicationRepositoryDjango(ApplicationRepository):

    def save(self, application: Application) -> None:
        ApplicationModel.objects.create(
            uuid=application.uuid,
            prospect_id=application.prospect_id,
            requisition_id=application.requisition.id,
            position_id=application.position.id,
            availability=application.availability,
        )
