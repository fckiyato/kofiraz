# Generated by Django 5.1.1 on 2024-11-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_rename_guest_passenger_remove_booking_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='description',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='paymethod',
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('card_to_card', 'کارت به کارت'), ('cash', 'نقدی')], default='cart_to_cart', max_length=13, verbose_name='روش پرداخت '),
        ),
    ]
