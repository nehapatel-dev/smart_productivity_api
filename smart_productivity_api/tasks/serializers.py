from django.utils import timezone
from rest_framework import serializers
from categories.models import Category
from .models import Task, ActivityLog


class TaskSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id", "title", "description", "priority", "status",
            "due_date", "category", "category_name",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    # Limit category choices to the requesting user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["category"].queryset = Category.objects.filter(user=request.user)

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ("id", "task", "action", "detail", "created_at")
