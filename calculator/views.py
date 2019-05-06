from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from datetime import datetime

from .models import Loan
from .serializers import LoanSerializer

@api_view(['POST'])
def post_loans(request):
    data = {
        'amount': request.data.get('amount'),
        'term': request.data.get('term'),
        'rate': request.data.get('term'),
        'date_initial': request.data.get('date')
    }
    serializer = LoanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
