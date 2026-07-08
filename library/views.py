from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Book, Library
from .forms import BookForm, LibraryForm


def book_list(request):

    books = Book.objects.all().order_by("title")

    return render(
        request,
        "library/book_list.html",
        {
            "books": books
        }
    )


def book_create(request):

    if request.method == "POST":

        form = BookForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Book added successfully."
            )

            return redirect("book-list")

    else:

        form = BookForm()

    return render(
        request,
        "library/book_form.html",
        {
            "form": form
        }
    )


def book_detail(request, pk):

    book = get_object_or_404(Book, pk=pk)

    return render(
        request,
        "library/book_detail.html",
        {
            "book": book
        }
    )


def book_update(request, pk):

    book = get_object_or_404(
        Book,
        pk=pk
    )

    if request.method == "POST":

        form = BookForm(
            request.POST,
            instance=book
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Book updated successfully."
            )

            return redirect("book-list")

    else:

        form = BookForm(
            instance=book
        )

    return render(
        request,
        "library/book_form.html",
        {
            "form": form
        }
    )


def book_delete(request, pk):

    book = get_object_or_404(
        Book,
        pk=pk
    )

    if request.method == "POST":

        book.delete()

    return redirect("book-list")


def library_list(request):

    library = Library.objects.select_related(
        "student",
        "book"
    ).all().order_by("-issue_date")

    return render(
        request,
        "library/library_list.html",
        {
            "library": library
        }
    )


def library_create(request):

    if request.method == "POST":

        form = LibraryForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Book issued successfully."
            )

            return redirect("library-list")

    else:

        form = LibraryForm()

    return render(
        request,
        "library/library_form.html",
        {
            "form": form
        }
    )


def library_detail(request, pk):

    library = get_object_or_404(
        Library.objects.select_related(
            "student",
            "book"
        ),
        pk=pk
    )

    return render(
        request,
        "library/library_detail.html",
        {
            "library": library
        }
    )


def library_update(request, pk):

    library = get_object_or_404(
        Library,
        pk=pk
    )

    if request.method == "POST":

        form = LibraryForm(
            request.POST,
            instance=library
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Library record updated successfully."
            )

            return redirect("library-list")

    else:

        form = LibraryForm(
            instance=library
        )

    return render(
        request,
        "library/library_form.html",
        {
            "form": form
        }
    )


def library_delete(request, pk):

    library = get_object_or_404(
        Library,
        pk=pk
    )

    if request.method == "POST":

        library.delete()

    return redirect("library-list")