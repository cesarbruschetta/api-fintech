import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timezone

from ..models import Loan, Payment, Client
from ..serializers import LoanSerializer


class RegisterPaymentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(RegisterPaymentTest, cls).setUpClass()

        client = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="20442121029",
        )
        cls.loan = Loan.objects.create(
            client=client,
            amount=Decimal("1001.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )

    def test_register_valid_payment(self):
        valid_payload = {"payment": "made",
                         "amount": 100, "date": "2019-05-09 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {})

    def test_register_payment_without_loan(self):
        valid_payload = {"payment": "made",
                         "amount": 100, "date": "2019-05-09 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': '000-0000-0000-0005'}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_register_payment_without_type(self):
        valid_payload = {"payment": "", "amount": 100,
                         "date": "2019-05-09 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_payment_without_amount(self):
        valid_payload = {"payment": "made", "date": "2019-05-09 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
        )

    def test_register_payment_without_date(self):
        valid_payload = {"payment": "made", "amount": 100, "date": ""}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_payment_invalid_format_date(self):
        valid_payload = {"payment": "made",
                         "amount": 100, "date": "20190509 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
