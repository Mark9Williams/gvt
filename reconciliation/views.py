from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Reconciliation
from .serializers import ReconciliationSerializer
from .services import generate_reconciliation_report


class ReconciliationViewSet(ModelViewSet):

    queryset = Reconciliation.objects.all()
    serializer_class = ReconciliationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["get"])
    def report(self, request, pk=None):

        reconciliation = self.get_object()

        report = generate_reconciliation_report(
            store=reconciliation.store,
            start_date=reconciliation.start_date,
            end_date=reconciliation.end_date
        )

        return Response({
            "reconciliation_id": reconciliation.id,
            "store": reconciliation.store.name,
            "start_date": reconciliation.start_date,
            "end_date": reconciliation.end_date,
            "report": report
        })