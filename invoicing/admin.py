from django.contrib import admin

from invoicing import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


class InvoiceLineItemAdmin(admin.TabularInline):
    model = models.InvoiceLineItem


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceLineItemAdmin,
    ]
    list_filter = ["customer__name", "paid"]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RecurringInvoice)
class RecurringInvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass
