from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Event
from .forms import EventForm


# List Events
def event_list(request):

    events = Event.objects.select_related(
        "organized_by"
    ).all()

    return render(
        request,
        "events/event_list.html",
        {
            "events": events
        }
    )


# Create Event
def event_create(request):

    if request.method == "POST":

        form = EventForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event created successfully."
            )

            return redirect("event-list")

    else:

        form = EventForm()

    return render(
        request,
        "events/event_form.html",
        {
            "form": form
        }
    )


# Event Detail
def event_detail(request, pk):

    event = get_object_or_404(
        Event.objects.select_related("organized_by"),
        pk=pk
    )

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event
        }
    )


# Update Event
def event_update(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk
    )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            instance=event
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event updated successfully."
            )

            return redirect("event-list")

    else:

        form = EventForm(
            instance=event
        )

    return render(
        request,
        "events/event_form.html",
        {
            "form": form
        }
    )


# Delete Event
def event_delete(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk
    )

    if request.method == "POST":

        event.delete()

        messages.success(
            request,
            "Event deleted successfully."
        )

        return redirect("event-list")

    return render(
        request,
        "events/event_confirm_delete.html",
        {
            "event": event
        }
    )