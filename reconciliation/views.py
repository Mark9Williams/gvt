from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Reconciliation
from .serializers import ReconciliationSerializer
from .services import generate_reconciliation_report


class ReconciliationViewSet(ModelViewSet): 

    queryset = Reconciliation.objects.all()
    serializer_class = ReconciliationSerializer

    @action(detail=True, methods=["get"])
    def report(self, request, pk=None):

        reconciliation = self.get_object()

        data = generate_reconciliation_report(
            store=reconciliation.store,
            start_date=reconciliation.start_date,
            end_date=reconciliation.end_date
        )

        return Response(data)