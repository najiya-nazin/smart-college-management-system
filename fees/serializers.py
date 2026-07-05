from rest_framework import serializers
from .models import Fee


class FeeSerializer(serializers.ModelSerializer):

    student_name = serializers.ReadOnlyField(
        source="student.user.name"
    )

    class Meta:
        model = Fee
        fields = [
            "id",
            "student",
            "student_name",
            "semester",
            "fee_type",
            "amount",
            "paid_amount",
            "payment_date",
            "status",
            "remarks",
        ]
