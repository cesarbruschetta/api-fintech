from django.test import TestCase
from datetime import datetime
from decimal import Decimal

from ..models import Loan, Payment


class LoanTest(TestCase):
    """ Test module for Loan model """
    
    def setUp(self):
        Loan.objects.create_loan(
            amount=Decimal('1000.00'), term=12, rate=Decimal('0.05'), date_initial=datetime(2019,3,24)
        )

    def test_loan(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        self.assertEqual(
            loan_01.installment, Decimal('85.61')) #check use of decimals, because the digit is wrong
    
    def test_payment_made(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        Payment.objects.create(
            loan_id=loan_01, type='MD', date=datetime(2019,4,24), amount=Decimal('100')
        )
        payment = Payment.objects.get(type='MD')
        self.assertEqual(
            payment.amount, Decimal('100'))
    
    def test_payment_missed(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        Payment.objects.create(
            loan_id=loan_01, type='MS', date=datetime(2019,4,24), amount=Decimal('200')
        )
        payment = Payment.objects.get(type='MS')
        self.assertEqual(
            payment.amount, Decimal('200'))
    
    """
        This test should failure, because 0 is not a option type.
        Search a way to do this.
    """
    def test_payment_error(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        Payment.objects.create(
            loan_id=loan_01, type='0', date=datetime(2019,4,24), amount=Decimal('300')
        )
        payment = Payment.objects.get(type='0')
        self.assertEqual(
            payment.amount, Decimal('300'))

