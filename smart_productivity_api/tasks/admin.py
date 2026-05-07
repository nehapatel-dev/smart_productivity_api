from django.contrib import admin
from .models import Task, ActivityLog

admin.site.register(Task)
admin.site.register(ActivityLog)
