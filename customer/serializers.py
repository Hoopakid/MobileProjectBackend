from rest_framework import serializers
from customer.models import Favorite, DiscountProduct, DiscountCategory
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
    country = serializers.CharField()


class DiscountCategorySerializer(serializers.Serializer):
    discount_percentage = serializers.FloatField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()


class DiscountCategoryListserializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCategory
        fields = '__all__'


class DiscountProductSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = DiscountProduct
        fields = ['product_ids', 'discount_percentage', 'start_time', 'end_time']

    def update(self, instance, validated_data):
        product_ids = validated_data.pop('product_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if product_ids is not None:
            instance.products.set(product_ids)

        return instance


class DiscountProductListSerializer(serializers.Serializer):

    class Meta:
        model = DiscountProduct
        fields = '__all__'
