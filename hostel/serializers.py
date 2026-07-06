from rest_framework import serializers
from .models import Hostel, HostelRoom


class HostelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hostel
        fields = [
            "id",
            "name",
            "location",
            "total_rooms",
        ]


class HostelRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = HostelRoom
        fields = [
            "id",
            "hostel",
            "room_no",
            "capacity",
            "current_occupancy",
        ]