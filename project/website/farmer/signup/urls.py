from django.urls import path
from .views import signaction

app_name = "farmer_signup"

urlpatterns = [
    path('', signaction, name='signup'),
]
