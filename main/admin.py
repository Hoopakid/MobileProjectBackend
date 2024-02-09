from django.contrib import admin
from .models import Product, Color, Size, File, Category

admin.site.register((Product, Color, Size, File, Category))
