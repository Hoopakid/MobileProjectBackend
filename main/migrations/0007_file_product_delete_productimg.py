# Generated by Django 5.0.2 on 2024-02-08 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_category_options_remove_product_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product'),
        ),
        migrations.DeleteModel(
            name='ProductImg',
        ),
    ]
