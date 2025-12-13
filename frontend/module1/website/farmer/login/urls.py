from django.urls import path
from .views import loginaction, welcome

app_name = "farmer_login"

urlpatterns = [
    path('', loginaction, name='login'),
    path('welcome/', welcome, name='welcome'),
]
