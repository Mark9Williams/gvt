from .models import User
from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
