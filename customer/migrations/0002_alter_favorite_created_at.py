# Generated by Django 5.0.2 on 2024-02-21 12:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]