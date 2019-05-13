import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from ..models import Loan, Client
from ..serializers import LoanSerializer


class CreateNewLoanTest(TestCase):
    """ Test module for inserting a new Loan """

    @classmethod
    def setUpClass(cls):
        super(CreateNewLoanTest, cls).setUpClass()
        cls.client_1 = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="51281103891",
        )

    def test_create_valid_loan(self):
        valid_payload = {
            "amount": 1000,
            "term": 12,
            "rate": 0.05,
            "date": "2019-05-09 03:18Z",
            "client_id": self.client_1.pk
        }
        response = self.client.post(
            reverse('loans'),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': '1', 'installment': 85.60})

    def test_create_invalid_term_loan(self):
        invalid_payload = {
            "amount": 1000,
            "term": 0,
            "rate": 0.05,
            "date": "2019-05-09 03:18Z"
        }
        response = self.client.post(
            reverse('loans'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_amount_loan(self):
        invalid_payload = {
            "term": 1,
            "rate": 0.05,
            "date": "2019-05-09 03:18Z"
        }
        response = self.client.post(
            reverse('loans'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_date_loan(self):
        invalid_payload = {
            "amount": 1000,
            "term": 1,
            "rate": 0.05
        }
        response = self.client.post(
            reverse('loans'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_rate_loan(self):
        invalid_payload = {
            "amount": 1000,
            "term": 1,
            "rate": 0,
            "date": "2019-05-09 03:18Z"
        }
        response = self.client.post(
            reverse('loans'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
