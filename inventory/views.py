from .models import StoreInventory
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import StoreInventorySerializer

# Create your views here.
class StoreInventoryViewSet(ModelViewSet):
    queryset = StoreInventory.objects.all()
    serializer_class = StoreInventorySerializer
