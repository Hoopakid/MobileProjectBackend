from rest_framework import serializers
from .models import Product, Size, Category, File, Color, ProductColors, ProductSizes


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file', 'hash')


class ProductSizesSerializer(serializers.ModelSerializer):
    size = SizeSerializer()

    class Meta:
        model = ProductSizes
        fields = ('size',)


class ProductColorsSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = ProductColors
        fields = ('color',)


class ProductAddSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizes
        fields = '__all__'


class ProductAddColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColors
        fields = '__all__'
