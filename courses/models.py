from django.db import models
from departments.models import Department


class Course(models.Model):

    name = models.CharField(max_length=100)

    code = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    duration = models.CharField(max_length=50)

    description = models.TextField()

    class Meta:
        db_table = "courses"
        ordering = ["name"]

    def __str__(self):
        return self.name