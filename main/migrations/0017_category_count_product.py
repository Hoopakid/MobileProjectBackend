# Generated by Django 5.0.2 on 2024-02-15 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_category_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='count_product',
            field=models.IntegerField(default=0),
        ),
    ]