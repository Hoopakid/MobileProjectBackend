# Generated by Django 5.0.2 on 2024-02-23 13:03
# Generated by Django 5.0.2 on 2024-02-22 15:47
# Generated by Django 5.0.2 on 2024-02-23 11:00

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
      ('main', '0018_merge_20240220_1340'),
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='DiscountCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percentage', models.FloatField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('count_product', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
                ('img', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.file')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percentage', models.FloatField()),
                ('rate', models.IntegerField(default=0)),
                ('sold_quantity', models.IntegerField(default=0)),
                ('discounted_price', models.FloatField(blank=True, null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=20)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.country')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('postal_code', models.CharField(max_length=20)),
                ('street_address', models.CharField(max_length=255)),
                ('house_number', models.CharField(max_length=50)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.country')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.state')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.state'),
        ),
    ]
