import random

from django.core.cache import cache
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ForgotPasswordSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer
)


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Registration Successful"
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                }
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "message": "Logout Successful"
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {
                    "error": "Invalid or Expired Refresh Token"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ForgotPasswordView(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        otp = str(random.randint(100000, 999999))

        cache.set(email, otp, timeout=300)

        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP is {otp}",
            from_email=None,
            recipient_list=[email],
            fail_silently=False
        )

        return Response(
            {
                "message": "OTP sent successfully"
            },
            status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        saved_otp = cache.get(email)

        if saved_otp != otp:
            return Response(
                {
                    "error": "Invalid OTP"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "OTP Verified Successfully"
            },
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        saved_otp = cache.get(email)

        if saved_otp != otp:
            return Response(
                {
                    "error": "Invalid OTP"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(email=email)

        user.set_password(serializer.validated_data["password"])
        user.save()

        cache.delete(email)

        return Response(
            {
                "message": "Password Reset Successfully"
            },
            status=status.HTTP_200_OK
        )