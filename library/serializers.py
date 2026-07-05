from rest_framework import serializers
from .models import Book, Library


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "isbn",
        ]


class LibrarySerializer(serializers.ModelSerializer):

    student_name = serializers.ReadOnlyField(
        source="student.user.name"
    )

    book_title = serializers.ReadOnlyField(
        source="book.title"
    )

    class Meta:
        model = Library
        fields = [
            "id",
            "student",
            "student_name",
            "book",
            "book_title",
            "issue_date",
            "due_date",
            "return_date",
            "status",
            "fine",
            "remarks",
        ]