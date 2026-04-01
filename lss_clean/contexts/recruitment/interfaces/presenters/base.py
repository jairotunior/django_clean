from typing import Protocol
from lss_clean.contexts.recruitment.application.dtos.prospect import CreateProspectResponse
from lss_clean.contexts.recruitment.interfaces.view_models.prospect import ProspectViewModel
from lss_clean.contexts.recruitment.interfaces.view_models.base import ErrorViewModel
from lss_clean.contexts.recruitment.application.dtos.reject_application import RejectApplicationResponse
from lss_clean.contexts.recruitment.interfaces.view_models.application import ApplicationViewModel


class ProspectPresenter(Protocol):

    def present_prospect(self, response: CreateProspectResponse) -> ProspectViewModel: ...

    def present_error(self, message: str, code: str) -> ErrorViewModel: ...


class ApplicationPresenter(Protocol):

    def present_application(self, response: RejectApplicationResponse) -> ApplicationViewModel: ...

    def present_error(self, message: str, code: str) -> ErrorViewModel: ...