from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendance
from .forms import AttendanceForm


# Create Attendance
def attendance_create(request):

    form = AttendanceForm()

    if request.method == "POST":
        form = AttendanceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("attendance_list")

    return render(request, "attendance_create.html", {
        "form": form
    })


# List Attendance
def attendance_list(request):

    attendance = Attendance.objects.select_related(
        "student"
    ).all().order_by("-date")

    return render(request, "attendance_list.html", {
        "attendance": attendance
    })


# Attendance Detail
def attendance_detail(request, pk):

    attendance = get_object_or_404(
        Attendance.objects.select_related("student"),
        pk=pk
    )

    return render(request, "attendance_detail.html", {
        "attendance": attendance
    })


# Update Attendance
def attendance_update(request, pk):

    attendance = get_object_or_404(Attendance, pk=pk)

    form = AttendanceForm(instance=attendance)

    if request.method == "POST":
        form = AttendanceForm(
            request.POST,
            instance=attendance
        )

        if form.is_valid():
            form.save()
            return redirect("attendance_list")

    return render(request, "attendance_update.html", {
        "form": form
    })


# Delete Attendance
def attendance_delete(request, pk):

    attendance = get_object_or_404(Attendance, pk=pk)

    if request.method == "POST":
        attendance.delete()
        return redirect("attendance_list")

    return render(request, "attendance_delete.html", {
        "attendance": attendance
    })