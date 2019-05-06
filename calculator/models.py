from django.db import models
from django.utils import timezone


class Loans(models.Model):

    amount = models.FloatField()
    term = models.PositiveIntegerField()
    rate = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    created_loans = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_loans += 1

    @property
    def url_id(self):
        long_id = f'{self.created_loans:015d}'
        return '{}-{}-{}-{}'.format(long_id[0:3], long_id[3:7], long_id[7:11], long_id[11:16])

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

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

        def __str__(self):
            return self.name


class Payments(models.Model):
    payment_status = (('missed', 'Missed'),('made', 'Made'))
    loan = models.ForeignKey(Loans, on_delete='PROTECT')
    paid = models.CharField(choices=payment_status, max_length=6)
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return f'Payments(loan={self.loan}, paid{self.paid}, amount={self.amount}, date={self.date})'

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

        def __str__(self):
            return self.name


class Balance(models.Model):
    loan = models.ForeignKey(Loans, on_delete='PROTECT')

    @property
    def get_balance(self):
        payments = Payments.objects.filter(loan=self.loan, paid='made')
        return self.loan.amount - sum([pay.amount for pay in payments])

    class Meta:
        abstract = True
        verbose_name = 'Balance'
        verbose_name_plural = "Balances"

        def __str__():
            return 'Balance: {self.get_balance}'

        def __repr__():
            return 'Balance(loan={self.loan})'
