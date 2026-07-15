from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Fee
from .forms import FeeForm


# List Fees
def fee_list(request):

    fees = Fee.objects.select_related(
        "student",
        "student__user"
    ).all().order_by("-payment_date")

    return render(
        request,
        "fees/fee_list.html",
        {
            "fees": fees
        }
    )


# Create Fee
def fee_create(request):

    if request.method == "POST":

        form = FeeForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee record created successfully."
            )

            return redirect("fee-list")

    else:

        form = FeeForm()

    return render(
        request,
        "fees/fee_form.html",
        {
            "form": form
        }
    )


# Fee Detail
def fee_detail(request, pk):

    fee = get_object_or_404(
        Fee.objects.select_related(
            "student",
            "student__user"
        ),
        pk=pk
    )

    return render(
        request,
        "fees/fee_detail.html",
        {
            "fee": fee
        }
    )


# Update Fee
def fee_update(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk
    )

    if request.method == "POST":

        form = FeeForm(
            request.POST,
            instance=fee
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee record updated successfully."
            )

            return redirect("fee-list")

    else:

        form = FeeForm(instance=fee)

    return render(
        request,
        "fees/fee_form.html",
        {
            "form": form
        }
    )


# Delete Fee
def fee_delete(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk
    )

    if request.method == "POST":

        fee.delete()

        messages.success(
            request,
            "Fee record deleted successfully."
        )

    return redirect("fee-list")


@login_required
def fee_receipt(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk,
        student__user=request.user
    )

    fee.balance = fee.amount - fee.paid_amount

    return render(
        request,
        "fees/fee_receipt.html",
        {
            "fee": fee
        }
    )