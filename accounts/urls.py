from django.urls import path
from . import views

urlpatterns = [

    path("", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot-password",),
    path("verify-otp/", views.verify_otp, name="verify-otp",),
    path("reset-password/", views.reset_password, name="reset-password",),
    path("logout_view/", views.logout_view, name="logout_view"),


]
