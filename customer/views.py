from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import DiscountProduct, ShippingAddress, Country, State, City
from customer.serializers import DiscountProductSerializer, ShippingAddressSerializer
from main.models import Product


class ShippignAddressAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShippingAddressSerializer

    def post(self, request):
        phone_number = request.data.get('phone_number')
        postal_code = request.data.get('postal_code')
        street_address = request.data.get('street_address')
        house_number = request.data.get('house_number')
        state_name = request.data.get('state')
        city_name = request.data.get('city')
        country_name = request.data.get('country')

        if not country_name:
            return Response("Country name cannot be empty")

        country, created = Country.objects.get_or_create(name=country_name)
        state, created = State.objects.get_or_create(state=state_name, country=country)
        city, created = City.objects.get_or_create(city=city_name, state=state)

        add_data = ShippingAddress.objects.create(
            user_id=request.data['id'],
            phone_number=phone_number,
            postal_code=postal_code,
            street_address=street_address,
            house_number=house_number,
            country=country,
            state=state,
            city=city
        )

        serializer = ShippingAddressSerializer(add_data)

        return Response(serializer.data)

    def get(self, request):
        shipping_addresses = ShippingAddress.objects.get(user_id=request.data.id)
        serializer = ShippingAddressSerializer(shipping_addresses, many=True)
        return serializer.data

    def put(self, request):
        phone_number = request.data.get('phone_number')
        street_address = request.data.get('street_address')
        city = request.data.get('city')
        state = request.data.get('state')
        postal_code = request.data.get('postal_code')
        country = request.data.get('country')

        try:
            title = ShippingAddress.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"error": "ShippingAddress not found"})

        if phone_number:
            title.phone_number = phone_number
        if street_address:
            title.street_address = street_address
        if city:
            title.city = city
        if state:
            title.state = state
        if postal_code:
            title.postal_code = postal_code
        if country:
            title.country = country
        title.save()
        shipping_address_serializer = ShippingAddressSerializer(title)
        return Response(shipping_address_serializer.data)

    def delete(self, request):
        user = request.user.id
        ShippingAddress.objects.get(user_id=user).delete()
        return Response({'success': True})


class DiscountProductAPIView(GenericAPIView):
    serializer_class = DiscountProductSerializer

    def post(self, request):
        product = request.data.get('c')
        percentage = request.data.get('discount_percentage')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        try:
            product_data = Product.objects.get(pk=product)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist"})

        if float(percentage) is not None:
            if 100 < float(percentage) < 0:
                return Response({"error": "Discount percentage should be between 0 and 100"}, status=400)

        discounted_price = float(product_data.price) - (float(product_data.price) * (float(percentage) / 100))
        discount_product_data = DiscountProduct.objects.create(
            product_id=product,
            discount_percentage=percentage,
            discounted_price=discounted_price,
            start_time=start_time,
            end_time=end_time
        )
        serializer = DiscountProductSerializer(discount_product_data)
        return Response(serializer.data)

    def get(self, request):
        discount_data = DiscountProduct.objects.all()
        discount_serializer = DiscountProductSerializer(discount_data, many=True)
        return discount_serializer.data

    def patch(self, request):
        product = request.POST.get('product_id')
        percentage = request.POST.get('discount_percentage')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        title = DiscountProduct.objects.get(product_id=product)
        if percentage:
            title.discount_percentage = percentage
        if start_time:
            title.start_time = start_time
        if end_time:
            title.end_time = end_time

        title.save()
        serializer = DiscountProductSerializer(title, many=True)
        return serializer.data
