from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Department
from .forms import DepartmentForm


def department_list(request):

    departments = Department.objects.all().order_by("name")

    return render(
        request,
        "departments/department_list.html",
        {
            "departments": departments
        }
    )


def department_create(request):

    if request.method == "POST":

        form = DepartmentForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Department created successfully."
            )

            return redirect("department-list")

    else:

        form = DepartmentForm()

    return render(
        request,
        "departments/department_form.html",
        {
            "form": form
        }
    )


def department_detail(request, pk):

    department = get_object_or_404(
        Department,
        pk=pk
    )

    return render(
        request,
        "departments/department_detail.html",
        {
            "department": department
        }
    )


def department_update(request, pk):

    department = get_object_or_404(
        Department,
        pk=pk
    )

    if request.method == "POST":

        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Department updated successfully."
            )

            return redirect("department_list")

    else:

        form = DepartmentForm(
            instance=department
        )

    return render(
        request,
        "departments/department_form.html",
        {
            "form": form
        }
    )


def department_delete(request, pk):

    department = get_object_or_404(
        Department,
        pk=pk
    )

    if request.method == "POST":

        department.delete()

        messages.success(
            request,
            "Department deleted successfully."
        )

        return redirect("department-list")

    return render(
        request,
        "departments/department_confirm_delete.html",
        {
            "department": department
        }
    )