from django.db import models
from courses.models import Course


class Exam(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_date = models.DateField()
    total_marks = models.IntegerField()

    class Meta:
        db_table = "exams"
        ordering = ["name"]

    def __str__(self):
        return self.name