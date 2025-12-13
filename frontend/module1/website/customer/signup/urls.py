from django.urls import path
from .views import signaction

app_name = "customer_signup"

urlpatterns = [
    path('', signaction, name='signup'),
]
