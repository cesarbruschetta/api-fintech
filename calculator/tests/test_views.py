import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Loan
from ..serializers import LoanSerializer


# initialize the APIClient app
client = Client()


class CreateNewLoanTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_payload = {
            "amount": 1000,
            "term": 12,
            "rate": 0.05,
            "date": "2019-05-09 03:18Z"
        }
        self.invalid_payload = {
            "amount": 1000,
            "term": 0,
            "rate": 0.05,
            "date": "2019-05-09 03:18Z"
        }

    def test_create_valid_loan(self):
        response = client.post(
            reverse('post_loans'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_loan(self):
        response = client.post(
            reverse('post_loans'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
