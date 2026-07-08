from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Hostel, HostelRoom
from .forms import HostelForm, HostelRoomForm


def hostel_list(request):

    hostels = Hostel.objects.all()

    return render(
        request,
        "hostel/hostel_list.html",
        {
            "hostels": hostels
        }
    )


def hostel_create(request):

    if request.method == "POST":

        form = HostelForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Hostel created successfully.")

            return redirect("hostel-list")

    else:

        form = HostelForm()

    return render(
        request,
        "hostel/hostel_form.html",
        {
            "form": form
        }
    )


def hostel_detail(request, pk):

    hostel = get_object_or_404(
        Hostel,
        pk=pk
    )

    return render(
        request,
        "hostel/hostel_detail.html",
        {
            "hostel": hostel
        }
    )


def hostel_update(request, pk):

    hostel = get_object_or_404(
        Hostel,
        pk=pk
    )

    if request.method == "POST":

        form = HostelForm(
            request.POST,
            instance=hostel
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Hostel updated successfully.")

            return redirect("hostel-list")

    else:

        form = HostelForm(instance=hostel)

    return render(
        request,
        "hostel/hostel_form.html",
        {
            "form": form
        }
    )


def hostel_delete(request, pk):

    hostel = get_object_or_404(
        Hostel,
        pk=pk
    )

    if request.method == "POST":

        hostel.delete()

    return redirect("hostel-list")


def room_list(request):

    rooms = HostelRoom.objects.select_related("hostel").all()

    return render(
        request,
        "hostel/room_list.html",
        {
            "rooms": rooms
        }
    )


def room_create(request):

    if request.method == "POST":

        form = HostelRoomForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Room created successfully.")

            return redirect("room-list")

    else:

        form = HostelRoomForm()

    return render(
        request,
        "hostel/room_form.html",
        {
            "form": form
        }
    )


def room_detail(request, pk):

    room = get_object_or_404(
        HostelRoom.objects.select_related("hostel"),
        pk=pk
    )

    return render(
        request,
        "hostel/room_detail.html",
        {
            "room": room
        }
    )


def room_update(request, pk):

    room = get_object_or_404(
        HostelRoom,
        pk=pk
    )

    if request.method == "POST":

        form = HostelRoomForm(
            request.POST,
            instance=room
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Room updated successfully.")

            return redirect("room-list")

    else:

        form = HostelRoomForm(instance=room)

    return render(
        request,
        "hostel/room_form.html",
        {
            "form": form
        }
    )


def room_delete(request, pk):

    room = get_object_or_404(
        HostelRoom,
        pk=pk
    )

    if request.method == "POST":

        room.delete()

    return redirect("room-list")