from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from ledger.models import Transaction, Account, Category


class IndexPageTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, reverse("login"))

    def test_redirect_if_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, reverse("dashboard"))


class ImportFireflyTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.client.force_login(self.user)

    def test_import_form(self):
        url = reverse("import_firefly")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_import_csv(self):
        url = reverse("import_firefly")
        file_content = b"""date,amount,description,type,source_name,destination_name,category
12-02-2023,20,Purchase,Income,Savings Account,Monthly Expenses,Groceries
13-02-2023,85,Bus Ticket,Income,Savings Account,Monthly Expenses,Transport"""
        csv_file = SimpleUploadedFile("file.csv", file_content, content_type="text/csv")
        data = {"csv_file": csv_file}
        response = self.client.post(url, data=data)
        # redirect to dashboard for now
        self.assertRedirects(response, reverse("dashboard"))

        # Verify that the data is imported properly
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(Category.objects.count(), 2)
