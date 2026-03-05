from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all().order_by("-created_at")
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # manager sees all sales
        if user.role == "manager":
            return Sale.objects.all().order_by("-created_at")

        # seller sees only their sales
        return Sale.objects.filter(seller=user).order_by("-created_at")