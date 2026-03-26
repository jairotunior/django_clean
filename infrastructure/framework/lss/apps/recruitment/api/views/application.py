from dataclasses import asdict
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

from apps.recruitment.api.serializers.application import CreateApplicationSerializer
from apps.recruitment.models import Application
from lss_clean.contexts.recruitment.application.dtos.profiling_command import (
    ProfilingCommand, 
    RequisitionCommand, 
    PositionCommand,
)
from apps.recruitment.repositories.prospect import ProspectRepositoryDjango
from apps.recruitment.repositories.application import ApplicationRepositoryDjango
from lss_clean.contexts.recruitment.application.use_cases.profiling_prospect import ProfilingProspectUseCase
from lss_clean.contexts.recruitment.domain.exceptions import BusinessRuleViolation, NotFoundError


def domain_to_response(application: Application):
    return {
        'uuid': application.uuid,
        'status': application.status.value,
        'created_at': application.created_at,
        'requisition': {
            'id': application.requisition.id,
            'uuid': application.requisition.uuid,
        },
        'position': {
            'id': application.position.id,
            'uuid': application.position.uuid,
            'name': application.position.name,
        },
        'availability': application.availability,
        'prospect': application.prospect_id,
    }


class ApplicationViewSet(GenericViewSet, CreateModelMixin):
    queryset = Application.objects.all()
    serializer_class = CreateApplicationSerializer
    lookup_field = 'uuid'


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = ProfilingCommand(
            prospect_id=serializer.validated_data['prospect'].id,
            requisition=RequisitionCommand(
                id=serializer.validated_data['requisition'].id,
                uuid=serializer.validated_data['requisition'].uuid,
            ),
            position=PositionCommand(
                id=serializer.validated_data['position'].id,
                uuid=serializer.validated_data['position'].uuid,
                name=serializer.validated_data['position'].name,
            ),
            availability=serializer.validated_data['availability'],
        )

        application_repository = ApplicationRepositoryDjango()
        prospect_repository = ProspectRepositoryDjango()

        try:
            application = ProfilingProspectUseCase(prospect_repository, application_repository).execute(command)
        except BusinessRuleViolation as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except NotFoundError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(domain_to_response(application), status=status.HTTP_201_CREATED)