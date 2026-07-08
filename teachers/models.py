from django.db import models
from departments.models import Department
from accounts.models import User

class Teacher(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="teachers"
    )

    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "teachers"
        ordering = ["user__name"]

    def __str__(self):
        return self.user.name