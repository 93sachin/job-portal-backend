from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "job", "applied_at"]
        read_only_fields = ["id", "applied_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["applicant"] = request.user
        return super().create(validated_data)