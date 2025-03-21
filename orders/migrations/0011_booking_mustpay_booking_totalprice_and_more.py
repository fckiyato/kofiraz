# Generated by Django 5.1.1 on 2024-11-12 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_remove_booking_natid_remove_booking_phonenum'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='mustpay',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='totalprice',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='paymethod',
            field=models.CharField(blank=True, choices=[('کارت به کارت', 'کارت به کارت'), ('نقدی', 'نقدی')], max_length=13, verbose_name='روش پرداخت '),
        ),
    ]
