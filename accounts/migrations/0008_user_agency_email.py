# Generated by Django 5.1.1 on 2024-10-02 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_delete_agencyusermodel_delete_normalusermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='agency_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
