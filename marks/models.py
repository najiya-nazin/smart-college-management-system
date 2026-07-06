from django.db import models
from students.models import Student
from courses.models import Course


class Marks(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    marks_obtained = models.PositiveIntegerField()

    max_marks = models.PositiveIntegerField()

    grade = models.CharField(max_length=5)

    class Meta:
        db_table = "marks"
        ordering = ["-marks_obtained"]
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} - {self.course}"
