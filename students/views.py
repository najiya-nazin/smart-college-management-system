from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import StudentCreateForm, StudentUpdateForm
from .models import Student
from departments.models import Department
from courses.models import Course


User = get_user_model()


def student_create(request):

    if request.method == "POST":
        form = StudentCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentCreateForm()

    return render(
        request,
        "students/student_create.html",
        {
            "form": form,
            "departments": Department.objects.all(),
            "courses": Course.objects.all(),
        },
    )

# List Students
def student_list(request):

    students = Student.objects.select_related(
        "user",
        "department"
    ).prefetch_related(
        "course"
    ).all().order_by("student_id")

    return render(request, "students/student_list.html", {
        "students": students
    })


# Student Detail
def student_detail(request, pk):

    student = get_object_or_404(
        Student.objects.select_related(
            "user",
            "department"
        ),
        pk=pk
    )

    return render(request, "students/student_detail.html", {
        "student": student
    })


def student_update(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentUpdateForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, "students/student_update.html", {
        "form": form
    })

# Delete Student
# def student_delete(request, pk):

#     student = get_object_or_404(Student, pk=pk)

#     if request.method == "POST":
#         student.delete()
#         return redirect("student_list")

#     return render(request, "students/student_delete.html", {
#         "student": student
#     })

# def student_delete(request, pk):
#     student = get_object_or_404(Student, pk=pk)

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)


#     if request.method == "POST":
#         user = student.user
#         user.delete()      
#         return redirect("student_list")

#     return render(request, "students/student_delete.html", {
#         "student": student
#     })

