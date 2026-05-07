from rest_framework import viewsets, permissions
from .permissions import IsOwner

from .models import Category
from .serializers import CategorySerializer

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# API VIEWSET
class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# HTML PAGE VIEW
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