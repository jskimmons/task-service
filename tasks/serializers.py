from rest_framework import serializers

from .models import Task
from users.models import User


class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user", queryset=User.objects.all()
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "due_date",
            "idempotency_key",
            "user_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, title):
        if not title or not title.strip():
            raise serializers.ValidationError("title is required")
        return title

    def validate_due_date(self, due_date):
        if due_date is None:
            raise serializers.ValidationError("due_date is required")
        return due_date
