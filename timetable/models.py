from django.db import models
from courses.models import Course
from teachers.models import Teacher


class Timetable(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="timetables"
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="timetables"
    )

    class_name = models.CharField(
        max_length=50
    )

    room_no = models.CharField(
        max_length=20
    )

    day = models.CharField(
        max_length=20
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    class Meta:
        db_table = "timetable"
        ordering = ["day", "start_time"]

    def __str__(self):
        return f"{self.class_name} - {self.day}"
