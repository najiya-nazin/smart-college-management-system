from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm


# Create Student
def student_create(request):

    form = StudentForm()

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    return render(request, "students/student_create.html", {
        "form": form
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
def student_update(request, pk):

    student = get_object_or_404(Student, pk=pk)

    form = StudentForm(instance=student)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    return render(request, "students/student_update.html", {
        "form": form
    })


# Delete Student
def student_delete(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(request, "students/student_delete.html", {
        "student": student
    })