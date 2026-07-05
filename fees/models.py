from django.db import models
from students.models import Student


class FeeType(models.TextChoices):
    TUITION = "Tuition", "Tuition"
    EXAM = "Exam", "Exam"
    LIBRARY = "Library", "Library"
    HOSTEL = "Hostel", "Hostel"
    TRANSPORT = "Transport", "Transport"
    OTHER = "Other", "Other"


class PaymentStatus(models.TextChoices):
    PAID = "Paid", "Paid"
    PENDING = "Pending", "Pending"
    PARTIAL = "Partial", "Partial"


class Fee(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="fees"
    )

    semester = models.PositiveSmallIntegerField()

    fee_type = models.CharField(
        max_length=20,
        choices=FeeType.choices
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = "fees"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.student.student_id} - {self.fee_type}"
