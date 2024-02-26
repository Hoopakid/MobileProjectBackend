from rest_framework import serializers

from .models import Product, Size, Category, File, Color, ProductSizeColor


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file', 'product')


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'img')


class CategorySerializer(serializers.ModelSerializer):
    img = FileUploadSerializer()

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
        fields = ('name', 'description', 'price', 'category')


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class GetProductSizeColorSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    color = ColorSerializer()
    product = ProductListSerializer()

    class Meta:
        model = ProductSizeColor
        fields = '__all__'

        model = File
        fields = ('file', 'product')

    def create(self, validated_data):
        return File.objects.create(**validated_data)


class GetProductSizeSerializer(serializers.ModelSerializer):
    size = SizeSerializer()

    class Meta:
        model = ProductSizeColor
        fields = ('size',)


class GetSizeColorSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = ProductSizeColor
        fields = ('color',)


class ProductAddSizeColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizeColor
        fields = '__all__'


class TemporarilyPhotosSerializer(serializers.Serializer):
    file = serializers.FileField()
