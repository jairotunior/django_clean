from re import A
from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

from apps.recruitment.api.serializers.application import CreateApplicationSerializer
from apps.recruitment.models import Application


def domain_to_response(application: Application):
    return {
        'uuid': application.uuid,
        'id': application.id,
        'status': application.status,
        'created_at': application.created_at,
        'requisition': application.requisition,
        'position': application.position,
        'availability': application.availability,
    }


class ApplicationViewSet(GenericViewSet, CreateModelMixin):
    queryset = Application.objects.all()
    serializer_class = CreateApplicationSerializer
    lookup_field = 'uuid'


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        params = {
            'prospect_id': serializer.validated_data['prospect'].id,
            'requisition_id': serializer.validated_data['requisition'].id,
            'position_id': serializer.validated_data['position'].id,
            'availability': serializer.validated_data['availability'],
        }

        controller = settings.APP_CONTAINER.prospect_controller
        result = controller.handle_profiling(**params)
        if not result.is_success:
            error = controller.application_presenter.present_error(result.error.message, str(result.error.code))
            return Response({'error': str(error.message), 'code': error.code}, status=status.HTTP_400_BAD_REQUEST)
        
        success = result._success
        return Response(domain_to_response(success), status=status.HTTP_201_CREATED)