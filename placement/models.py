from django.db import models
from students.models import Student


class Company(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True
    )

    location = models.CharField(
        max_length=150
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    class Meta:
        db_table = "company"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PlacementStatus(models.TextChoices):
    PLACED = "Placed", "Placed"
    PENDING = "Pending", "Pending"
    REJECTED = "Rejected", "Rejected"


class Placement(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="placements"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="placements"
    )

    job_role = models.CharField(
        max_length=100
    )

    package = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    placement_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=PlacementStatus.choices,
        default=PlacementStatus.PLACED
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = "placements"
        ordering = ["-placement_date"]

    def __str__(self):
        return f"{self.student.student_id} - {self.company.name}"
