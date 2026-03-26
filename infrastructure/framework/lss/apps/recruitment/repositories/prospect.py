from uuid import UUID
from typing import Optional
from lss_clean.contexts.recruitment.application.repositories.prospect import ProspectRepository
from lss_clean.contexts.recruitment.domain.entities import Prospect, Application, Requisition, Position, RequisitionDetail
from apps.recruitment.models import Prospect as ProspectModel
from lss_clean.contexts.recruitment.domain.exceptions import NotFoundError, BusinessRuleViolation
from django.core.exceptions import MultipleObjectsReturned


def build_prospect(prospect: ProspectModel) -> Prospect:
    current_application = prospect.applications.last()
    return Prospect(
        uuid=prospect.uuid,
        id=prospect.id,
        user_id=prospect.user.id,
        first_name=prospect.first_name,
        last_name=prospect.last_name,
        email=prospect.email,
        phone=prospect.phone,
        address=prospect.address,
        city=prospect.city,
        state=prospect.state,
        zip=prospect.zip,
        country=prospect.country,
        availability=prospect.availability,
        created_at=prospect.created_at,
        current_application=Application(
            id=current_application.id,
            uuid=current_application.uuid,
            status=current_application.status,
            created_at=current_application.created_at,
            requisition=Requisition(
                id=current_application.requisition.id,
                uuid=current_application.requisition.uuid,
                name=current_application.requisition.name,
                description=current_application.requisition.description,
                created_at=current_application.requisition.created_at,
                is_active=current_application.requisition.is_active,
                details=[
                    RequisitionDetail(
                        id=detail.id,
                        uuid=detail.uuid,
                        position=Position(
                            id=detail.position.id,
                            uuid=detail.position.uuid,
                            name=detail.position.name,
                            description=detail.position.description,
                            is_active=detail.position.is_active,
                        ),
                        is_active=detail.is_active,
                    ) for detail in current_application.requisition.details.all()
                ],
            ),
            position=Position(
                id=current_application.position.id,
                uuid=current_application.position.uuid,
                name=current_application.position.name,
                description=current_application.position.description,
                is_active=current_application.position.is_active,
            ),
            availability=current_application.availability,
        ) if current_application else None,
    )


class ProspectRepositoryDjango(ProspectRepository):

    def save(self, prospect: Prospect) -> None:
        ProspectModel.objects.create(
            uuid=prospect.uuid,
            user_id=prospect.user_id,
            first_name=prospect.first_name,
            last_name=prospect.last_name,
            email=prospect.email,
            phone=prospect.phone,
            address=prospect.address,
            city=prospect.city,
            state=prospect.state,
            zip=prospect.zip,
            country=prospect.country,
            availability=prospect.availability,
            current_application=prospect.current_application,
        )

    def base_get(self, **kwargs) -> Optional[ProspectModel]:
        return ProspectModel.objects.select_related(
            'user'
        ).prefetch_related(
            'applications',
            'applications__requisition',
            'applications__position',
            'applications__requisition__details',
        ).get(**kwargs)

    def get(self, prospect_id: int) -> Optional[Prospect]:
        try:
            prospect = self.base_get(id=prospect_id)
        except ProspectModel.DoesNotExist:
            raise NotFoundError(f"Prospect with id {prospect_id} does not exist")
        except MultipleObjectsReturned:
            raise BusinessRuleViolation("Multiple prospects found with the same id")

        return build_prospect(prospect)

    def get_by_email(self, email: str) -> Optional[Prospect]:
        prospect = ProspectModel.objects.filter(email=email).first()
        if not prospect:
            return None
        return build_prospect(prospect)