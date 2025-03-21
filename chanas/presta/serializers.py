from rest_framework import serializers
from .models import presta

class PrestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = presta
        fields = '__all__'