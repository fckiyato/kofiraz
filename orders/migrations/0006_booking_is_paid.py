# Generated by Django 5.1.1 on 2024-11-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_booking_paymethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
