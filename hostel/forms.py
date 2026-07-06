from django import forms
from .models import Hostel, HostelRoom


class HostelForm(forms.ModelForm):

    class Meta:
        model = Hostel
        fields = [
            "name",
            "location",
            "total_rooms",
        ]


class HostelRoomForm(forms.ModelForm):

    class Meta:
        model = HostelRoom
        fields = [
            "hostel",
            "room_no",
            "capacity",
            "current_occupancy",
        ]