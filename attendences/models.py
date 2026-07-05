from django.db import models
from students.models import Student


class AttendanceStatus(models.TextChoices):
    PRESENT = "Present", "Present"
    ABSENT = "Absent", "Absent"
    LATE = "Late", "Late"


class Attendance(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-date"]
        unique_together = ("student", "date")

    def __str__(self):
        return f"{self.student.student_id} - {self.date}"
