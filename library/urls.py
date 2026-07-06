from django.urls import path
from . import views

urlpatterns = [


    path(
        "books/",
        views.book_list,
        name="book-list"
    ),

    path(
        "books/create/",
        views.book_create,
        name="book-create"
    ),

    path(
        "books/<int:pk>/",
        views.book_detail,
        name="book-detail"
    ),

    path(
        "books/<int:pk>/edit/",
        views.book_update,
        name="book-update"
    ),

    path(
        "books/<int:pk>/delete/",
        views.book_delete,
        name="book-delete"
    ),


    path(
        "",
        views.library_list,
        name="library-list"
    ),

    path(
        "create/",
        views.library_create,
        name="library-create"
    ),

    path(
        "<int:pk>/",
        views.library_detail,
        name="library-detail"
    ),

    path(
        "<int:pk>/edit/",
        views.library_update,
        name="library-update"
    ),

    path(
        "<int:pk>/delete/",
        views.library_delete,
        name="library-delete"
    ),

]