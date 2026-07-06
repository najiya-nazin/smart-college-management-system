from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Exam
from .forms import ExamForm


# List Exams
def exam_list(request):

    exams = Exam.objects.select_related("course").all()

    return render(
        request,
        "exams/exam_list.html",
        {
            "exams": exams
        }
    )


# Create Exam
def exam_create(request):

    if request.method == "POST":

        form = ExamForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam created successfully."
            )

            return redirect("exam-list")

    else:

        form = ExamForm()

    return render(
        request,
        "exams/exam_form.html",
        {
            "form": form
        }
    )


# Exam Detail
def exam_detail(request, pk):

    exam = get_object_or_404(
        Exam.objects.select_related("course"),
        pk=pk
    )

    return render(
        request,
        "exams/exam_detail.html",
        {
            "exam": exam
        }
    )


# Update Exam
def exam_update(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk
    )

    if request.method == "POST":

        form = ExamForm(
            request.POST,
            instance=exam
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam updated successfully."
            )

            return redirect("exam-list")

    else:

        form = ExamForm(instance=exam)

    return render(
        request,
        "exams/exam_form.html",
        {
            "form": form
        }
    )


# Delete Exam
def exam_delete(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk
    )

    if request.method == "POST":

        exam.delete()

        messages.success(
            request,
            "Exam deleted successfully."
        )

        return redirect("exam-list")

    return render(
        request,
        "exams/exam_confirm_delete.html",
        {
            "exam": exam
        }
    )