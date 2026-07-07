from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Course
from .forms import CourseForm


# List all courses
def course_list(request):

    courses = Course.objects.select_related(
        "department"
    ).all().order_by("name")

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses
        }
    )


# Create a new course
def course_create(request):

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Course added successfully.")

            return redirect("course-list")

    else:

        form = CourseForm()

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form
        }
    )


# View course details
def course_detail(request, pk):

    course = get_object_or_404(
        Course.objects.select_related("department"),
        pk=pk
    )

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course
        }
    )


# Update course
def course_update(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Course updated successfully.")

            return redirect("course-list")

    else:

        form = CourseForm(instance=course)

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form
        }
    )


# Delete course
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Course


def course_delete(request, pk):

    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":

        course.delete()

        messages.success(request, "Course deleted successfully.")

        return redirect("course-list")

    return redirect("course-list")