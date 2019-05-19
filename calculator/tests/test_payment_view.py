import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timezone

from ..models import Loan, Payment, Client
from ..serializers import LoanSerializer
from .token import get_token


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

    def setUp(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = get_token()

    def test_register_valid_payment(self):
        date = datetime.strftime(datetime.today().astimezone(
            tz=timezone.utc), "%Y-%m-%d %H:%M%z")
        valid_payload = {"payment": "made", "amount": 100, "date": date}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {"payment": "made", "received": "100.00", "expected": "85.69"})

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
        invalid_payload = {"payment": "made", "date": "2019-05-09 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_payment_without_date(self):
        invalid_payload = {"payment": "made", "amount": 100, "date": ""}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_payment_invalid_format_date(self):
        invalid_payload = {"payment": "made",
                           "amount": 100, "date": "20190509 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payment_expected_posmade(self):
        Payment.objects.create(
            loan_id=self.loan,
            status="made",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("85.69"),
        )
        date = datetime.strftime(datetime.today().astimezone(tz=timezone.utc), "%Y-%m-%d %H:%M%z")
        valid_payload = {"payment": "made", "amount": 85.69, "date": date}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(
            response.data, {"payment": "made", "received": "85.69", "expected": "85.69"})

    def test_payment_expected_posmissed(self):
        Payment.objects.create(
            loan_id=self.loan,
            status="missed",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("85.69"),
        )
        valid_payload = {"payment": "made",
                         "amount": 85.69, "date": "2019-05-24 03:18Z"}

        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(
            response.data, {"payment": "made", "received": "85.69", "expected": "93.48"})
