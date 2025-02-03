
from django.urls import path
from .views import UserRegister
from .views import UserLogin

urlpatterns = [
    path('user/register', UserRegister.as_view()),
    path('user/login', UserLogin.as_view()),
]