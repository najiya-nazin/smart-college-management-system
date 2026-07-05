from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Library
from .serializers import BookSerializer, LibrarySerializer


class BookListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        books = Book.objects.all().order_by("title")

        serializer = BookSerializer(
            books,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = BookSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class BookDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Book,
            pk=pk
        )

    def get(self, request, pk):

        book = self.get_object(pk)

        serializer = BookSerializer(book)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        book = self.get_object(pk)

        serializer = BookSerializer(
            book,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        book = self.get_object(pk)

        serializer = BookSerializer(
            book,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):

        book = self.get_object(pk)

        book.delete()

        return Response(
            {
                "message": "Book deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class LibraryListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        library = Library.objects.select_related(
            "student",
            "book"
        ).all().order_by("-issue_date")

        serializer = LibrarySerializer(
            library,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = LibrarySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class LibraryDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return get_object_or_404(
            Library.objects.select_related(
                "student",
                "book"
            ),
            pk=pk
        )

    def get(self, request, pk):

        library = self.get_object(pk)

        serializer = LibrarySerializer(library)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):

        library = self.get_object(pk)

        serializer = LibrarySerializer(
            library,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):

        library = self.get_object(pk)

        serializer = LibrarySerializer(
            library,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):

        library = self.get_object(pk)

        library.delete()

        return Response(
            {
                "message": "Library record deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )
