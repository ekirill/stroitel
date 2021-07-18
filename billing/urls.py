from django.urls import path

from billing.views import billing


urlpatterns = [
    path('', billing, name='billing'),
]
