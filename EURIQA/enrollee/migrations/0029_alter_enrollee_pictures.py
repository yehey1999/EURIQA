# Generated by Django 4.0 on 2021-12-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollee', '0028_alter_enrollee_pictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollee',
            name='pictures',
            field=models.ImageField(blank=True, null=True, upload_to='static/faces/'),
        ),
    ]
