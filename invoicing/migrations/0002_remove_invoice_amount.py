# Generated by Django 4.1.7 on 2023-07-02 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='amount',
        ),
    ]
