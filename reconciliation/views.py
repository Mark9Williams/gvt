# from django.shortcuts import render
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .services import generate_reconciliation_report
# # Create your views here.

# class ReconciliationViewSet(ModelViewSet):
#     ...
#     @action(detail=True, methods=["get"])
#     def report(self, request, pk=None):
#         reconciliation = self.get_object()
#         data = generate_reconciliation_report(
#             store=reconciliation.store,
#             start_date=reconciliation.start_date,
#             end_date=reconciliation.end_date
#         )
#         return Response(data)