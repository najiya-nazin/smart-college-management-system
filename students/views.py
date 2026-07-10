from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .forms import StudentForm
from .models import Student
from departments.models import Department
from courses.models import Course
from django.contrib.auth.decorators import login_required

User = get_user_model()


def student_create(request):

    users = User.objects.filter(role="STUDENT")
    departments = Department.objects.all()
    courses = Course.objects.all()

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "students/student_create.html", {
        "form": form,
        "users": users,
        "departments": departments,
        "courses": courses,
    })


# List Students
def student_list(request):

    students = Student.objects.select_related(
        "user",
        "department",
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
            "department",
            "course"
        ),
        pk=pk
    )

    return render(request, "students/student_detail.html", {
        "student": student
    })


# Update Student
# def student_update(request, pk):

#     student = get_object_or_404(Student, pk=pk)

#     form = StudentForm(instance=student)

#     if request.method == "POST":
#         form = StudentForm(request.POST, instance=student)

#         if form.is_valid():
#             form.save()
#             return redirect("student_list")

#     return render(request, "students/student_update.html", {
#         "form": form
#     })


def student_update(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

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

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        user = student.user
        user.delete()      
        return redirect("student_list")

    return render(request, "students/student_delete.html", {
        "student": student
    })


@login_required
def student_dashboard(request):



    return render(
        request,
        "students/student_dashboard.html",
        
    )