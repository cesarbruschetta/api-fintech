from django.contrib import admin
from .models import Loan, Payment, Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "email", "phone", "cpf")


class LoanAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "amount", "term", "rate", "date_initial")


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "status", "date", "amount")


admin.site.register(Loan, LoanAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Client, ClientAdmin)
