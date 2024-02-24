from rest_framework import serializers
from customer.models import Favorite, DiscountProduct
from main.models import Product, Category


class FavouriteSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField()

    class Meta:
        model = Favorite
        fields = ['product_ids']


class ShippingAddressSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    postal_code = serializers.CharField()
    street_address = serializers.CharField()
    house_number = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    county = serializers.CharField()


class DiscountCategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'img', 'count_product']


class DiscountProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountProduct
        fields = ['discount_percentage', 'start_time', 'end_time']


class DiscountProductListSerializer(serializers.Serializer):
    discounted_price = serializers.FloatField()

    class Meta:
        model = Product
        fields = ('name', 'description', 'rate', 'sold_quantity')
