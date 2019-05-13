from django.urls import path
from . import views


urlpatterns = [
    path('v1/clients/', views.post_clients, name='post_clients'),
    path('v1/loans/', views.post_loans, name='post_loans'),
    path('v1/loans/<int:pk>/payments', views.post_payments, name='post_payments'),
    path('v1/loans/<int:pk>/balance', views.get_balance, name='get_balance'),
]