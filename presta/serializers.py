from rest_framework import serializers
from .models import Presta

class PrestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presta
        fields = '__all__'