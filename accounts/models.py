from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None, **extra_fields):

        extra_fields.setdefault("role", Role.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email=email,
            name=name,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.STUDENT,db_index=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.role})"

    class Meta:
        ordering = ["name"]