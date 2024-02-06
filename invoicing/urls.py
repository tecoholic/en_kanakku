from django.urls import path

from . import views

urlpatterns = [
    path("<int:invoice_id>/print_view/", views.invoice_print_view, name="print_view"),
]
