import os.path

from django.test import TestCase

from ledger.importer.firefly_iii import FireflyIIIImporter
from ledger.models import Transaction, Account, Category, TransactionType


class FireflyIIIImporterTestCase(TestCase):
    def test_importer_with_sample_file(self):
        tests_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        importer = FireflyIIIImporter()
        importer.import_csv(os.path.join(tests_dir, "data", "firefly_iii_export.csv"))

        self.assertEqual(
            Transaction.objects.filter(
                transaction_type=TransactionType.DEPOSIT
            ).count(),
            1,
        )
        self.assertEqual(
            Transaction.objects.filter(
                transaction_type=TransactionType.WITHDRAWAL
            ).count(),
            9,
        )
        self.assertEqual(Account.objects.count(), 5)
        self.assertEqual(Category.objects.count(), 4)
