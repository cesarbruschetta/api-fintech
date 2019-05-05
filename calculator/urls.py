from django.urls import path

from .views import *

urlpatterns = [
    path('', loans),
    path('payments/', payments),
    path('balance/', balance),
]
