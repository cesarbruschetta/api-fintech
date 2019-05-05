from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import LoanSerializer


@api_view(['POST'])
def post_loan(request):
    return response({})
