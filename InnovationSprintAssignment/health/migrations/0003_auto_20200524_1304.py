# Generated by Django 3.0.6 on 2020-05-24 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0002_auto_20200524_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertemps',
            name='active_status',
            field=models.CharField(choices=[('HEALTHY', 'Healthy'), ('FEVER', 'Fever')], default='HEALTHY', max_length=9),
        ),
    ]
