from django.urls import path
from . import views


urlpatterns = [
    path('v1/clients/', views.clients, name='clients'),
    path('v1/loans/', views.loans, name='loans'),
    path('v1/loans/<int:pk>/payments', views.payments, name='payments'),
    path('v1/loans/<int:pk>/balance', views.balance, name='balance'),
]
