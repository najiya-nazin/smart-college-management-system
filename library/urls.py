from django.urls import path

from .views import (
    BookListCreateAPIView,
    BookDetailAPIView,
    LibraryListCreateAPIView,
    LibraryDetailAPIView,
)

urlpatterns = [

    path(
        "books/",
        BookListCreateAPIView.as_view(),
        name="book-list-create"
    ),

    path(
        "books/<int:pk>/",
        BookDetailAPIView.as_view(),
        name="book-detail"
    ),

    path(
        "library/",
        LibraryListCreateAPIView.as_view(),
        name="library-list-create"
    ),

    path(
        "library/<int:pk>/",
        LibraryDetailAPIView.as_view(),
        name="library-detail"
    ),
]