# Generated by Django 5.1.1 on 2024-11-09 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='natid',
            field=models.IntegerField(unique=True),
        ),
    ]
