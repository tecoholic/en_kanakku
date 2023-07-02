from django.test import TestCase
from datetime import date

from .models import Invoice, InvoiceLineItem, Customer


class InvoiceModelTestCase(TestCase):

    def test_amount(self):
        customer = Customer.objects.create(
            name = "Test Client",
            email = "hello@example.com",
            address = "Planet Earth",
            phone = "1234567890",
        )
        invoice = Invoice.objects.create(
            customer = customer,
            invoice_number="INV-001",
            issue_date = date.today(),
            due_date = date.today(),
        )

        self.assertEqual(invoice.amount, 0)

        line_1 = InvoiceLineItem.objects.create(
            invoice=invoice,
            description = "Line Item 1",
            quantity=1,
            unit_price=50
        )

        self.assertEqual(invoice.amount, 50)

        line_2 = InvoiceLineItem.objects.create(
            invoice = invoice,
            description = "Line Item 2",
            quantity = 3,
            unit_price = 10
        )

        self.assertEqual(invoice.amount, 80)

