import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from ..models import Client
from .token import get_token


class CreateNewClientTest(TestCase):
    """ Test module for inserting a new Client """
    def setUp(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = get_token()
        
    def test_create_valid_client(self):
        valid_payload = {
            "name": "Ian Marcos",
            "surname": "Carvalho",
            "email": "ianmarcoscarvalho@gmail.com.br",
            "phone": "9137946863",
            "cpf": "51281103898",
        }
        response = self.client.post(
            reverse('clients'),
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"client_id": "1"})

    def test_create_invalid_client(self):
        invalid_payload = {
            "name": "Ian Marcos",
            "surname": "Carvalho",
            "email": "ianmarcoscarvalho@gmail.com.br",
            "phone": "9137946863",
        }
        response = self.client.post(
            reverse('clients'),
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
