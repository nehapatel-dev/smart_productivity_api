from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet
from . import views


router = DefaultRouter()
router.register(r'', CategoryViewSet, basename='category')

urlpatterns = [
    path('page/', views.category_page, name='category_page'),
]

urlpatterns += router.urls