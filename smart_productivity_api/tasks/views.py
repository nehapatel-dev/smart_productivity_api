from django.utils import timezone
from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions import IsOwner
from services.analytics import get_user_task_analytics

from .models import Task, ActivityLog
from .serializers import TaskSerializer, ActivityLogSerializer
from .filters import TaskFilter

from categories.models import Category   # ✅ FIX: missing import


# =========================
# TASK API VIEWSET
# =========================
class TaskViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for tasks (owner-scoped).
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "status", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Task.objects.alive().filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        ActivityLog.objects.create(user=self.request.user, task=task, action="created")

    def perform_update(self, serializer):
        task = serializer.save()
        ActivityLog.objects.create(user=self.request.user, task=task, action="updated")

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted", "updated_at"])
        ActivityLog.objects.create(user=self.request.user, task=instance, action="deleted")

    @action(detail=False, methods=["get"], url_path="analytics")
    def analytics(self, request):
        return Response(get_user_task_analytics(request.user))

    @action(detail=False, methods=["get"], url_path="reminders")
    def reminders(self, request):
        now = timezone.now()

        upcoming = self.get_queryset().exclude(
            status=Task.Status.COMPLETED
        ).filter(
            due_date__gte=now,
            due_date__lte=now + timedelta(hours=24)
        )

        return Response(
            TaskSerializer(upcoming, many=True, context={"request": request}).data
        )


# =========================
# ACTIVITY LOG API
# =========================
class ActivityLogListView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivityLog.objects.filter(user=self.request.user)


# =========================
# TASK HTML UI PAGE
# =========================
@login_required
def task_page(request):

    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')

        if title:

            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                category_id=category_id
            )

            return redirect('/api/tasks/page/')

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'categories': categories
    })