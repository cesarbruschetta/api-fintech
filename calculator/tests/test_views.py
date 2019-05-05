import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Loan
from ..serializers import LoanSerializer


# initialize the APIClient app
client = Client()