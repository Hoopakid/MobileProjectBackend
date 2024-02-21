from django.contrib import admin
from .models import Product, Color, Size, File, Category, ProductSizeColor, Shoping_cart, PromoCode

admin.site.register((Product, Color, Size, File, Category, ProductSizeColor, Shoping_cart, PromoCode))
