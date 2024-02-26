# Generated by Django 5.0.2 on 2024-02-25 06:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='discountproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.city'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.country'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='state',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.country'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.state'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.state'),
        ),
    ]