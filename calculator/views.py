from django.shortcuts import render

from .models import Loans


def loans(request):
    context = {
        'title': 'Loans API',
        'Loans': Loans.objects,
    }
    return render(request, 'calculator/loans.html', context)


def payments(request):
    pass


def balance(request):
    pass

