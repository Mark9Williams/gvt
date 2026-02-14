from .models import StoreAssignment
from rest_framework import serializers

class StoreAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAssignment
        fields = "__all__"