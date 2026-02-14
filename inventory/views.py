from .models import StoreInventory, StockTransfer
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import StoreInventorySerializer, StockTransferSerializer

# Create your views here.
class StoreInventoryViewSet(ModelViewSet):
    queryset = StoreInventory.objects.all()
    serializer_class = StoreInventorySerializer

class  StockTransferViewSet(ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer