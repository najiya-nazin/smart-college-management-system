from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from .forms import TeacherForm


# Create Teacher
def add_teacher(request):
    form = TeacherForm()

    if request.method == "POST":
        form = TeacherForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("teacher_list")

    return render(request, "teacher/add_teacher.html", {
        "form": form
    })


# List Teachers
def teacher_list(request):
    teachers = Teacher.objects.all()

    return render(request, "teacher/teacher_list.html", {
        "teachers": teachers
    })


# Teacher Detail
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    return render(request, "teacher/teacher_detail.html", {
        "teacher": teacher
    })


# Update Teacher
def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    form = TeacherForm(instance=teacher)

    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)

        if form.is_valid():
            form.save()
            return redirect("teacher_list")

    return render(request, "teacher/edit_teacher.html", {
        "form": form
    })


# Delete Teacher
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        teacher.delete()
        return redirect("teacher_list")

    return render(request, "teacher/delete_teacher.html", {
        "teacher": teacher
    })