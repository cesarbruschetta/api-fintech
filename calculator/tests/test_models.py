from django.test import TestCase
from datetime import datetime, timezone
from decimal import Decimal

from ..models import Loan, Payment, Client


class ClientTest(TestCase):
    """ Test module for Client model """

    @classmethod
    def setUpClass(cls):
        super(ClientTest, cls).setUpClass()
        Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            telephone="(91) 3794-6863",
            cpf="512.811.038-96",
        )

    def test_client(self):
        loan_01 = Client.objects.all()[0]
        self.assertEqual(loan_01.name, "Ian Marcos")


class LoanTest(TestCase):
    """ Test module for Loan and Payment model """

    @classmethod
    def setUpClass(cls):
        super(LoanTest, cls).setUpClass()

        client = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            telephone="(91) 3794-6863",
            cpf="204.421.210-24",
        )
        Loan.objects.create(
            client=client,
            amount=Decimal("1001.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )

    def setUp(self):
        self.loan_01 = Loan.objects.get(amount=Decimal("1001.00"))

    def test_loan(self):
        self.assertEqual(self.loan_01.installment, Decimal("85.69"))

    def test_payment_made(self):
        Payment.objects.create(
            loan_id=self.loan_01,
            type="MD",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("100"),
        )
        payment = Payment.objects.get(type="MD")
        self.assertEqual(payment.amount, Decimal("100"))

    def test_payment_missed(self):
        Payment.objects.create(
            loan_id=self.loan_01,
            type="MS",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )
        payment = Payment.objects.get(type="MS", loan_id=self.loan_01)
        self.assertEqual(payment.amount, Decimal("200"))

    """
        This test should failure, because 0 is not a option type.
        Search a way to do this.
    """

    def test_payment_error(self):
        Payment.objects.create(
            loan_id=self.loan_01,
            type="0",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("300"),
        )
        payment = Payment.objects.get(type="0", loan_id=self.loan_01)
        self.assertEqual(payment.amount, Decimal("300"))


class BalanceTest(TestCase):
    """ Test module for Balance model """

    @classmethod
    def setUpClass(cls):
        super(BalanceTest, cls).setUpClass()

        client = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            telephone="(91) 3794-6863",
            cpf="496.034.860-78",
        )

        cls.loan_01 = Loan.objects.create(
            client=client,
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )
        Payment.objects.create(
            loan_id=cls.loan_01,
            type="MD",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )
        Payment.objects.create(
            loan_id=cls.loan_01,
            type="MD",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )
        Payment.objects.create(
            loan_id=cls.loan_01,
            type="MS",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )

    def test_balance_loan_valid(self):
        self.assertEqual(
            self.loan_01.get_balance(
                date_base=datetime(2019, 4, 25).astimezone(tz=timezone.utc)
            ),
            Decimal("600"),
        )

    def test_balance_without_payments(self):
        self.assertEqual(
            self.loan_01.get_balance(
                date_base=datetime(2019, 3, 25).astimezone(tz=timezone.utc)
            ),
            self.loan_01.amount,
        )

    def test_balance_loan_without_date_base(self):
        self.assertEqual(self.loan_01.get_balance(), Decimal("600"))
