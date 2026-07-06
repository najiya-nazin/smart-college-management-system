from rest_framework import serializers
from .models import Timetable


class TimetableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timetable
        fields = [
            "id",
            "course",
            "teacher",
            "class_name",
            "room_no",
            "day",
            "start_time",
            "end_time",
        ]

        extra_kwargs = {
            "course": {"required": True},
            "teacher": {"required": True},
            "class_name": {"required": True},
            "room_no": {"required": True},
            "day": {"required": True},
            "start_time": {"required": True},
            "end_time": {"required": True},
        }