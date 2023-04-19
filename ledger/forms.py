from django import forms
from crispy_bulma.widgets import FileUploadInput

from ledger.models import Account


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Select the Firefly III CSV export file", widget=FileUploadInput
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data["csv_file"]
        if not csv_file.name.endswith(".csv"):
            raise forms.ValidationError(
                "Invalid file format: Only CSV files are allowed."
            )
        return csv_file


class HDFCDelimitedTextImportForm(forms.Form):
    file = forms.FileField(
        label="Select HDFC Delimited Text export of your Transactions",
        widget=FileUploadInput,
    )
    account = forms.ModelChoiceField(queryset=Account.objects.all())
    update_account_balance = forms.BooleanField(required=False)
