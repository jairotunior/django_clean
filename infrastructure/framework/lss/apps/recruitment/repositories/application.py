from lss_clean.contexts.recruitment.application.repositories.application import ApplicationRepository
from lss_clean.contexts.recruitment.domain.entities import Application, Requisition, Position


def build_application(application) -> Application:
    return Application(
        id=application.id,
        uuid=application.uuid,
        prospect_id=application.prospect_id,
        requisition=Requisition(
            id=application.requisition.id,
            uuid=application.requisition.uuid,
            name=application.requisition.name,
            description=application.requisition.description,
            created_at=application.requisition.created_at,
            is_active=application.requisition.is_active,
        ),
        position=Position(
            id=application.position.id,
            uuid=application.position.uuid,
            name=application.position.name,
            description=application.position.description,
            is_active=application.position.is_active,
        ),
        availability=application.availability,
        created_at=application.created_at,
        status=application.status,
    )


class ApplicationRepositoryDjango(ApplicationRepository):

    def save(self, application: Application) -> Application:
        from apps.recruitment.models import Application as ApplicationModel
        application_model = ApplicationModel.objects.create(
            uuid=application.uuid,
            prospect_id=application.prospect_id,
            requisition_id=application.requisition.id,
            position_id=application.position.id,
            availability=application.availability,
            status=application.status.value,
            created_at=application.created_at,
        )
        return build_application(application_model)
