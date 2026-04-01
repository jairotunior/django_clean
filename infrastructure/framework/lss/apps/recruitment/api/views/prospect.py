import json
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.recruitment.api.serializers.prospect import ProspectSerializer
from apps.recruitment.models import Prospect as ProspectModel
from apps.recruitment.repositories.prospect import ProspectRepositoryDjango
from lss_clean.contexts.recruitment.application.use_cases.create_prospect import CreateProspectUseCase
from lss_clean.contexts.recruitment.domain.entities import Prospect
from lss_clean.contexts.recruitment.interfaces.controllers.prospect import ProspectController



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

        params = {
            'first_name': serializer.validated_data['first_name'],
            'last_name': serializer.validated_data['last_name'],
            'email': serializer.validated_data['email'],
            'phone': serializer.validated_data['phone'],
            'address': serializer.validated_data['address'],
            'city': serializer.validated_data['city'],
            'state': serializer.validated_data['state'],
            'zip': serializer.validated_data['zip'],
            'country': serializer.validated_data['country'],
            'user_id': serializer.validated_data['user'].id,
            'availability': serializer.validated_data['availability'],
        }

        prospect_controller = settings.APP_CONTAINER.prospect_controller
        result = prospect_controller.handle_create(**params)
        if not result.is_success:
            error = prospect_controller.prospect_presenter.present_error(result.error.message, str(result.error.code))
            return Response({'error': error.message}, status=status.HTTP_400_BAD_REQUEST)
        
        success = result._success
        response = {
            'uuid': success.uuid,
            'id': success.id,
            'user_id': success.user_id,
            'first_name': success.first_name,
            'last_name': success.last_name,
            'email': success.email,
            'phone': success.phone,
            'address': success.address,
            'city': success.city,
            'state': success.state,
            'zip': success.zip,
            'country': success.country,
            'availability': success.availability,
            'created_at': success.created_at,
        }
        return Response(response, status=status.HTTP_201_CREATED)
