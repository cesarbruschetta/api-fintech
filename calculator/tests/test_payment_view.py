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


class RegisterPaymentTest(TestCase):

    def setUp(self):
        self.loan = Loan.objects.create(
            amount=Decimal('1000.00'), term=12, rate=Decimal('0.05'), date_initial=datetime(2019,3,24,11,30).astimezone(tz=timezone.utc)
        )

    def test_register_valid_payment(self):
        valid_payload = {
            "payment": "made",
            "amount": 100,
            "date": "2019-05-09 03:18Z"
        }
        response = client.post(
            reverse('post_payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
