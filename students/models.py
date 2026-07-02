from django.db import models
from accounts.models import User
from departments.models import Department
from courses.models import Course


class Gender(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    OTHER = "Other", "Other"


class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student"
    )

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="students"
    )

    semester = models.PositiveSmallIntegerField()

    dob = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )

    address = models.TextField()

    admission_date = models.DateField()

    guardian_name = models.CharField(
        max_length=150
    )

    guardian_phone = models.CharField(
        max_length=15
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "students"
        ordering = ["student_id"]

    def __str__(self):
        return f"{self.student_id} - {self.user.name}"




