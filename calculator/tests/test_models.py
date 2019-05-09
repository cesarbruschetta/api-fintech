from django.test import TestCase
from datetime import datetime, timezone
from decimal import Decimal

from ..models import Loan, Payment


class LoanTest(TestCase):
    """ Test module for Loan and Payment model """
    
    def setUp(self):
        Loan.objects.create(
            amount=Decimal('1000.00'), term=12, rate=Decimal('0.05'), date=datetime(2019,3,24,11,30).astimezone(tz=timezone.utc)
        )

    def test_loan(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        self.assertEqual(
            loan_01.installment, Decimal('85.60'))
    
    def test_payment_made(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        Payment.objects.create(
            loan_id=loan_01, payment='made', date=datetime(2019,4,24).astimezone(tz=timezone.utc), amount=Decimal('100')
        )
        payment = Payment.objects.get(payment='made')
        self.assertEqual(
            payment.amount, Decimal('100'))
    
    def test_payment_missed(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        Payment.objects.create(
            loan_id=loan_01, payment='MS', date=datetime(2019,4,24).astimezone(tz=timezone.utc), amount=Decimal('200')
        )
        payment = Payment.objects.get(payment='MS')
        self.assertEqual(
            payment.amount, Decimal('200'))
    
    """
        This test should failure, because 0 is not a option type.
        Search a way to do this.
    """
    def test_payment_error(self):
        loan_01 = Loan.objects.get(amount=Decimal('1000.00'))
        Payment.objects.create(
            loan_id=loan_01, payment='0', date=datetime(2019,4,24).astimezone(tz=timezone.utc), amount=Decimal('300')
        )
        payment = Payment.objects.get(payment='0')
        self.assertEqual(
            payment.amount, Decimal('300'))


class BalanceTest(TestCase):
    """ Test module for Balance model """
    
    def setUp(self):
        self.loan_01 = Loan.objects.create(
            amount=Decimal('1000.00'), term=12, rate=Decimal('0.05'), date=datetime(2019,3,24,11,30).astimezone(tz=timezone.utc)
        )
        Payment.objects.create(
            loan_id=self.loan_01, payment='made', date=datetime(2019,4,24).astimezone(tz=timezone.utc), amount=Decimal('200')
        )
        Payment.objects.create(
            loan_id=self.loan_01, payment='made', date=datetime(2019,4,24).astimezone(tz=timezone.utc), amount=Decimal('200')
        )
        Payment.objects.create(
            loan_id=self.loan_01, payment='MS', date=datetime(2019,4,24).astimezone(tz=timezone.utc), amount=Decimal('200')
        )
    
    def test_balance_loan_valid(self):
        self.assertEqual(self.loan_01.get_balance(date_base=datetime(2019,4,25).astimezone(tz=timezone.utc)), Decimal('600'))

    def test_balance_without_payments(self):
        self.assertEqual(self.loan_01.get_balance(date_base=datetime(2019,3,25).astimezone(tz=timezone.utc)), self.loan_01.amount)
    
    def test_balance_loan_without_date_base(self):
        self.assertEqual(self.loan_01.get_balance(), Decimal('600'))