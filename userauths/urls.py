from django.urls import path
from . import views

app_name = "userauths"

urlpatterns = [
    path("sign-up", views.register_view, name="sign-up"),
    path("sign-in", views.login_view, name="login"),
    path("sing-out", views.logout_user, name="logout")
]
