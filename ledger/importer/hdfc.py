import logging
from typing import Dict

from dateutil.parser import parse
from ledger.models import Account, Transaction, TransactionType

from ledger.importer.utils import find_comma_indexes, split_string

logger = logging.getLogger(__name__)


class HDFCDelimitedTextImporter:
    def __init__(self, account: Account):
        logger.info("Initializing HDFCDelimitedTextImporter for account: %s", account)
        self.account = account
        self.expected_headers = [
            "Date",
            "Narration",
            "Value Dat",
            "Debit Amount",
            "Credit Amount",
            "Chq/Ref Number",
            "Closing Balance",
        ]

    def import_transactions(self, filepath: str, update_account_balance: bool = False):
        headers = []
        row = {}
        column_ends = []
        with open(filepath) as fp:
            for line in fp:
                if not line.strip():
                    continue

                # Technically we could skip parsing this row as we already have
                # the headers hardcoded as expected_headers. But this assignment
                # and the assertion will help us catch any change in the bank
                # statement's formatting
                if not headers:
                    headers = [s.strip() for s in line.split(",")]
                    assert headers == self.expected_headers
                    continue

                # Set the column_ends based on the comma locations on the first transaction
                if not column_ends:
                    column_ends = find_comma_indexes(line)
                    # make sure we are splitting the row text into the same number of columns
                    # as the headers
                    assert len(column_ends) == len(headers) - 1

                row_items = [
                    s.replace(",", "").strip() for s in split_string(line, column_ends)
                ]
                row = dict(zip(headers, row_items))
                debit = float(row["Debit Amount"])
                credit = float(row["Credit Amount"])
                Transaction.objects.create(
                    date=parse(row["Date"], dayfirst=True),
                    description=row["Narration"],
                    # Since firefly stores everything as an outflow lets -1 times the amount
                    amount=-1 * (debit or credit),
                    transaction_type=TransactionType.WITHDRAWAL
                    if debit
                    else TransactionType.DEPOSIT,
                    source=self.account if debit else None,
                    destination=self.account if credit else None,
                )
        if update_account_balance:
            self.account.balance = float(row["Closing Balance"])
            self.account.save()
