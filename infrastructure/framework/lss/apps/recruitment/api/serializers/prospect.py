from rest_framework import serializers
from apps.recruitment.models import Prospect as ProspectModel


class ProspectSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProspectModel
        fields = [
            'id', 
            'uuid',
            'user', 
            'first_name', 
            'last_name', 
            'email',
            'phone', 
            'address', 
            'city', 
            'state', 
            'zip', 
            'country', 
            'availability', 
            'created_at'
        ]