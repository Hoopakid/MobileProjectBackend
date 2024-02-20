from django.core.validators import MaxValueValidator
from rest_framework import serializers

from .models import Product, Size, Category, File, Color, ProductSizeColor, Shoping_cart, PromoCode


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',)


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
        fields = ('name', 'description', 'price', 'category', 'quantity')


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


class AddToShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shoping_cart
        fields = ('product_id', )


sort_by_choices = (
        ('New_Today', 'New_This_Week', 'Top_sellers')
    )


class FilterQuerySerializer(serializers.Serializer):
    category_id = serializers.CharField(required=False)
    start_price = serializers.IntegerField(required=False)
    end_price = serializers.IntegerField(required=False)
    sort_by = serializers.ChoiceField(choices=sort_by_choices)
    rate = serializers.IntegerField(validators=[MaxValueValidator(5)])


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ('discount', )


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)
