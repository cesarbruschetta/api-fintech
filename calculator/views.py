from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from decimal import Decimal
from datetime import datetime

from .models import Loan
from .serializers import LoanSerializer, PaymentSerializer, BalanceSerializer


class LoanView(ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def performe_create(self, serializer):
        loan = get_object_or_404(
            Loan, id=self.request.data.get('loan_id')
        )
        return serializer.save(loan=loan)

@api_view(['POST'])
def post_payments(request, pk):
    try:
        Loan.objects.get(pk=pk)
    except Loan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    data = {
        'loan_id': pk,
        'type': request.data.get('payment'),
        'date': request.data.get('date'),
        'amount': request.data.get('amount')
    }
    serializer = PaymentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_balance(request, pk):
    try:
        Loan.objects.get(pk=pk)
    except Loan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BalanceSerializer(data={'date': request.query_params.get('date'), 'loan_id': pk})
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
