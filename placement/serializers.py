from rest_framework import serializers

from .models import Company, Placement


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "location",
            "website",
            "email",
            "phone",
        ]


class PlacementSerializer(serializers.ModelSerializer):

    student_name = serializers.ReadOnlyField(
        source="student.user.name"
    )

    company_name = serializers.ReadOnlyField(
        source="company.name"
    )

    class Meta:
        model = Placement
        fields = [
            "id",
            "student",
            "student_name",
            "company",
            "company_name",
            "job_role",
            "package",
            "placement_date",
            "status",
            "remarks",
        ]