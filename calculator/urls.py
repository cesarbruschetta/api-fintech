from django.urls import path, re_path
from . import views


urlpatterns = [
    path('v1/clients/', views.clients, name='clients'),
    path('v1/loans/', views.loans, name='loans'),
    re_path(r'^v1/loans/(?P<pk>[0-9]{3}-[0-9]{4}-[0-9]{4}-[0-9]{4})/payments$', views.payments, name='payments'),
    re_path(r'^v1/loans/(?P<pk>[0-9]{3}-[0-9]{4}-[0-9]{4}-[0-9]{4})/balance$', views.balance, name='balance'),
]