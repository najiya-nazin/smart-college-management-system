from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'code',
            'department',
            'duration',
            'description',
        ]
        

        extra_kwargs = {
            'name': {'required': True},
            'code': {'required': True},
            'department': {'required': True},
            'duration': {'required': True},
            'description': {'required': True},
        }