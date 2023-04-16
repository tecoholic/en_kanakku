import os.path

from django.test import TestCase

from ledger.importer.base import CSVImporter
from ledger.models import Transaction, Account, Category, TransactionType


class CSVImporterTestCase(TestCase):
    def setUp(self):
        self.mapping = {
            "date": "date",
            "description": "description",
            "transaction_type": "type",
            "amount": "amount",
            "source": "from_account",
            "destination": "to_account",
            "category": "category",
        }
        self.importer = CSVImporter(Transaction, self.mapping)

    def test_create_transaction_creates_transactions_based_on_mapping(self):
        transaction = self.importer.create_transaction(
            {
                "date": "1999-12-31",
                "description": "End of a millenium",
                "type": "DEPOSIT",
                "amount": 12.75,
                "from_account": "Employer 1",
                "to_account": "My Savings Account",
                "category": "Salary",
            }
        )
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_transaction_throws_an_exception_when_mapping_is_wrong(self):
        field_mapping = {"hello": "world"}
        importer = CSVImporter(Transaction, field_mapping)
        with self.assertRaises(ValueError):
            importer.create_transaction({"test": "unexpected"})

    def test_csv_files_are_processed_as_expected(self):
        tests_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.importer.import_csv(os.path.join(tests_dir, "data", "test.csv"))
        self.assertEqual(Transaction.objects.count(), 3)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Account.objects.count(), 2)

    def test_related_objects_are_not_created_if_the_field_is_empty(self):
        transaction = self.importer.create_transaction(
            {
                "date": "2022-03-12",
                "description": "This doesn't have a category",
                "type": TransactionType.TRANSFER,
                "amount": 30,
                "from_account": "My Account",
                "to_account": "",
                "category": "",
            }
        )
        self.assertEqual(Category.objects.count(), 0)
        self.assertIsNone(transaction.destination)

    def test_transaction_type_is_auto_assigned_if_missing_from_the_data(self):
        transaction = self.importer.create_transaction(
            {
                "date": "2022-03-12",
                "description": "This doesn't have a category",
                "type": "",
                "amount": 30,
                "from_account": "My Account",
                "to_account": "",
                "category": "",
            }
        )
        self.assertEqual(transaction.transaction_type, TransactionType.DEPOSIT)

        transaction = self.importer.create_transaction(
            {
                "date": "2022-03-12",
                "description": "This doesn't have a category",
                "type": "",
                "amount": -30,
                "from_account": "My Account",
                "to_account": "",
                "category": "",
            }
        )
        self.assertEqual(transaction.transaction_type, TransactionType.WITHDRAWAL)
