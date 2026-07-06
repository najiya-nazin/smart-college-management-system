from django import forms
from .models import Fee


class FeeForm(forms.ModelForm):

    class Meta:
        model = Fee
        fields = [
            "student",
            "semester",
            "fee_type",
            "amount",
            "paid_amount",
            "payment_date",
            "status",
            "remarks",
        ]