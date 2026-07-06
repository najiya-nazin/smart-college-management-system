from django import forms
from django.contrib.auth import authenticate
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "phone",
            "role",
            "password",
            "confirm_password",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(
            email=email,
            password=password
        )

        if not user:
            raise forms.ValidationError(
                "Invalid email or password."
            )

        self.user = user

        return cleaned_data

    def get_user(self):
        return self.user


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class VerifyOTPForm(forms.Form):
    email = forms.EmailField()

    otp = forms.CharField(
        max_length=6
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

    otp = forms.CharField(
        max_length=6
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data