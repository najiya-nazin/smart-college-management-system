from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Marks
from .forms import MarksForm


# List Marks
def marks_list(request):

    marks = Marks.objects.select_related(
        "student",
        "course"
    ).all()

    return render(
        request,
        "marks/marks_list.html",
        {
            "marks": marks
        }
    )


# Create Marks
def marks_create(request):

    if request.method == "POST":

        form = MarksForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Marks added successfully."
            )

            return redirect("marks-list")

    else:

        form = MarksForm()

    return render(
        request,
        "marks/marks_form.html",
        {
            "form": form
        }
    )


# Marks Detail
def marks_detail(request, pk):

    marks = get_object_or_404(
        Marks.objects.select_related(
            "student",
            "course"
        ),
        pk=pk
    )

    return render(
        request,
        "marks/marks_detail.html",
        {
            "marks": marks
        }
    )


# Update Marks
def marks_update(request, pk):

    marks = get_object_or_404(
        Marks,
        pk=pk
    )

    if request.method == "POST":

        form = MarksForm(
            request.POST,
            instance=marks
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Marks updated successfully."
            )

            return redirect("marks-list")

    else:

        form = MarksForm(
            instance=marks
        )

    return render(
        request,
        "marks/marks_form.html",
        {
            "form": form
        }
    )


# Delete Marks
def marks_delete(request, pk):

    marks = get_object_or_404(
        Marks,
        pk=pk
    )

    if request.method == "POST":

        marks.delete()

        messages.success(
            request,
            "Marks deleted successfully."
        )

        return redirect("marks-list")

    return render(
        request,
        "marks/marks_confirm_delete.html",
        {
            "marks": marks
        }
    )