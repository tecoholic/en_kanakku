from ledger.models import Transaction

from .base import CSVImporter


class FireflyIIIImporter(CSVImporter):
    def __init__(self):
        mapping = {
            "date": "date",
            "amount": "amount",
            "description": "description",
            "transaction_type": "type",
            "source": "source_name",
            "destination": "destination_name",
            "category": "category",
        }
        super().__init__(Transaction, mapping)
