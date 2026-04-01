from lss_clean.contexts.recruitment.application.repositories.requisition import RequisitionRepository
from lss_clean.contexts.recruitment.domain.entities import Requisition
from uuid import UUID
from typing import Optional


def build_requisition(requisition) -> Requisition:
    return Requisition(
        uuid=requisition.uuid,
        id=requisition.id,
        name=requisition.name,
        description=requisition.description,
        created_at=requisition.created_at,
        is_active=requisition.is_active,
    )


class RequisitionRepositoryDjango(RequisitionRepository):

    def get(self, requisition_id: UUID) -> Optional[Requisition]:
        from apps.recruitment.models import Requisition as RequisitionModel
        requisition = RequisitionModel.objects.filter(id=requisition_id).first()
        if not requisition:
            return None
        return build_requisition(requisition)
    
    def save(self, requisition: Requisition) -> None:
        from apps.recruitment.models import Requisition as RequisitionModel
        RequisitionModel.objects.create(
            uuid=requisition.uuid,
            name=requisition.name,
            description=requisition.description,
            is_active=requisition.is_active,
        )
    
    def get_by_id(self, requisition_id: int) -> Optional[Requisition]:
        from apps.recruitment.models import Requisition as RequisitionModel
        requisition = RequisitionModel.objects.filter(id=requisition_id).first()
        if not requisition:
            return None
        return build_requisition(requisition)
