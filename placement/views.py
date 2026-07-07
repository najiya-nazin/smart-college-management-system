from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Placement
from .forms import CompanyForm, PlacementForm




def company_create(request):

    form = CompanyForm()

    if request.method == "POST":
        form = CompanyForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("company_list")

    return render(request, "company/company_create.html", {
        "form": form
    })


def company_list(request):

    companies = Company.objects.all().order_by("name")

    return render(request, "company/company_list.html", {
        "companies": companies
    })


def company_detail(request, pk):

    company = get_object_or_404(Company, pk=pk)

    return render(request, "company/company_detail.html", {
        "company": company
    })


def company_update(request, pk):

    company = get_object_or_404(Company, pk=pk)

    form = CompanyForm(instance=company)

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)

        if form.is_valid():
            form.save()
            return redirect("company_list")

    return render(request, "company/company_update.html", {
        "form": form
    })


def company_delete(request, pk):

    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":
        company.delete()
        return redirect("company_list")

    return render(request, "company/company_delete.html", {
        "company": company
    })




def placement_create(request):

    form = PlacementForm()

    if request.method == "POST":
        form = PlacementForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("placement_list")

    return render(request, "company/placement_create.html", {
        "form": form
    })


def placement_list(request):

    placements = Placement.objects.select_related(
        "student",
        "student__user",
        "company"
    ).all().order_by("-placement_date")

    return render(request, "company/placement_list.html", {
        "placements": placements
    })


def placement_detail(request, pk):

    placement = get_object_or_404(
        Placement.objects.select_related(
            "student",
            "student__user",
            "company"
        ),
        pk=pk
    )

    return render(request, "company/placement_detail.html", {
        "placement": placement
    })


def placement_update(request, pk):

    placement = get_object_or_404(Placement, pk=pk)

    form = PlacementForm(instance=placement)

    if request.method == "POST":
        form = PlacementForm(request.POST, instance=placement)

        if form.is_valid():
            form.save()
            return redirect("placement_list")

    return render(request, "company/placement_update.html", {
        "form": form
    })


def placement_delete(request, pk):

    placement = get_object_or_404(Placement, pk=pk)

    if request.method == "POST":
        placement.delete()
        return redirect("placement_list")

    return render(request, "company/placement_delete.html", {
        "placement": placement
    })