# Generated by Django 5.0.2 on 2024-02-08 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_size_category_alter_file_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='product',
            name='sold_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
