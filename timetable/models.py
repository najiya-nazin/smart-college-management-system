from django.db import models
from courses.models import Course
from teachers.models import Teacher


class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class_name = models.CharField(max_length=50)
    room_no = models.CharField(max_length=20)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()