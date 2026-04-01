from dataclasses import dataclass
from typing import Optional
from lss_clean.contexts.recruitment.interfaces.presenters.base import ProspectPresenter
from lss_clean.contexts.recruitment.application.dtos.prospect import CreateProspectResponse
from lss_clean.contexts.recruitment.interfaces.view_models.prospect import ProspectViewModel
from lss_clean.contexts.recruitment.interfaces.view_models.base import ErrorViewModel


class WebProspectViewPresenter(ProspectPresenter):

    def present_prospect(self, response: CreateProspectResponse) -> ProspectViewModel:
        return ProspectViewModel(
            id=response.id,
            uuid=str(response.uuid),
            user_id=response.user_id,
            first_name=response.first_name,
            last_name=response.last_name,
            email=response.email,
            phone=response.phone,
            address=response.address,
            city=response.city,
            state=response.state,
            zip=response.zip,
            country=response.country.value,
            availability=response.availability.value,
            created_at=response.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        )
    
    def present_error(self, message: str, code: Optional[str] = None) -> ErrorViewModel:
        return ErrorViewModel(message=message, code=code)


class CliProspectPresenter(ProspectPresenter):

    def present_prospect(self, response: CreateProspectResponse) -> ProspectViewModel:
        return ProspectViewModel(
            id=response.id,
            uuid=response.uuid,
            user_id=response.user_id,
            first_name=response.first_name,
            last_name=response.last_name,
            email=response.email,
            phone=response.phone,
            address=response.address,
            city=response.city,
            state=response.state,
            zip=response.zip,
            country=response.country,
            availability=response.availability,
            created_at=response.created_at,
        )
    
    def present_error(self, message: str, code: Optional[str] = None) -> ErrorViewModel:
        return ErrorViewModel(message=message, code=code)