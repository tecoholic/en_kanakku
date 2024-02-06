# Generated by Django 4.1.7 on 2024-02-06 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0004_gst_related_details_for_the_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='invoicing.supplier'),
        ),
    ]