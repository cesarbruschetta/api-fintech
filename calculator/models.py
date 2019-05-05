from django.db import models
from decimal import Decimal


class LoanManager(models.Manager):
    def create_loan(self, *args, **kwargs):
        loan = self.create(*args, **kwargs)
        loan.save_installment()
        return loan


class Loan(models.Model):
    """
    Loan Model
    Defines the attributes of a loan
    """
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)
    term = models.IntegerField('Term')
    rate = models.DecimalField('Rate', max_digits=15, decimal_places=2)
    date_initial = models.DateTimeField('Date creation', auto_now=False, auto_now_add=False)
    installment = models.DecimalField('Installment', max_digits=15, decimal_places=2,default=Decimal('0000000000000.00'))
    objects = LoanManager()

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    def save_installment(self):
        r = self.rate / 12
        self.installment = (r + r / ((1 + r) ** self.term - 1)) * self.amount
        return self.save()


class Payment(models.Model):
    """
    Payment Model
    Defines the attributes of a Payment
    """
    loan_id = models.ForeignKey('Loan', on_delete=models.CASCADE)
    PAYMENT_CHOICES = (('MD', 'Made'), ('MS', 'Missed'))
    type = models.CharField('Type', max_length=2, choices=PAYMENT_CHOICES, default='MD')
    date = models.DateField('Date', auto_now=False, auto_now_add=False)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
