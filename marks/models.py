from django.db import models
from students.models import Student
from courses.models import Course

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField()
    grade = models.CharField(max_length=5)


    def __str__(self):
        return self.name

    
