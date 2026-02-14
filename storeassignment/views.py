from .models import StoreAssignment
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import StoreAssignmentSerializer


# Create your views here.
class StoreAssignmentViewSet(ModelViewSet):
    queryset = StoreAssignment.objects.all()
    serializer_class = StoreAssignmentSerializer