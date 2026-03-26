from rest_framework import serializers
from apps.recruitment.models import Application, Prospect, Requisition, Position


class CreateApplicationSerializer(serializers.ModelSerializer):

    prospect = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Prospect.objects.all(),
        required=True,
        allow_null=False,
    )
    requisition = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Requisition.objects.all(),
        required=True,
        allow_null=False,
    )
    position = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Position.objects.all(),
        required=True,
        allow_null=False,
    )

    class Meta:
        model = Application
        fields = [
            'prospect',
            'requisition',
            'position',
            'availability',
        ]