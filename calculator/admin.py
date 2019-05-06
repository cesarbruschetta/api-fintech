from django.contrib import admin

# Register your models here.
from .models import Payment, Loan

admin.site.register(Payment)
admin.site.register(Loan)