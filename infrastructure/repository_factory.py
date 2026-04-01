from infrastructure.framework.lss.apps.recruitment.repositories.prospect import ProspectRepositoryDjango
from infrastructure.framework.lss.apps.recruitment.repositories.application import ApplicationRepositoryDjango
from infrastructure.framework.lss.apps.recruitment.repositories.requisition import RequisitionRepositoryDjango
from infrastructure.framework.lss.apps.recruitment.repositories.position import PositionRepositoryDjango


def create_repository():

    prospect_repository = ProspectRepositoryDjango()
    application_repository = ApplicationRepositoryDjango()
    requisition_repository = RequisitionRepositoryDjango()
    position_repository = PositionRepositoryDjango()


    return prospect_repository, application_repository, requisition_repository, position_repository