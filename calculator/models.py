from django.db import models
from django.utils import timezone


class Loan(models.Model):

    amount = models.FloatField()
    term = models.PositiveIntegerField(default=12)
    rate = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    @property
    def installments(self):
        r = self.rate/12
        return (r + r / (((1 + r) ** self.term) - 1))*self.amount

    @property
    def balance(self):
        selection = self.payment_set.values('amount')
        return self.amount - sum(selection)

    def __str__(self):
        return f'Loans({self.amount}, {self.term}, {self.rate}, {self.date})'

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

        def __str__(self):
            return self.name


class Payment(models.Model):
    
    payment_status_choice = (('missed', 'Missed'),('made', 'Made'))
    
    loan = models.ForeignKey(Loan, on_delete='PROTECT')
    paid = models.CharField(choices=payment_status_choice, max_length=6)
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Payments(loan={self.loan}, paid{self.paid}, amount={self.amount}, date={self.date})'

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

        def __str__(self):
            return self.name

