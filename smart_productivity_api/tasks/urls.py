from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, ActivityLogListView, task_page  # ✅ FIX: task_page add kiya

router = DefaultRouter()
router.register(r"", TaskViewSet, basename="task")

urlpatterns = [
    path("logs/", ActivityLogListView.as_view(), name="activity-logs"),
    path("page/", task_page, name="task_page"),  # ✅ FIX: views.task_page hata diya
]

urlpatterns += router.urls