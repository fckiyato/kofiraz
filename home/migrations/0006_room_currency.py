# Generated by Django 5.1.1 on 2024-10-06 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_hotel_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='currency',
            field=models.CharField(choices=[('TL', '₺'), ('euro', '€')], default='TL', max_length=4),
        ),
    ]
