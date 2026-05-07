from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from categories.models import Category

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer
)

User = get_user_model()


# =========================
# REGISTER API
# =========================
class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            "success": True,
            "message": "User registered successfully.",
            "user": UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


# =========================
# LOGIN API
# =========================
class LoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


# =========================
# PROFILE API
# =========================
class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):

        return self.request.user


# =========================
# HOME PAGE
# =========================
def auth_home(request):

    return render(request, 'auth_home.html')


# =========================
# REGISTER HTML PAGE
# =========================
def register_page(request):

    context = {}

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:

            context['error'] = 'Passwords do not match'
            return render(request, 'register.html', context)

        if User.objects.filter(username=username).exists():

            context['error'] = 'Username already exists'
            return render(request, 'register.html', context)

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        context['success'] = True

    return render(request, 'register.html', context)


# =========================
# LOGIN HTML PAGE
# =========================
def login_page(request):

    context = {}

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            context['success'] = 'Login Successful'

            return redirect('/api/categories/page/')

        else:

            context['error'] = 'Invalid Username or Password'

    return render(request, 'login.html', context)


# =========================
# CATEGORY HTML PAGE
# =========================
@login_required
def category_page(request):

    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':

        name = request.POST.get('name')

        if name:

            Category.objects.create(
                user=request.user,
                name=name
            )

            return redirect('/api/categories/page/')

    context = {
        'categories': categories
    }

    return render(request, 'categories.html', context)