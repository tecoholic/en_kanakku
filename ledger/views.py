import os

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CSVUploadForm
from .importer.firefly_iii import FireflyIIIImporter


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return redirect("login")


@login_required
def dashboard(request):
    return render(request, "ledger/dashboard.html")


@login_required
def import_firefly(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file: TemporaryUploadedFile = request.FILES["csv_file"]
            importer = FireflyIIIImporter()
            importer.import_csv(file.temporary_file_path())
            os.remove(file.temporary_file_path())
            return redirect("dashboard")
    else:
        form = CSVUploadForm()
    return render(request, "ledger/import/firefly.html", {"form": form})
