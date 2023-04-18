from pathlib import Path
from os.path import abspath

from django.test import TestCase

from ledger.importer.hdfc import HDFCDelimitedTextImporter
from ledger.models import Transaction, Account, Category, TransactionType


class HDFCDelimitedTextImporterTestCase(TestCase):
    def setUp(self) -> None:
        test_dir = Path(abspath(__file__)).parents[1]
        self.test_file = str(test_dir / "data" / "hdfc_delimited.txt")
        self.account = Account.objects.create(name="Test Account")

    def test_importer_with_sample_file(self):
        self.assertEqual(Transaction.objects.count(), 0)

        importer = HDFCDelimitedTextImporter(self.account)
        importer.import_transactions(self.test_file)

        self.assertEqual(Transaction.objects.count(), 6)
        self.assertEqual(Transaction.objects.filter(source=self.account).count(), 5)
        self.assertEqual(
            Transaction.objects.filter(destination=self.account).count(), 1
        )

    def test_importer_updates_the_account_balance_when_expected(self):
        self.assertEqual(self.account.balance, 0)

        importer = HDFCDelimitedTextImporter(self.account)
        importer.import_transactions(self.test_file)

        # Balance is unchanged by default
        self.assertEqual(self.account.balance, 0)

        importer.import_transactions(self.test_file, update_account_balance=True)

        # Balance is updated to the same value as the last transaction
        self.assertEqual(self.account.balance, 379907.40)
