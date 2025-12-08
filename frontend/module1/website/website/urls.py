# website/urls.py
from django.contrib import admin
from django.urls import path
from signup.views import signaction
from login.views import loginaction

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signaction, name='home'),          # ← root now shows signup
    path('signup/', signaction, name='signup'),
    path('login/', loginaction, name='login'),
]
