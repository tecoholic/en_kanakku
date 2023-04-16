from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class AccountType(models.TextChoices):
    """Account Types supported.

    1. Saving - Usually the default bank account where we put our money
    2. Mutual Fund - Investments to Mutual Funds
    3. Expense - Accounts which get money from our expense items
    4. Wallet - Cash that we withdraw and hove in our wallet
    5. Credit Card - Self explanatory
    6. Loan - Any long term debt like loans, mortgages, EMIs..etc.,
    7. Family - A family member to whom you transfer funds
    """

    SAVING = "SAV", _("Saving")
    MUTUAL_FUND = "MUT", _("Mutual Fund")
    EXPENSE = "EXP", _("Expense")
    CREDIT_CARD = "CC", _("Credit Card")
    LOAN = "LOA", _("Loan")
    CASH_WALLET = "WAL", _("Cash Wallet")
    FAMILY = "FAM", _("Family")


class Currency(models.TextChoices):
    INR = "INR", _("Indian Rupees")
    USD = "USD", _("United States Dollar")
    EUR = "EUR", _("Euro")
    AUD = "AUD", _("Australian Dollar")
    GBP = "GBP", _("Great Britian Pound")


class Account(TimeStampedModel, models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_type = models.CharField(max_length=3, choices=AccountType.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    currency = models.CharField(
        max_length=3, default=Currency.INR, choices=Currency.choices
    )

    def __str__(self):
        return f"{self.name}"


class Category(TimeStampedModel, models.Model):
    """Categories for Transactions."""

    class Meta:
        verbose_name_plural = "catagories"

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class TransactionType(models.TextChoices):
    DEPOSIT = "DEPOSIT", _("Income")
    WITHDRAWAL = "WITHDRAWAL", _("Expense")
    TRANSFER = "TRANSFER", _("Transfer")


class Transaction(TimeStampedModel):
    date = models.DateField()
    description = models.TextField()
    transaction_type = models.CharField(max_length=50, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="source_transactions",
        null=True,
        blank=True,
    )
    destination = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="destination_transactions",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.description} - {self.amount}"
