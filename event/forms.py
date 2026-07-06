from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "event_date",
            "organized_by",
        ]