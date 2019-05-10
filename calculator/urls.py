from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^v1/loans/$',
        views.LoanView.as_view(),
        name='post_loans'
    ),
    url(
        r'^v1/loans/(?P<pk>[0-9]+)/payments$',
        views.PaymentView.as_view(),
        name='post_payments'
    ),
    url(
        r'^v1/loans/(?P<pk>[0-9]+)/balance$',
        views.get_balance,
        name='get_balance'
    ),
]