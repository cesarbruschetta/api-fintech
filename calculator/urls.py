from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^v1/loans/$',
        views.post_loans,
        name='post_loans'
    ),
    url(
        r'^v1/loans/(?P<pk>[0-9]+)/payments$',
        views.post_payments,
        name='post_payments'
    ),
]