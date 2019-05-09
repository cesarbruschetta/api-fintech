import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timezone

from ..models import Loan, Payment
from ..serializers import LoanSerializer


# initialize the APIClient app
client = Client()


class BalanceViewTest(TestCase):

    def setUp(self):
        self.loan = Loan.objects.create(
            amount=Decimal('1000.00'), term=12, rate=Decimal('0.05'), date_initial=datetime(2019,3,24,11,30).astimezone(tz=timezone.utc)
        )
        Payment.objects.create(
            loan_id=self.loan, type='made', date=datetime(2019,4,24).astimezone(tz=timezone.utc), amount=Decimal('200')
        )
        Payment.objects.create(
            loan_id=self.loan, type='made', date=datetime(2019,5,24).astimezone(tz=timezone.utc), amount=Decimal('200')
        )

    def test_get_balance(self):
        valid_payload = {
            "date": "2019-06-09 03:18Z"
        }
        response = client.get(
            reverse('get_balance', kwargs={'pk': self.loan.pk}),
            valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'balance': 600})

    def test_get_balance_without_payload(self):
        response = client.get(
            reverse('get_balance', kwargs={'pk': self.loan.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'balance': 800})
    
    def test_get_balance_invalid_date(self):
        valid_payload = {
            "date": ""
        }
        response = client.get(
            reverse('get_balance', kwargs={'pk': self.loan.pk}),
            valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_balance_invalid_loan(self):
        response = client.get(
            reverse('get_balance', kwargs={'pk': 850})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
