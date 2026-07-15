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


        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "event_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "organized_by": forms.Select(attrs={
                "class": "form-select"
            }),
        }