from django.db import models
from decimal import Decimal


class Loan(models.Model): 
    """
    Loan Model
    Defines the attributes of a loan
    """
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)
    term = models.IntegerField('Term')
    rate = models.DecimalField('Rate', max_digits=15, decimal_places=2)
    date_initial = models.DateField('Date creation', auto_now=False, auto_now_add=False)
    installment = models.DecimalField('Installment', max_digits=15, decimal_places=2,default=Decimal('0000000000000.00'))

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    @classmethod
    def create(cls, title, ):
        book = cls(title=title)
        # do something with the book
        return book


class Payment(models.Model):
    """
    Payment Model
    Defines the attributes of a Payment
    """
    loan_id = models.ForeignKey('Loan', on_delete=models.CASCADE)
    PAYMENT_CHOICES = (('1', 'Made'), ('0', 'Missed'))
    type = models.CharField('Type',max_length=1, choices=PAYMENT_CHOICES, default='1')
    date = models.DateField('Date', auto_now=False, auto_now_add=False)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
