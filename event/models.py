from django.db import models
from departments.models import Department


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_date = models.DateField()
    organized_by = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = "events"
        ordering = ["title"]


    def __str__(self):
        return self.name