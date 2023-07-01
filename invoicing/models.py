from django.db import models


class Currencies(models.TextChoices):
    USD = "USD", "USD"
    EUR = "EUR", "EUR"
    AUD = "AUD", "AUD"
    INR = "INR", "INR"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    currency = models.CharField(
        max_length=3, choices=Currencies.choices, default=Currencies.USD
    )

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20)
    issue_date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.invoice_number


class PaymentModes(models.TextChoices):
    CASH = "cash", "Cash"
    CREDIT_CARD = "credit_card", "Credit Card"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    BANK_REMITTANCE = "bank_remittance", "Bank Remittance"
    OTHER = "other", "Other"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_mode = models.CharField(
        max_length=20,
        choices=PaymentModes.choices,
        default=PaymentModes.BANK_REMITTANCE,
    )
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(
        max_length=3, choices=Currencies.choices, default=Currencies.USD
    )

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.payment_mode}"


class RecurringInvoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3, choices=Currencies.choices, default=Currencies.USD
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    recurrence_interval = models.PositiveIntegerField(default=1)
    recurrence_unit = models.CharField(
        max_length=10,
        choices=(
            ("day", "Day"),
            ("week", "Week"),
            ("month", "Month"),
            ("year", "Year"),
        ),
        default="month",
    )
    auto_send = models.BooleanField(default=False)

    def __str__(self):
        return self.invoice_number


class InvoiceLineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description}"
