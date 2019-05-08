from django.contrib.postgres.validators import RangeMinValueValidator
from django.db import models
from decimal import Decimal, ROUND_DOWN
from datetime import datetime, timezone


class Client(models.Model):
    """
    Client Model
    Defines the attributes of a client
    """

    name = models.CharField("Name", max_length=255)
    surname = models.CharField("Surname", max_length=255)
    email = models.CharField("E-mail", max_length=255)
    telephone = models.CharField("Telephone", max_length=255)
    cpf = models.CharField("CPF", max_length=255, unique=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return str(self.name)


class Loan(models.Model):
    """
    Loan Model
    Defines the attributes of a loan
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(
        "Amount",
        max_digits=15,
        decimal_places=2,
        validators=[RangeMinValueValidator(Decimal("0.01"))],
    )
    term = models.IntegerField("Term", validators=[RangeMinValueValidator(1)])
    rate = models.DecimalField(
        "Rate",
        max_digits=15,
        decimal_places=2,
        validators=[RangeMinValueValidator(Decimal("0.01"))],
    )
    date_initial = models.DateTimeField(
        "Date creation", auto_now=False, auto_now_add=False
    )

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"

    def __str__(self):
        return str(self.pk)

    @property
    def installment(self):
        r = self.rate / 12
        installment = (r + r / ((1 + r) ** self.term - 1)) * self.amount
        return installment.quantize(Decimal(".01"), rounding=ROUND_DOWN)

    def get_balance(self, date_base=datetime.now().astimezone(tz=timezone.utc)):
        try:
            payments = self.payment_set.filter(type="MD", date__lte=date_base).values(
                "amount"
            )
            return self.amount - sum([payment["amount"] for payment in payments])
        except:
            return Decimal("0")


class Payment(models.Model):
    """
    Payment Model
    Defines the attributes of a Payment
    """

    loan_id = models.ForeignKey("Loan", on_delete=models.CASCADE)
    PAYMENT_CHOICES = (("MD", "Made"), ("MS", "Missed"))
    type = models.CharField("Type", max_length=2, choices=PAYMENT_CHOICES, default="MD")
    date = models.DateTimeField("Date", auto_now=False, auto_now_add=False)
    amount = models.DecimalField(
        "Amount",
        max_digits=15,
        decimal_places=2,
        validators=[RangeMinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return str(self.pk)
