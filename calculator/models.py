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

    def __repr__(self):
        return f'Client(id={self.id}, name={self.name}, surname={self.surname}, email={self.email}, phone={self.phone}, cpf={self.cpf})'
        
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'



class Loan(models.Model):
    """
    Loan Model
    Defines the attributes of a loan
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)
    term = models.IntegerField('Term')
    rate = models.DecimalField('Rate', max_digits=15, decimal_places=2)
    date_initial = models.DateTimeField('Date creation', auto_now=False, auto_now_add=False)

   
    def client_payment_history(self):
        loans_history = self.client.loan_set.all()
        missed_payments = sum([Payment.objects.filter(loan_id=loan, status='MS').count() for loan in loans_history])
        debt = sum([loan.get_balance() for loan in loans_history])
        bias = 0 
        if debt == 0:
            if missed_payments == 0:
                bias = -0.02
            elif 0 < missed_payments <= 3:
                bias = 0.04
        return Decimal(bias)

    @property
    def installment(self):
        r = self.rate / self.term
        installment = (r + r / ((1 + r) ** self.term - 1)) * self.amount * (1 + self.client_payment_history())
        return installment.quantize(Decimal('.01'), rounding=ROUND_DOWN)
    
    def get_balance(self, date_base=datetime.now().astimezone(tz=timezone.utc)):
        try:
            payments = self.payment_set.filter(status='MD', date__lte=date_base).values('amount')
            return self.amount - sum([payment['amount'] for payment in payments])
        except:
            return Decimal('0')

    def __repr__(self):
        return f'Loan(loan_id={self.id}, amount={self.amount}, term={self.term}, rate={self.rate}, date_initial={self.date_initial})'

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'


class Payment(models.Model):
    """
    Payment Model
    Defines the attributes of a Payment
    """
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    PAYMENT_CHOICES = (('MD', 'Made'), ('MS', 'Missed'))
    status = models.CharField('Type', db_column='type', max_length=2, choices=PAYMENT_CHOICES, default='MD')
    date = models.DateTimeField('Date', auto_now=False, auto_now_add=False)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)

    def __repr__(self):
        return f'Payment(loan_id={self.loan_id}, type={self.status}, date={self.date}, amount={self.amount})'
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

