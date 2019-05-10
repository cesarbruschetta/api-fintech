from django.contrib.postgres.validators import RangeMinValueValidator
from django.db import models
from decimal import Decimal, ROUND_DOWN
from datetime import datetime, timezone
from django.forms import DecimalField
from django.core.validators import MaxValueValidator, MinValueValidator


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

    def get_history(self):
        pass


class Loan(models.Model):
    """
    Loan Model
    Defines the attributes of a loan
    """
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2,validators=[MinValueValidator(0.01)])
    term = models.IntegerField('Term', validators=[MinValueValidator(1)])
    rate = models.DecimalField('Rate', max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)])
    date_initial = models.DateTimeField('Date creation', auto_now=False, auto_now_add=False)

    def _instalment_adjustment(self):
        loans_history = self.client.loan_set.all()
        missed_payments = sum([Payment.objects.filter(loan_id=loan, status='MS').count() for loan in loans_history])
        if len(loans_history) > 1:
            existing_debt = sum([loans_history[i].get_balance() for i in range(len(loans_history)-1)])
            adjustment = 0
            if existing_debt == 0:
                if missed_payments == 0:
                    adjustment = -0.02
                elif 0 < missed_payments <= 3:
                    adjustment = 0.04
                return Decimal(adjustment)
        return Decimal(0)

    @property
    def instalment(self):
        r = self.rate / self.term
        instalment = (r + r / ((1 + r) ** self.term - 1)) * self.amount * (1 + self.instalment_adjustment())
        return instalment.quantize(Decimal('.01'), rounding=ROUND_DOWN)
    
    def get_balance(self, date_base=datetime.now().astimezone(tz=timezone.utc)):
        try:
            payments = self.payment_set.filter(status='MD', date__lte=date_base).values('amount')
            return self.amount - sum([payment['amount'] for payment in payments])
        except:
            return Decimal('0')

    def __repr__(self):
        return f'Loan(loan_id={self.id}, amount={self.amount}, term={self.term}, rate={self.rate}, date_initial={self.date_initial})'

    def __str__(self):
        return f'id: {self.pk} | {self.client}'


    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'


class Payment(models.Model):
    """
    Payment Model
    Defines the attributes of a Payment
    """
    PAYMENT_CHOICES = (('MD', 'Made'), ('MS', 'Missed'))

    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    status = models.CharField('Type', db_column='type', max_length=2, choices=PAYMENT_CHOICES, default='MD')
    date = models.DateTimeField('Date', auto_now=False, auto_now_add=False)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)

    def __repr__(self):
        return f'Payment(loan_id={self.loan_id}, type={self.status}, date={self.date}, amount={self.amount})' #555555555555555555555
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

