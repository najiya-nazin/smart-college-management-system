from django.db import models
from students.models import Student


class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.CharField(max_length=150)

    publisher = models.CharField(max_length=150)

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    class Meta:
        db_table = "books"
        ordering = ["title"]

    def __str__(self):
        return self.title


class LibraryStatus(models.TextChoices):
    ISSUED = "Issued", "Issued"
    RETURNED = "Returned", "Returned"


class Library(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT
    )

    issue_date = models.DateField()

    due_date = models.DateField()

    return_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=LibraryStatus.choices,
        default=LibraryStatus.ISSUED
    )

    fine = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = "library"
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.student.student_id} - {self.book.title}"