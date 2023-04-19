from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from ledger.models import Transaction, Account, Category


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.client.force_login(self.user)


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


class ImportFireflyTest(LoggedInTestCase):
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


class ImportHDFCViewTest(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(
            name="Test Account", balance=0.0, user=self.user
        )

    def test_import_form(self):
        url = reverse("import_hdfc")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_import_delimited_text(self):
        url = reverse("import_hdfc")
        file_content = b"""
  Date     ,Narration                                                                                                                ,Value Dat,Debit Amount       ,Credit Amount      ,Chq/Ref Number   ,Closing Balance
  12/12/2023,THIS IS an Expense                                                                                                      ,12/12/2023,4000.75           ,0.00               ,1234GH234        ,204500.95
  13/12/2023,    Second Expense                                                                                                      ,12/12/2023,500.000           ,0.00               ,1234GH234        ,204000.95
"""
        file = SimpleUploadedFile(
            "statememt.txt", file_content, content_type="text/plain"
        )
        # Upload without updating the balance
        data = {"file": file, "account": self.account.pk}
        response = self.client.post(url, data=data)

        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertEqual(Account.objects.get(pk=self.account.pk).balance, 0)

        # Verify that the account balance is updated
        file = SimpleUploadedFile(
            "statememt.txt", file_content, content_type="text/plain"
        )
        data = {
            "file": file,
            "account": self.account.pk,
            "update_account_balance": True,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(
            Account.objects.get(pk=self.account.pk).balance, Decimal("204000.95")
        )
