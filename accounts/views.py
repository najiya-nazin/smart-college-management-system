import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login
from django.core.cache import cache
from django.core.mail import send_mail
from .models import User
from .forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    VerifyOTPForm,
    ResetPasswordForm,
)


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Registration Successful")

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def login_view(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            update_last_login(None, user)

            messages.success(request, "Login Successful")

            return redirect("admin_dashboard")

    else:

        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )


@login_required
def admin_dashboard(request):

    return render(
        request,
        "accounts/admin_dashboard.html",
    )


@login_required
def logout_view(request):

    logout(request)

    messages.success(request, "Logout Successful")

    return redirect("login")


def forgot_password(request):

    if request.method == "POST":

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            try:
                User.objects.get(email=email)

            except User.DoesNotExist:

                messages.error(request, "User not found")

                return redirect("forgot-password")

            otp = str(random.randint(100000, 999999))

            cache.set(email, otp, timeout=300)

            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP is {otp}",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "OTP Sent Successfully")

            return redirect("verify-otp")

    else:

        form = ForgotPasswordForm()

    return render(
        request,
        "accounts/forgot_password.html",
        {"form": form},
    )


def verify_otp(request):

    if request.method == "POST":

        form = VerifyOTPForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            otp = form.cleaned_data["otp"]

            saved_otp = cache.get(email)

            if saved_otp != otp:

                messages.error(request, "Invalid OTP")

                return redirect("verify-otp")

            messages.success(request, "OTP Verified Successfully")

            return redirect("reset-password")

    else:

        form = VerifyOTPForm()

    return render(
        request,
        "accounts/verify_otp.html",
        {"form": form},
    )


def reset_password(request):

    if request.method == "POST":

        form = ResetPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            otp = form.cleaned_data["otp"]

            saved_otp = cache.get(email)

            if saved_otp != otp:

                messages.error(request, "Invalid OTP")

                return redirect("reset-password")

            user = User.objects.get(email=email)

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            cache.delete(email)

            messages.success(
                request,
                "Password Reset Successfully"
            )

            return redirect("login")

    else:

        form = ResetPasswordForm()

    return render(
        request,
        "accounts/reset_password.html",
        {"form": form},
    )
