# Generated by Django 5.1.1 on 2024-10-28 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_comment_hotel_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='agency_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
