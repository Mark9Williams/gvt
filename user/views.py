from .models import User
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserCreateSerializer, UserProfileSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateAPIView
# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
    
class UserProfileView(RetrieveUpdateAPIView):
    queryset = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'},status =status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'message':'Refresh token is required'},status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)



    
