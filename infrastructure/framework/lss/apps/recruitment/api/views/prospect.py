from dataclasses import asdict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.recruitment.api.serializers.prospect import ProspectSerializer
from apps.recruitment.models import Prospect as ProspectModel
from apps.recruitment.repositories.prospect import ProspectRepositoryDjango
from lss_clean.contexts.recruitment.application.use_cases.create_prospect import CreateProspectUseCase
from lss_clean.contexts.recruitment.application.dtos.prospect_command import CreateProspectCommand
from lss_clean.contexts.recruitment.domain.enums import CountryName, Availability
from lss_clean.contexts.recruitment.domain.exceptions import BusinessRuleViolation
from lss_clean.contexts.recruitment.domain.entities import Prospect



def domain_to_response(prospect: Prospect):
    return {
        'uuid': prospect.uuid,
        'id': prospect.id,
        'user_id': prospect.user_id,
        'first_name': prospect.first_name,
        'last_name': prospect.last_name,
        'email': prospect.email,
        'phone': prospect.phone,
        'address': prospect.address,
        'city': prospect.city,
        'state': prospect.state,
        'zip': prospect.zip,
        'country': prospect.country,
        'availability': prospect.availability,
        'created_at': prospect.created_at,
    }


class ProspectAPIView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    queryset = ProspectModel.objects.all()
    serializer_class = ProspectSerializer
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = CreateProspectCommand(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
            phone=serializer.validated_data['phone'],
            address=serializer.validated_data['address'],
            city=serializer.validated_data['city'],
            state=serializer.validated_data['state'],
            zip=serializer.validated_data['zip'],
            country=serializer.validated_data['country'],
            user_id=serializer.validated_data['user'].id,
            availability=serializer.validated_data['availability'],
        )

        prospect_repository = ProspectRepositoryDjango()
        try:
            prospect = CreateProspectUseCase(prospect_repository).execute(command)
        except BusinessRuleViolation as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(domain_to_response(prospect), status=status.HTTP_201_CREATED)