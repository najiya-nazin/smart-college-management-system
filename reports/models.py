from django.db import models
from accounts.models import User

# Create your models here.

class Report(models.Model):
    report_type = models.CharField(max_length=50)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/')

    class Meta:
        db_table = "reports"
        ordering = ["report_type"]

    def __str__(self):
        return self.report_type
    