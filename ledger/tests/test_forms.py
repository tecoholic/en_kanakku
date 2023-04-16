from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ledger.forms import CSVUploadForm


class CSVUploadFormTest(TestCase):
    def test_valid_csv_file(self):
        file_data = b"name,age\nAlice,30\nBob,40\n"
        csv_file = SimpleUploadedFile("test.csv", file_data, content_type="text/csv")
        data = {"csv_file": csv_file}
        form = CSVUploadForm({}, data)
        self.assertTrue(form.is_valid())

    def test_invalid_csv_file(self):
        file_data = b"name,age\nAlice,30\nBob,40\n"
        text_file = SimpleUploadedFile("test.txt", file_data, content_type="text/plain")
        data = {"csv_file": text_file}
        form = CSVUploadForm({}, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["csv_file"],
            ["Invalid file format: Only CSV files are allowed."],
        )
