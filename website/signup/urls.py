from django.urls import path
from .views import signaction

urlpatterns = [
    path('', signaction, name='signup'),   # matches /signup/
]
