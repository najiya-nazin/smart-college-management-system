from django.shortcuts import render, redirect, get_object_or_404
from .models import Timetable
from .forms import TimetableForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Create Timetable
def create_timetable(request):

    users = User.objects.filter(role="TEACHER")
    print(users)

    form = TimetableForm()

    if request.method == "POST":
        form = TimetableForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("timetable_list")

    return render(request, "timetables/create_timetable.html", {
        "form": form,
        "users":users,

    })


# List Timetables
def timetable_list(request):

    timetables = Timetable.objects.all()

    return render(request, "timetables/timetable_list.html", {
        "timetables": timetables
    })


# Timetable Detail
def timetable_detail(request, pk):

    timetable = get_object_or_404(Timetable, pk=pk)

    return render(request, "timetables/timetable_detail.html", {
        "timetable": timetable
    })


# Update Timetable
def update_timetable(request, pk):

    timetable = get_object_or_404(Timetable, pk=pk)

    form = TimetableForm(instance=timetable)

    if request.method == "POST":
        form = TimetableForm(request.POST, instance=timetable)

        if form.is_valid():
            form.save()
            return redirect("timetable_list")

    return render(request, "timetables/update_timetable.html", {
        "form": form
    })


# Delete Timetable
def delete_timetable(request, pk):

    timetable = get_object_or_404(Timetable, pk=pk)

    if request.method == "POST":
        timetable.delete()
        return redirect("timetable_list")

    return render(request, "timetables/delete_timetable.html", {
        "timetable": timetable
    })