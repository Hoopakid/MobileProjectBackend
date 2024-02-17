import datetime
import hashlib

from django.db import models

from django.utils.text import slugify
from os.path import splitext

from mptt.models import MPTTModel, TreeForeignKey


def slugify_upload(instance, filename):
    folder = instance._meta.model_name
    name, ext = splitext(filename)
    name_t = slugify(name) or name
    return f"{folder}/{name_t}{ext}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.IntegerField(default=0)
    sold_quantity = models.IntegerField(default=0)
    price = models.FloatField()
    category = models.ForeignKey('main.Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class ProductSizeColor(models.Model):
    size = models.ForeignKey('main.Size', on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey('main.Color', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    img = models.ForeignKey('main.File', on_delete=models.CASCADE, blank=True, null=True)
    count_product = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to=slugify_upload, blank=True, null=True)
    hash = models.CharField(max_length=150, blank=True, null=True, unique=True)
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        input = self.file.name
        result = hashlib.sha256(input.encode())
        self.hash = result.hexdigest()
        super(File, self).save(*args, **kwargs)

    def __str__(self):
        return self.file.name




