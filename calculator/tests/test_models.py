from django.test import TestCase
from datetime import datetime
from decimal import Decimal

from ..models import Loan


class LoanTest(TestCase):
    """ Test module for Loan model """

    def setUp(self):
        Loan.objects.create(
            amount=Decimal('1000.00'), term=12, rate=Decimal('0.05'), date_initial=datetime(2019,3,24), installment=Decimal('0.00')
        )

    def test_loan(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        self.assertEqual(
            loan_01.term, 12)
