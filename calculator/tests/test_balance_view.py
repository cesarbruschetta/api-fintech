import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timezone

from ..models import Loan, Payment, Client
from ..serializers import LoanSerializer


class BalanceViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BalanceViewTest, cls).setUpClass()

        client = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="20442121027",
        )
        cls.loan = Loan.objects.create(
            client=client,
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )
        Payment.objects.create(
            loan_id=cls.loan,
            status="made",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )
        Payment.objects.create(
            loan_id=cls.loan,
            status="made",
            date=datetime(2019, 5, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )

    def test_get_balance(self):
        valid_payload = {"date": "2019-06-09 03:18Z"}
        response = self.client.get(
            reverse('balance', kwargs={'pk': self.loan.pk}),
            valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"balance": Decimal("600")})

    def test_get_balance_without_payload(self):
        response = self.client.get(
            reverse('balance', kwargs={'pk': self.loan.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"balance": Decimal("800")})

    def test_get_balance_invalid_date(self):
        valid_payload = {"date": ""}
        response = self.client.get(
            reverse('balance', kwargs={'pk': self.loan.pk}),
            valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_balance_invalid_loan(self):
        response = self.client.get(
            reverse('balance', kwargs={'pk': 850})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
