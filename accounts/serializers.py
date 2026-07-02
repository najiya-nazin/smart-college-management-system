from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "role",
            "password",
            "confirm_password"
        )

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop("confirm_password")

        password = validated_data.pop("password")

        user     = User.objects.create(**validated_data)

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):

    email    = serializers.EmailField()

    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        user = authenticate(
            email=attrs["email"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user

        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):

    email            = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):

    email            = serializers.EmailField()

    otp              = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):

    email            = serializers.EmailField()

    otp              = serializers.CharField(max_length=6)

    password         = serializers.CharField(min_length=8)

    confirm_password = serializers.CharField()

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )

        return attrs