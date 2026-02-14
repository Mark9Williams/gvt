from .models import Store
from django.shortcuts import render
from .serializers import StoreSerializer
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

