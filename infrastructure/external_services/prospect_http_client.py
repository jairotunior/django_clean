from lss_clean.contexts.recruitment.domain.entities import Prospect
from lss_clean.contexts.recruitment.application.services.prospect import ProspectServicePort


class ProspectHTTPCLient(ProspectServicePort):

    def __init__(self, base_url: str, http_client):
        self.base_url = base_url
        self.http_client = http_client

    def reserve_items(self, prospect: Prospect) -> None:
        payload = {
            "first_name": prospect.first_name,
            "last_name": prospect.last_name,
            "email": prospect.email,
            "phone": prospect.phone,
            "address": prospect.address,
            "city": prospect.city,
            "state": prospect.state,
            "zip": prospect.zip,
            "country": prospect.country,
        }
        response = self.http_client.post(f"{self.base_url}/prospects", json=payload)
        response.raise_for_status()
