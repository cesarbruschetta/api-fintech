import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Loan
from ..serializers import LoanSerializer


# initialize the APIClient app
client = Client()


class CreateNewLoanTest(TestCase):
    """ Test module for inserting a new Loan """

    def test_create_valid_loan(self):
        valid_payload = {
            "amount": 1000,
            "term": 12,
            "rate": 0.05,
            "date": "2019-05-09 03:18Z"
        }
        response = client.post(
            reverse('post_loans'),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_term_loan(self):
        invalid_payload = {
            "amount": 1000,
            "term": 0,
            "rate": 0.05,
            "date": "2019-05-09 03:18Z"
        }
        response = client.post(
            reverse('post_loans'),
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
        response = client.post(
            reverse('post_loans'),
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
        response = client.post(
            reverse('post_loans'),
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
        response = client.post(
            reverse('post_loans'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
