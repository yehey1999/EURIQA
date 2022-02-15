# Generated by Django 4.0 on 2022-02-15 04:34

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollee', '0033_alter_enrollee_pictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollee',
            name='pictures',
            field=models.ImageField(blank=True, null=True, upload_to=django.core.files.storage.FileSystemStorage(location='static/facerec_assets/images/')),
        ),
    ]
