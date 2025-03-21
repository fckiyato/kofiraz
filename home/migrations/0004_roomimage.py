# Generated by Django 5.1.1 on 2024-10-05 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_hotel_hotel_image_hotelimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='room/images/', verbose_name='عکس های اتاق ها')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RoomsImages', to='home.room')),
            ],
        ),
    ]
