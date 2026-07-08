from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm


# Create Report
def report_create(request):

    form = ReportForm()

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("report_list")

    return render(request, "reports/report_form.html", {
        "form": form
    })


# List Reports
def report_list(request):

    reports = Report.objects.select_related(
        "generated_by"
    ).all()

    return render(request, "reports/report_list.html", {
        "reports": reports
    })


# Report Detail
def report_detail(request, pk):

    report = get_object_or_404(
        Report.objects.select_related("generated_by"),
        pk=pk
    )

    return render(request, "reports/report_detail.html", {
        "report": report
    })


# Update Report
def report_update(request, pk):

    report = get_object_or_404(Report, pk=pk)

    form = ReportForm(instance=report)

    if request.method == "POST":
        form = ReportForm(
            request.POST,
            request.FILES,
            instance=report
        )

        if form.is_valid():
            form.save()
            return redirect("report_list")

    return render(request, "reports/report_form.html", {
        "form": form
    })


# Delete Report
def report_delete(request, pk):

    report = get_object_or_404(
        Report,
        pk=pk
    )

    if request.method == "POST":

        report.delete()

    return redirect("report_list")