from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from datetime import datetime

from .models import Loan
from .serializers import LoanSerializer, PaymentSerializer


@api_view(['POST'])
def post_loans(request):
    data = {
        'amount': request.data.get('amount'),
        'term': request.data.get('term'),
        'rate': request.data.get('rate'),
        'date_initial': request.data.get('date')
    }
    serializer = LoanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        loan = Loan.objects.get(pk=pk)
    except Loan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    date_base = request.query_params.get('date')
    if date_base:
        balance = loan.get_balance(date_base)
    else:
        balance = loan.get_balance()
    return Response({'balance': balance}, status=status.HTTP_200_OK)
