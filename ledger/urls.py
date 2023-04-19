from django.urls import path, include

from ledger import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("django.contrib.auth.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("import/firefly/", views.import_firefly, name="import_firefly"),
    path("import/hdfc/", views.import_hdfc, name="import_hdfc"),
]
