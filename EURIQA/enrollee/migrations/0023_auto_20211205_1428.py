# Generated by Django 3.1.7 on 2021-12-05 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0004_auto_20211129_2317'),
        ('enrollee', '0022_auto_20211205_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examanswers',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.exam'),
        ),
        migrations.AlterField(
            model_name='examanswers',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.part'),
        ),
        migrations.AlterField(
            model_name='examanswers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.question'),
        ),
    ]
