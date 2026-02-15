from rest_framework import serializer
from .models import Reconciliation

class ReconciliationSerializer(serializer.ModelSerializer):
    class Meta:
        model = Reconciliation
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)