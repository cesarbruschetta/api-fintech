from django.db import models
from django.utils import timezone


class Loans(models.Model):
    amount = models.FloatField()
    term = models.IntegerField()
    rate = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    @property
    def installments(self):
        r = self.rate/12
        return (r + r / (((1 + r) ** self.term) - 1))*self.amount

    @property
    def balance(self):
        selection = Payments.objects.filter(loan_id=self.id, paid='made')
        return self.amount - sum([pay.amount for pay in selection])

    def __repr__(self):
        return f'Loans({self.amount}, {self.term}, {self.rate}, {self.date})'


class Payments(models.Model):
    payment_status = (
        ('missed', 'missed'),
        ('made', 'made'),
    )

    loan = models.ForeignKey(Loans, on_delete='PROTECT')
    paid = models.TextField(choices=payment_status)
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
