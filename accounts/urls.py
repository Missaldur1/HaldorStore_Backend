from django.urls import path
from .views import RegisterView, LoginView, user_profile, change_password

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # Funciones edit accounts
    path("user/", user_profile, name="user"),
    path("change-password/", change_password, name="change-password"),
]