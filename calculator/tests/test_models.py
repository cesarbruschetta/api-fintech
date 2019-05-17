import unittest
from django.test import TestCase
from datetime import datetime, timezone
from decimal import *

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
            phone="9137946863",
            cpf="51281103896",
        )

    def test_client(self):
        loan_01 = Client.objects.all()[0]
        self.assertEqual(loan_01.name, "Ian Marcos")


class LoanTest(TestCase):
    """ Test module for Loan and Payment model """

    @classmethod
    def setUpClass(cls):
        super(LoanTest, cls).setUpClass()

        cls.client_1 = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="20442121024",
        )
        Loan.objects.create(
            client=cls.client_1,
            amount=Decimal("1001.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )

    def setUp(self):
        self.loan_01 = Loan.objects.get(
            amount=Decimal("1001.00"), client=self.client_1)

    def test_calculate_instalment(self):
        self.assertEqual(self.loan_01.instalment, Decimal("85.69"))

    def test_payment_made(self):
        Payment.objects.create(
            loan_id=self.loan_01,
            status="MD",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("100"),
        )
        payment = Payment.objects.get(status="MD")
        self.assertEqual(payment.amount, Decimal("100"))

    def test_payment_missed(self):
        Payment.objects.create(
            loan_id=self.loan_01,
            status="MS",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )
        payment = Payment.objects.get(status="MS", loan_id=self.loan_01)
        self.assertEqual(payment.amount, Decimal("200"))

    """
        This test should failure, because 0 is not a option status.
        Search a way to do this.
    """

    def test_payment_error(self):
        Payment.objects.create(
            loan_id=self.loan_01,
            status="0",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("300"),
        )
        payment = Payment.objects.get(status="0", loan_id=self.loan_01)
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
            phone="9137946863",
            cpf="49603486078",
        )

        cls.loan_01 = Loan.objects.create(
            client=client,
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )
        Payment.objects.create(
            loan_id=cls.loan_01,
            status="made",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )
        Payment.objects.create(
            loan_id=cls.loan_01,
            status="made",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )
        Payment.objects.create(
            loan_id=cls.loan_01,
            status="missed",
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


class InstalmentTest(TestCase):
    """ Test module for Balance model """

    @classmethod
    def setUpClass(cls):
        super(InstalmentTest, cls).setUpClass()

        cls.client1 = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="ianmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="49603486078",
        )
        Loan.objects.create(
            client=cls.client1,
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )
        cls.client2 = Client.objects.create(
            name="Ian Marcos",
            surname="Carvalho",
            email="nmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="59603486078",
        )
        Loan.objects.create(
            client=cls.client2,
            amount=Decimal("3143.50"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )
        cls.client3 = Client.objects.create(
            name="Cliente3",
            surname="Carvalho",
            email="nmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="59603486070",
        )
        Loan.objects.create(
            client=cls.client3,
            amount=Decimal("15168.50"),
            term=12,
            rate=Decimal("1.3"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )
        cls.client4 = Client.objects.create(
            name="Cliente3",
            surname="Carvalho",
            email="nmarcoscarvalho@gmail.com.br",
            phone="9137946863",
            cpf="59603486000",
        )
        Loan.objects.create(
            client=cls.client4,
            amount=Decimal("3435078.51"),
            term=7,
            rate=Decimal("2.3"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )

    def setUp(self):
        self.loan_01 = Loan.objects.get(amount="1000.00", client=self.client1)
        self.loan_02 = Loan.objects.get(amount="3143.50", client=self.client2)
        self.loan_03 = Loan.objects.get(amount="15168.50", client=self.client3)
        self.loan_04 = Loan.objects.get(
            amount="3435078.51", client=self.client4)

    def test_instalment(self):
        self.assertEqual(self.loan_01.instalment, Decimal("85.60"))

    def test_instalment_discount(self):
        Payment.objects.create(
            loan_id=self.loan_01,
            status="made",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("1000.00"),
        )
        self.loan_02 = Loan.objects.create(
            client=Client.objects.get(pk=1),
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )
        original_instalment = self.loan_01.instalment
        self.assertEqual(original_instalment, Decimal('85.60'))
        self.assertLess(self.loan_02.instalment, Decimal('85.60'))

    def test_instalment_increase(self):
        CENTS = Decimal("0.01")
        Payment.objects.create(
            loan_id=self.loan_01,
            status="missed",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("200"),
        )
        Payment.objects.create(
            loan_id=self.loan_01,
            status="made",
            date=datetime(2019, 4, 24).astimezone(tz=timezone.utc),
            amount=Decimal("1000"),
        )
        self.loan_02 = Loan.objects.create(
            client=Client.objects.get(pk=1),
            amount=Decimal("1000.00"),
            term=12,
            rate=Decimal("0.05"),
            date_initial=datetime(
                2019, 3, 24, 11, 30).astimezone(tz=timezone.utc),
        )
        original_instalment = self.loan_01.instalment
        self.assertEqual(original_instalment, Decimal('85.60'))
        self.assertGreater(self.loan_02.instalment, Decimal('85.60'))

    def test_float_places_loan1(self):
        _2places = Decimal("0.00")
        loan = self.loan_01
        with localcontext() as ctx:
            ctx.rounding = ROUND_DOWN
            rate = Decimal(f"{loan.rate}")
            term = Decimal(f"{loan.term}")
            amount = Decimal(f"{loan.amount}")
            calculated_cost = ((
                rate
                + (rate
                   / ((1 + (rate / term))
                      ** term - 1)))
                * amount).quantize(_2places)
        total_cost = Decimal(loan.term * loan.instalment)
        self.assertAlmostEqual(total_cost, calculated_cost, delta=0.08)

    def test_float_places_loan2(self):
        _2places = Decimal("0.00")
        loan = self.loan_02
        with localcontext() as ctx:
            ctx.rounding = ROUND_DOWN
            rate = Decimal(f"{loan.rate}")
            term = Decimal(f"{loan.term}")
            amount = Decimal(f"{loan.amount}")
            calculated_cost = ((
                rate
                + (rate
                   / ((1 + (rate / term))
                      ** term - 1)))
                * amount).quantize(_2places)
        total_cost = Decimal(loan.term * loan.instalment)
        self.assertAlmostEqual(total_cost, calculated_cost, delta=0.08)

    def test_float_places_loan3(self):
        _2places = Decimal("0.00")
        loan = self.loan_03
        with localcontext() as ctx:
            ctx.rounding = ROUND_DOWN
            rate = Decimal(f"{loan.rate}")
            term = Decimal(f"{loan.term}")
            amount = Decimal(f"{loan.amount}")
            calculated_cost = ((
                rate
                + (rate
                   / ((1 + (rate / term))
                      ** term - 1)))
                * amount).quantize(_2places)
        total_cost = Decimal(loan.term * loan.instalment)
        self.assertAlmostEqual(total_cost, calculated_cost, delta=0.08)

    def test_float_places_loan3(self):
        _2places = Decimal("0.00")
        loan = self.loan_04
        with localcontext() as ctx:
            ctx.rounding = ROUND_DOWN
            rate = Decimal(f"{loan.rate}")
            term = Decimal(f"{loan.term}")
            amount = Decimal(f"{loan.amount}")
            calculated_cost = ((
                rate
                + (rate
                   / ((1 + (rate / term))
                      ** term - 1)))
                * amount).quantize(_2places)
        total_cost = Decimal(loan.term * loan.instalment)
        self.assertAlmostEqual(total_cost, calculated_cost, delta=0.08)
