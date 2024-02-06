from django.shortcuts import get_object_or_404, render

from .models import Invoice


def invoice_print_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, "invoicing/invoice_print_view.html", {"invoice": invoice})
