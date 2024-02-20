from rest_framework import serializers
from customer.models import Favorite, DiscountProduct


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


class DiscountProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountProduct
        fields = ['product', 'discount_percentage', 'start_time', 'end_time']
