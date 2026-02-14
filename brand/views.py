from .models import Brand
from .serializers import BrandSerializer
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    #permission_classes = [IsAuthenticated]
