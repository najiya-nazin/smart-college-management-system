from django import forms
from .models import Book, Library


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "publisher",
            "isbn",
        ]


class LibraryForm(forms.ModelForm):

    class Meta:
        model = Library
        fields = [
            "student",
            "book",
            "issue_date",
            "due_date",
            "return_date",
            "status",
            "fine",
            "remarks",
        ]