from django.contrib import admin
from .models import Loan, Payment

admin.site.register(Loan)
admin.site.register(Payment)
