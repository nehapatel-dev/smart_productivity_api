"""Business logic for task analytics, isolated from views."""
from django.utils import timezone
from tasks.models import Task


def get_user_task_analytics(user) -> dict:
    qs = Task.objects.filter(user=user, is_deleted=False)
    now = timezone.now()
    return {
        "total_tasks": qs.count(),
        "completed_tasks": qs.filter(status=Task.Status.COMPLETED).count(),
        "pending_tasks": qs.filter(status=Task.Status.PENDING).count(),
        "in_progress_tasks": qs.filter(status=Task.Status.IN_PROGRESS).count(),
        "overdue_tasks": qs.exclude(status=Task.Status.COMPLETED)
                           .filter(due_date__lt=now).count(),
    }
