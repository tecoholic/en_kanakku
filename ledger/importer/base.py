import csv
from decimal import Decimal
from typing import Dict, Type

from dateutil.parser import parse as parse_date
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey, Model


from ledger.models import Transaction, TransactionType


class CSVImporter:
    """
    A generic CSV importer for Django models.

    Attributes:
    -----------
    model_cls : django.db.models.Model
        The Django model class to import data into.
    mapping : dict
        A dictionary mapping CSV field names to model field names.
        Keys are CSV field names and values are model field names.
    """

    def __init__(
        self,
        model_cls: Type[Transaction],
        mapping: Dict[str, str],
        transaction_type_mapping: Dict[str, str] | None = None,
    ):
        """
        Initializes a new instance of the CSVImporter class.

        Parameters:
        -----------
        model_cls : django.db.models.Model
            The Django model class to import data into.
        mapping : dict
            A dictionary mapping CSV field names to model field names.
            Keys are CSV field names and values are model field names.
        transaction_type_mapping: dict
            A dictionary mapping the transaction types in the CSV field
            corresponding to "transaction_type" of the model if the CSV
            uses words other than"Deposit", "Withdrawal" and "Transfer".
        """
        self.model_cls = model_cls
        self.mapping = mapping
        self.transaction_type_mapping = transaction_type_mapping or {}

    def import_csv(self, file_path: str):
        """
        Imports data from a CSV file into the specified Django model.

        Parameters:
        -----------
        file_path : str
            The path to the CSV file to import.

        Raises:
        -------
        ValueError
            If the CSV file does not contain all the required fields.
        """
        with open(file_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                model_obj = self.create_transaction(row)
                model_obj.save()

    def create_transaction(self, row: Dict) -> Transaction:
        """
        Converts a CSV row into a Django model object.

        Parameters:
        -----------
        row : dict
            A dictionary representing a single row of CSV data.

        Returns:
        --------
        django.db.models.Model
            A new instance of the Django model class with the specified field values.

        Raises:
        -------
        ValueError
            If the CSV row does not contain all the required fields.
        """
        # Map CSV fields to model fields
        model_kwargs = {}
        for model_field, csv_field in self.mapping.items():
            if csv_field not in row:
                raise ValueError(f"CSV field {csv_field} not found in row {row}")
            model_kwargs[model_field] = row[csv_field]

        # Convert data types if necessary
        if "date" in model_kwargs:
            model_kwargs["date"] = parse_date(model_kwargs["date"]).date()

        if "amount" in model_kwargs:
            model_kwargs["amount"] = Decimal(model_kwargs["amount"])

        if not model_kwargs.get("transaction_type", None):
            model_kwargs["transaction_type"] = (
                TransactionType.DEPOSIT
                if model_kwargs["amount"] > 0
                else TransactionType.WITHDRAWAL
            )
        else:
            model_kwargs["transaction_type"] = model_kwargs["transaction_type"].upper()
            # If it is not a value defined in the TransactionType choices, then
            # standardise it by looking up the custom mapping
            if model_kwargs["transaction_type"] not in [
                c[0] for c in TransactionType.choices
            ]:
                model_kwargs["transaction_type"] = self.transaction_type_mapping.get(
                    model_kwargs["transaction_type"], model_kwargs["transaction_type"]
                )

        # Find all the relationships
        related_fields: Dict[str, Type[Model]] = {}
        for field in self.model_cls._meta.get_fields():
            if isinstance(field, ForeignKey):
                related_fields[field.name] = field.related_model

        # Find or create related objects
        for field_name, related_model in related_fields.items():
            if field_name in model_kwargs:
                related_name = model_kwargs[field_name]
                # If the related field is empty skip it
                if not related_name.strip():
                    del model_kwargs[field_name]
                    continue
                try:
                    related_obj = related_model.objects.get(name=related_name)
                except ObjectDoesNotExist:
                    related_obj = related_model(name=related_name)
                    related_obj.save()
                model_kwargs[field_name] = related_obj

        # Create model object
        return self.model_cls(**model_kwargs)
