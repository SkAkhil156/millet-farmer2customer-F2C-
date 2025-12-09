from django.urls import path
from .views import loginaction, welcome

urlpatterns = [
    path('', loginaction, name='login'),   # matches /login/
    path('welcome/', welcome, name='welcome'),  # matches /login/welcome/ (or you can put welcome elsewhere)
]
