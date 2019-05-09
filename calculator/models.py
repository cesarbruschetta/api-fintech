from django.contrib.postgres.validators import RangeMinValueValidator
from django.db import models
from decimal import Decimal, ROUND_DOWN
from datetime import datetime, timezone


class Client(models.Model):
    name = models.CharField('Name', max_length=15)
    surname = models.CharField('Last name', max_length=15)
    email = models.EmailField('E-mail')
    phone = models.BigIntegerField('Phone')
    cpf = models.BigIntegerField('CPF')

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __repr__(self):
        return f'Client(id={self.pf}, name={self.name}, surname={self.surname}, email={self.email}, phone={self.phone}, cpf={self.cpf}'


class Loan(models.Model):
    """
    Loan Model
    Defines the attributes of a loan
    """
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2,
                                 validators=[
                                  RangeMinValueValidator(Decimal('0.01'))
                                 ])
    term = models.IntegerField('Term',validators=[
                                RangeMinValueValidator(1)
                               ])
    rate = models.DecimalField('Rate', max_digits=15, decimal_places=2, validators=[
                                RangeMinValueValidator(1)
                               ])
    date_initial = models.DateTimeField('Date creation', auto_now=False, auto_now_add=False)


    @property
    def installment(self):
        number_missed_payments = len(self.payment_set.filter(type='MS').values('amount'))
        if loan.get_balance == 0:
            if number_missed_payments == 0:
                bias = -0.02
            elif 0 < number_missed_payments <= 3:
                bias = 0.04
        r = self.rate / self.term
        installment = (r + r / ((1 + r) ** self.term - 1)) * self.amount * bias
        return installment.quantize(Decimal('.01'), rounding=ROUND_DOWN)
    
    def get_balance(self, date_base=datetime.now().astimezone(tz=timezone.utc)):
        try:
            payments = self.payment_set.filter(type='MD', date__lte=date_base).values('amount')
            return self.amount - sum([payment['amount'] for payment in payments])
        except:
            return Decimal('0')

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'


        def __repr__(self):
            return f'Loan(loan_id={self.loan_id}, amount={self.amount}, term={self.term}, rate={self.rate}, date={self.date_initial})'


class Payment(models.Model):
    """
    Payment Model
    Defines the attributes of a Payment
    """
    loan_id = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    PAYMENT_CHOICES = (('MD', 'Made'), ('MS', 'Missed'))
    status = models.CharField('Type', max_length=2, choices=PAYMENT_CHOICES, default='MD')
    date = models.DateTimeField('Date', auto_now=False, auto_now_add=False)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'


    def __repr__(self):
        return f'Payment(loan_id={self.loan_id}, type={self.status}, date={self.date}, amount={self.amount})'
