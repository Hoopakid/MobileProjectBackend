from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from customer.models import DiscountProduct, ShippingAddress, Country, State, City, Favorite
from customer.serializers import DiscountProductSerializer, ShippingAddressSerializer, FavouriteSerializer, \
    DiscountCategorySerializer, DiscountProductListSerializer
from main.models import Product, Category
from main.serializers import ProductListSerializer


class MyFavouriteAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteSerializer

    def post(self, request):
        user_id = request.user.id
        product_ids = request.data.get('product_ids', [])

        if not user_id:
            return Response({'success': False, "error": "user_id is required"})

        success_product_ids = []
        error_product_ids = []

        for product_id in product_ids:
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                error_product_ids.append(product_id)
                continue

            try:
                favorite = Favorite.objects.get(user_id=user_id, product_id=product_id)
                favorite.delete()
                success_product_ids.append(product_id)
            except Favorite.DoesNotExist:
                user_product = Favorite.objects.create(
                    user_id=user_id,
                    product_id=product_id
                )
                user_product.save()
                success_product_ids.append(product_id)
            except:
                error_product_ids.append(product_id)

        response_data = {'success': True,
                         'success_product_ids': success_product_ids,
                         'error_product_ids': error_product_ids}
        return Response(response_data)

    def get(self, request):
        user_id = request.user.id
        favorites = Favorite.objects.filter(user_id=user_id)
        product_ids = [favorite.product_id for favorite in favorites]
        products = Product.objects.filter(pk__in=product_ids)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


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
        user = request.user.id

        if not user:
            return Response({'success': False, "error": "user_id is required"})

        try:
            exists_data = ShippingAddress.objects.get(user=user)
            if exists_data:
                exists_data.delete()
        except ShippingAddress.DoesNotExist:
            pass

        try:
            country = Country.objects.get(name=country_name)
        except Country.DoesNotExist:
            return Response({'success': False, 'detail': 'such a country does not exist !!!'})

        try:
            state = State.objects.get(state=state_name, country=country)
        except State.DoesNotExist:
            return Response({'success': False, 'detail': 'There is no state in such a country !!!'})

        try:
            city = City.objects.get(city=city_name, state=state.id)
            add_data = ShippingAddress.objects.create(
                user_id=request.user.id,
                phone_number=phone_number,
                postal_code=postal_code,
                street_address=street_address,
                house_number=house_number,
                country_id=country.id,
                state_id=state.id,
                city_id=city.id
            )
            add_data.save()
            serializer = ShippingAddressSerializer(add_data)
            return Response({'success': True, 'detail': serializer.data})
        except City.DoesNotExist:
            return Response({'success': False, 'detail': 'There is no city in such a state !!!'})

    def get(self, request):
        user_id = request.user.id

        if not user_id:
            return Response({'success': False, "error": "user_id is required"})

        shipping_addresses = ShippingAddress.objects.filter(user_id=user_id)
        serializer = ShippingAddressSerializer(shipping_addresses, many=True)
        return Response(serializer.data)

    def put(self, request):
        phone_number = request.data.get('phone_number')
        postal_code = request.data.get('postal_code')
        street_address = request.data.get('street_address')
        house_number = request.data.get('house_number')
        state_name = request.data.get('state')
        city_name = request.data.get('city')
        country_name = request.data.get('country')
        user = request.user.id

        if not user:
            return Response({'success': False, "error": "user_id is required"})

        try:
            title = ShippingAddress.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"error": "ShippingAddress not found"})

        try:
            exists_data = ShippingAddress.objects.get(user=user)
            if exists_data:
                exists_data.delete()
        except ShippingAddress.DoesNotExist:
            pass

        try:
            country = Country.objects.get(name=country_name)
        except Country.DoesNotExist:
            return Response({'success': False, 'detail': 'such a country does not exist !!!'})

        try:
            state = State.objects.get(state=state_name, country=country)
        except State.DoesNotExist:
            return Response({'success': False, 'detail': 'There is no state in such a country !!!'})

        try:
            city = City.objects.get(city=city_name, state=state.id)
            if phone_number:
                title.phone_number = phone_number
            if postal_code:
                title.postal_code = postal_code
            if street_address:
                title.street_address = street_address
            if house_number:
                title.house_number = house_number
            if city:
                title.city = city
            if state:
                title.state = state
            if country:
                title.country = country
            title.save()
            serializer = ShippingAddressSerializer(title)
            return Response({'success': True, 'detail': serializer.data})
        except City.DoesNotExist:
            return Response({'success': False, 'detail': 'There is no city in such a state !!!'})

    def delete(self, request):
        try:
            exists_data = ShippingAddress.objects.get(user=request.user.id)
            if exists_data:
                exists_data.delete()
            return Response({'success': True})
        except ShippingAddress.DoesNotExist:
            return Response({'success': False})


class DiscountProductAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DiscountProductSerializer

    def post(self, request, category_id):
        percentage = request.data.get('discount_percentage')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        try:
            category_instance = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:  # Changed Product.DoesNotExist to Category.DoesNotExist
            return Response({"error": "Category does not exist"})

        products = Product.objects.filter(category_id=category_id)

        if not 0 <= float(percentage) <= 100:  # Corrected the condition
            return Response({"error": "Discount percentage should be between 0 and 100"}, status=400)

        datas = []

        for product in products:
            discounted_price = float(product.price) - (float(product.price) * (float(percentage) / 100))
            discount_product_data = DiscountProduct.objects.create(
                category=category_instance,
                product=product,
                discount_percentage=percentage,
                discounted_price=discounted_price,
                start_time=start_time,
                end_time=end_time
            )
            datas.append(discount_product_data)

        serializer = DiscountProductSerializer(datas, many=True)
        return Response(serializer.data)


    def patch(self, request, category_id):
        percentage = request.data.get('discount_percentage')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        try:
            category_instance = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category does not exist"})

        discount_product_data = DiscountProduct.objects.filter(category=category_instance)

        for title in discount_product_data:
            if percentage:
                title.discount_percentage = percentage
                title.discounted_price = float(title.product.price) - (
                        float(title.product.price) * (float(percentage) / 100))

            if start_time:
                title.start_time = start_time
            if end_time:
                title.end_time = end_time

            title.save()
        serializer = DiscountProductSerializer(discount_product_data, many=True)
        return Response(serializer.data)


class DiscountCategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = DiscountCategorySerializer


class DiscountProductListAPIView(GenericAPIView):
    serializer_class = DiscountProductListSerializer

    def get(self, request, category_id):
        current_time = now()
        discount_category_data = DiscountProduct.objects.filter(
            category=category_id,
            start_time__gte=current_time
        )

        if not discount_category_data:
            return Response({'success': False, 'error': 'Category not found !!!'})

        products_with_discount = []
        for discount in discount_category_data:
            product = Product.objects.get(pk=discount.product.id)
            products_with_discount.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'discounted_price': discount.discounted_price,
                'rate': product.rate,
                'sold_quantity': product.sold_quantity
            })

        discount_serializer = DiscountProductListSerializer(products_with_discount, many=True)
        return Response(discount_serializer.data)
