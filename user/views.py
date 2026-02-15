from .models import User
from django.shortcuts import render
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
    
