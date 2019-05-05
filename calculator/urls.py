from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^v1/loans/$',
        views.post_loan,
        name='post_loan'
    )
]