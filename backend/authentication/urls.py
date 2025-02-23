
from django.urls import path
from .views import UserRegister
from .views import UserLogin

urlpatterns = [
    path('user/api/register', UserRegister.as_view()),
    path('user/api/login', UserLogin.as_view()),
    path('user/api/logout', UserLogout.as_view()),
]
