from .models import Product
from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
