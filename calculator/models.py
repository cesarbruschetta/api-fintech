from django.db import models
from django.forms import DecimalField
from django.core.validators import MinValueValidator

from decimal import Decimal, ROUND_FLOOR, localcontext
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


def increment_loan_id():
    id_loan = '{:015d}'.format(Loan.objects.count() + 1)
    return '{}-{}-{}-{}'.format(id_loan[:3], id_loan[3:7], id_loan[7:11], id_loan[11:15])


class Client(models.Model):
    """
    Client Model
    Defines the attributes of a client
    """

    name = models.CharField("Name", max_length=30)
    surname = models.CharField("Last name", max_length=30)
    email = models.EmailField("E-mail")
    phone = models.BigIntegerField("Phone")
    cpf = models.BigIntegerField("CPF", unique=True)

    @property
    def is_indebted(self):
        
        loans = self.loan_set.all()
        mp = 0
        for loan in loans:
            balance = loan.get_balance(date_base=loan.expiration_date)
            if balance > 0:
                mp = loan.missed_payments
                
        if mp >= 3:
            return True
        return False

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"Client(id={self.id}, name={self.name}, surname={self.surname}, email={self.email}, phone={self.phone}, cpf={self.cpf})"


class Loan(models.Model):
    """
    Loan Model
    Defines the attributes of a loan
    """
    CENTS = Decimal("0.00")

    id = models.CharField(
        max_length=19, default=increment_loan_id, editable=False, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(
        "Amount",
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    date_initial = models.DateTimeField(
        "Date creation", auto_now=False, auto_now_add=False
    )
    term = models.DecimalField(
        "Term",
        max_digits=2,
        decimal_places=0,
        validators=[MinValueValidator(Decimal("1"))],
    )
    rate = models.DecimalField(
        "Rate",
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    rate_adjust = models.DecimalField(
        "Adjustment",
        editable=False,
        default=Decimal('0.00'),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    instalment = models.DecimalField(
        "Instalment",
        editable=False,
        default=Decimal('0.00'),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    
    @property
    def expiration_date(self):
        return self.date_initial + relativedelta(months=+self.term)
    
    @property
    def missed_payments(self):
        return self.payment_set.filter(status="missed").count()

    def _rate_adjustment(self):
        loans_history = self.client.loan_set.all()
        missed_payments = sum(
            [ loan.missed_payments for loan in loans_history]
        )
        adjustment = Decimal('0.00')
        if len(loans_history) >= 1:
            if missed_payments == 0:
                adjustment = Decimal("-0.002")
            elif 0 < missed_payments <= 3:
                adjustment = Decimal("0.004")
        return adjustment

    def calculate_instalment(self):
        """Returns a instalment value in loan creation"""
        

        with localcontext() as ctx:
            ctx.rounding = ROUND_FLOOR
            rate = Decimal(f"{self.rate}")
            term = Decimal(f"{self.term}")
            amount = Decimal(f"{self.amount}")
            r = (rate + self._rate_adjustment()) / term
            instalment = ((
                r
                + r
                / (ctx.power((1 + r), term)
                   - 1)) * amount).quantize(self.CENTS)
        return instalment

    # def monthly_instalments(self):
    #     """Returns a instalment value based on made/missed payments"""
    #     remainder_instalments = self.term - self.payment_set.count()
    #     next_instalment = (self.get_balance()/remainder_instalments).quantize(self.CENTS)
    #     return next_instalment

    def get_balance(self, date_base=datetime.now().astimezone(tz=timezone.utc)):
        try:
            payments = self.payment_set.filter(
                status="made", date__lte=date_base
            ).values("amount")
            return Decimal(self.instalment * self.term).quantize(self.CENTS) - sum([payment["amount"] for payment in payments])
        except:
            return Decimal(self.instalment * self.term)

    def save(self, *args, **kwargs):
        self.rate_adjustment = self._rate_adjustment()
        self.instalment = self.calculate_instalment()
        super(Loan, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"

    def __str__(self):
        return f"Loan(loan_id={self.id}, amount={self.amount}, term={self.term}, rate={self.rate}, date_initial={self.date_initial})"


class Payment(models.Model):
    """
    Payment Model
    Defines the attributes of a Payment
    """
    PAYMENT_CHOICES = (('made', 'made'), ('missed', 'missed'))
    CENTS = Decimal("0.00")

    loan_id = models.ForeignKey('Loan', on_delete=models.CASCADE)
    status = models.CharField(
        'status', db_column='type', max_length=6, choices=PAYMENT_CHOICES)
    date = models.DateTimeField('Date', auto_now=False, auto_now_add=False)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2,
                                 validators=[
                                     MinValueValidator(Decimal("0.01"))
                                 ])
    amount_expected = models.DecimalField('Amount', max_digits=15, decimal_places=2, editable=False,
                                 default=Decimal("0.00"), 
                                 )

    def _instalment_expected(self):
        """Returns a instalment value based on made/missed payments"""
        loan = self.loan_id
        remainder_instalments = loan.term - loan.payment_set.count()
        next_instalment = (loan.get_balance()/remainder_instalments).quantize(self.CENTS)
        return next_instalment
    
    def __str__(self):
        return f"Payment(loan_id={self.loan_id}, status={self.status}, date={self.date}, amount={self.amount})"

    def save(self, *args, **kwargs):
        self.amount_expected = self._instalment_expected()
        super(Payment, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
