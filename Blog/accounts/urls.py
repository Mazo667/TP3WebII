from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("password_change/", views.CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
]