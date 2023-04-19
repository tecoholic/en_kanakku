from django.contrib import admin, messages

from ledger import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_filter = ["account_type"]
    actions = ["merge_accounts"]

    @admin.action(description="Merge accounts")
    def merge_accounts(self, request, queryset):
        """Merges multiple accounts into the first account in the queryset"""
        first = queryset.order_by("pk").first()
        other_accounts = [acc for acc in queryset.all() if acc != first]

        source_updated = models.Transaction.objects.filter(
            source__in=other_accounts
        ).update(source=first)
        destination_updated = models.Transaction.objects.filter(
            destination__in=other_accounts
        ).update(destination=first)

        for account in other_accounts:
            account.delete()

        self.message_user(
            request,
            f"{source_updated} transactions' source account and {destination_updated} transactions' destination account has been set as '{first.name}'",
            messages.SUCCESS,
        )


@admin.register(models.Category)
class CatagoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ["source", "transaction_type", "category"]
    date_hierarchy = "date"
