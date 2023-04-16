from datetime import date
from django.http import HttpRequest

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ledger.models import Account, Category, Transaction


class BaseAdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="testuser", email="testuser@test.com", password="testpass"
        )
        self.client.force_login(self.user)


class TransactionAdminTest(BaseAdminTestCase):
    def setUp(self):
        super().setUp()
        self.transaction = Transaction.objects.create(
            date=date.today(), amount=100, description="Test transaction"
        )

    def test_transaction_list_view(self):
        response = self.client.get(reverse("admin:ledger_transaction_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test transaction")


class CategoryAdminTest(BaseAdminTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name="Test Category")

    def test_account_list_view(self):
        response = self.client.get(reverse("admin:ledger_category_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")


class AccountAdminTest(BaseAdminTestCase):
    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(name="Test Account")

    def test_account_list_view(self):
        response = self.client.get(reverse("admin:ledger_account_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Account")

    def test_the_selected_accounts_are_merged(self):
        self.account1 = Account.objects.create(name="Account 1")
        self.account2 = Account.objects.create(name="Account 2")
        self.account3 = Account.objects.create(name="Account 3")

        for account in [self.account1, self.account2, self.account3]:
            Transaction.objects.create(
                date=date.today(),
                amount=20,
                description="Transaction for " + account.name,
                source=account,
            )
            Transaction.objects.create(
                date=date.today(),
                amount=20,
                description="Transaction for " + account.name,
                destination=account,
            )

        # Peform Action
        data = {
            "action": "merge_accounts",
            "_selected_action": [self.account1.pk, self.account2.pk],
        }
        url = reverse("admin:ledger_account_changelist")
        self.client.post(url, data)

        # Verify that all the transactions with either the source or the destination pointing
        # to account 2 has now been moved to account 1
        self.assertEqual(Transaction.objects.filter(source=self.account1).count(), 2)
        self.assertEqual(
            Transaction.objects.filter(destination=self.account1).count(), 2
        )
        self.assertEqual(
            Transaction.objects.filter(source__name="Account 2").count(), 0
        )
        self.assertEqual(
            Transaction.objects.filter(destination__name="Account 2").count(), 0
        )
        # And that the account 2 is deleted
        self.assertEqual(Account.objects.filter(name="Account 2").count(), 0)
