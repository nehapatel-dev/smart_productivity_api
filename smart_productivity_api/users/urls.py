from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ProfileView
from . import views

urlpatterns = [
    path('', views.auth_home),
    path('register-page/', views.register_page),
    path('login-page/', views.login_page),
    path('page/', views.category_page),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
