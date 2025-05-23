# Generated by Django 4.2.2 on 2025-05-07 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0002_customer_added_by_customer_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customers', to=settings.AUTH_USER_MODEL),
        ),
    ]
