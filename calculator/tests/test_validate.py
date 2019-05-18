import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timezone

from .token import get_token
from ..models import Loan, Payment, Client


class ValidateloanPaymentTest(TestCase):
        
    @classmethod
    def setUpClass(cls):
        super(ValidateloanPaymentTest, cls).setUpClass()
        
        client = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="11142121030",
        )
        cls.loan = Loan.objects.create(
            client=client,
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(2019, 1, 1, 12, 00).astimezone(tz=timezone.utc),
        )
        
    def setUp(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = get_token()
        
    def test_register_payment_over_value(self):
        valid_payloan = {"payment": "made", "amount": 2000, "date": "2019-02-01 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payloan),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Payment amount higher than its loan balance.", response.json()["non_field_errors"])
    
    def test_register_payment_before_dateinitial(self):
        valid_payloan = {"payment": "made", "amount": 100, "date": "2018-12-01 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payloan),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Date of a payment before the creation date of its loan.", response.json()["non_field_errors"])
        
    def test_register_payment_total_pay_afer_try_pay(self):
        valid_payloan = {"payment": "made", "amount": 1000, "date": "2019-02-01 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payloan),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        valid_payloan = {"payment": "made", "amount": 100, "date": "2019-02-02 03:18Z"}
        response = self.client.post(
            reverse('payments', kwargs={'pk': self.loan.pk}),
            data=json.dumps(valid_payloan),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class ValidateClientLoanTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ValidateClientLoanTest, cls).setUpClass()
        
        cls.client_1 = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="20442121031",
        )

    def tearDown(self):
        self.client_1.loan_set.all().delete()
        
    def setUp(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = get_token()

    def test_register_two_loan_unpayment(self):
        loan = Loan.objects.create(
            client=self.client_1,
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(2019, 1, 1, 12, 00).astimezone(tz=timezone.utc),
        )
        
        Payment.objects.create(
            loan_id=loan,
            status="missed",
            date=datetime(2019, 2, 1).astimezone(tz=timezone.utc),
            amount=loan.instalment,
        )
        Payment.objects.create(
            loan_id=loan,
            status="missed",
            date=datetime(2019, 3, 1).astimezone(tz=timezone.utc),
            amount=loan.instalment,
        )
        Payment.objects.create(
            loan_id=loan,
            status="missed",
            date=datetime(2019, 4, 1).astimezone(tz=timezone.utc),
            amount=loan.instalment,
        )

        valid_payloan = {
            "amount": 1000,
            "term": 12,
            "rate": 0.05,
            "date": "2019-06-01 03:18Z",
            "client_id": self.client_1.pk,
        }
        response = self.client.post(
            reverse('loans'),
            data=json.dumps(valid_payloan),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Denied loan request", response.json()["client"])

    def test_register_two_loan_first_pay(self):
        loan = Loan.objects.create(
            client=self.client_1,
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(2019, 1, 1, 12, 00).astimezone(tz=timezone.utc),
        )

        Payment.objects.create(
            loan_id=loan,
            status="missed",
            date=datetime(2019, 2, 1).astimezone(tz=timezone.utc),
            amount=loan.instalment,
        )
        Payment.objects.create(
            loan_id=loan,
            status="missed",
            date=datetime(2019, 3, 1).astimezone(tz=timezone.utc),
            amount=loan.instalment,
        )
        Payment.objects.create(
            loan_id=loan,
            status="missed",
            date=datetime(2019, 4, 1).astimezone(tz=timezone.utc),
            amount=loan.instalment,
        )
        Payment.objects.create(
            loan_id=loan,
            status="made",
            date=datetime(2019, 5, 1).astimezone(tz=timezone.utc),
            amount=Decimal("1027.20"),
        )

        valid_payloan = {
            "amount": 1000,
            "term": 12,
            "rate": 0.05,
            "date": "2019-06-01 03:18Z",
            "client_id": self.client_1.pk,
        }
        response = self.client.post(
            reverse('loans'),
            data=json.dumps(valid_payloan),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_register_loan_not_total_payment(self):
        loan = Loan.objects.create(
            client=self.client_1,
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(2019, 1, 1, 12, 00).astimezone(tz=timezone.utc),
        )
        Payment.objects.create(
            loan_id=loan,
            status="made",
            date=datetime(2019, 2, 1).astimezone(tz=timezone.utc),
            amount=loan.instalment,
        )
        
        # loan 1 is not payment
        self.assertTrue(loan.get_balance() > 0)
        
        valid_payloan = {
            "amount": 1000,
            "term": 12,
            "rate": 0.05,
            "date": "2019-03-01 03:18Z",
            "client_id": self.client_1.pk,
        }
        response = self.client.post(
            reverse('loans'),
            data=json.dumps(valid_payloan),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)