import datetime
import hashlib
from pprint import pprint

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from .models import Product, Color, Category, Size, File, ProductSizeColor, Shoping_cart, PromoCode
from .serializers import CreateProductSerializer, ProductListSerializer, CategorySerializer, ColorSerializer, \
    SizeSerializer, FileUploadSerializer, ProductAddSizeColorSerializer, \
    GetProductSizeColorSerializer, AddCategorySerializer, GetSizeColorSerializer, GetProductSizeSerializer, \
    AddToShoppingCartSerializer, FilterQuerySerializer, PromoCodeSerializer, QuerySerializer


class CreateProductAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = CreateProductSerializer

    def post(self, request):
        product_serializer = self.serializer_class(data=request.data)
        if product_serializer.is_valid():
            product_instance = product_serializer.save()
            product = ProductListSerializer(product_instance)
            return Response(product.data)
        else:
            return Response({'message': 'Product data invalid'})


class GetProductsByCategoryIdAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductListSerializer

    def get(self, request, category_id):
        try:
            product_data = Product.objects.filter(category_id=category_id)
            product_serializer = ProductListSerializer(product_data, many=True)
            return Response(data=product_serializer.data, status=200)
        except Exception as e:
            return Response(status=401, data=f'{e}')


class ProductUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = ()
    serializer_class = CreateProductSerializer
    queryset = Product.objects.all()

    def get(self, request, pk):
        try:
            product_instance = self.get_object()
            if product_instance:
                serializer = ProductListSerializer(product_instance)
                return Response(serializer.data)
            else:
                return Response({'message': 'Product not found!'}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def put(self, request, pk):
        try:
            product_instance = self.get_object()
            if product_instance:
                serializer = self.serializer_class(instance=product_instance, data=request.data)
                if serializer.is_valid():
                    updated_product = serializer.save()
                    product_serializer = ProductListSerializer(updated_product)
                    return Response(product_serializer.data)
                else:
                    return Response({'message': 'Product input invalid !'}, status=400)
            else:
                return Response({'message': 'Product not found!'}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def patch(self, request, pk):
        try:
            product_instance = self.get_object()  # Retrieve the product instance
            if product_instance:
                product_instance.name = request.POST.get('name', product_instance.name)
                product_instance.description = request.POST.get('description', product_instance.description)
                product_instance.price = request.POST.get('price', product_instance.price)
                product_instance.category = request.POST.get('category', product_instance.category)
                product_instance.save()

                # Pass the instance and data to the serializer
                product_serializer = self.serializer_class(instance=product_instance, data=request.data)
                if product_serializer.is_valid():
                    product = product_serializer.save()
                    product_serializer = ProductListSerializer(product)
                    return Response(product_serializer.data)
                else:
                    return Response(product_serializer.errors, status=400)
            else:
                return Response({'message': 'Product not found!'}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=400)


class CreateCategoryAPIView(CreateAPIView):
    queryset = Category.objects.all()
    permission_classes = ()
    serializer_class = AddCategorySerializer


class CategoryGetAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = ()
    serializer_class = CategorySerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = ()
    serializer_class = CategorySerializer


class CreateColorAPIView(CreateAPIView):
    queryset = Color.objects.all()
    permission_classes = ()
    serializer_class = ColorSerializer


class ColorListAPIView(ListAPIView):
    queryset = Color.objects.all()
    permission_classes = ()
    serializer_class = ColorSerializer


class ColorGetAPIView(RetrieveAPIView):
    queryset = Color.objects.all()
    permission_classes = ()
    serializer_class = ColorSerializer


class CreateSizeAPIView(CreateAPIView):
    queryset = Size.objects.all()
    permission_classes = ()
    serializer_class = SizeSerializer


class SizeListAPIView(ListAPIView):
    queryset = Size.objects.all()
    permission_classes = ()
    serializer_class = SizeSerializer


class SizeGetAPIView(RetrieveAPIView):
    queryset = Size.objects.all()
    permission_classes = ()
    serializer_class = SizeSerializer


class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductFileGetDeleteAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = ()
    serializer_class = FileUploadSerializer

    def get(self, request, pk):
        files = File.objects.filter(product=pk)
        files_serializer = self.serializer_class(files, many=True)
        return Response(files_serializer.data)

    def delete(self, request, pk):
        File.objects.get(pk=pk).delete()
        return Response(status=204)


class GetProductSizesAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductAddSizeColorSerializer

    def get(self, request, pk):
        try:
            product_detail = ProductSizeColor.objects.filter(product_id=pk)
            product_detail_serializer = GetProductSizeSerializer(product_detail, many=True)
            return Response(product_detail_serializer.data)
        except Exception as e:
            return Response({'detail': f'{e}'}, status=401)


class GetColorByProductSizeIdAPIView(APIView):
    permission_classes = ()

    def get(self, request):
        try:
            product_id = request.GET.get('product_id')
            size_id = request.GET.get('size_id')

            if product_id is not None and size_id is not None:
                data = ProductSizeColor.objects.filter(Q(product_id=product_id) & Q(size_id=size_id))
                data_serializer = GetSizeColorSerializer(data, many=True)
                return Response(data_serializer.data)
            else:
                return Response({"detail": "product_id and size_id parameters are required."}, status=400)
        except Exception as e:
            return Response(data=f'{e}', status=500)


class AddProductSizeColorAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductAddSizeColorSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({'detail': f'{e}'})


class AllProductSizeColorAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = GetProductSizeColorSerializer

    def get(self, request):
        data = ProductSizeColor.objects.all()
        data_serializer = self.serializer_class(data, many=True)
        return Response(data_serializer.data)


@receiver(post_save, sender=Product)
def update_category_count(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        if category:
            category.count_product = Product.objects.filter(category=category).count()
            category.save()


class ProductListByOtherCategoryAPIView(APIView):
    permission_classes = ()

    def get(self, request):
        try:
            categories = Category.objects.all()
            data = []
            for category in categories:
                product = Product.objects.filter(category_id=category.id).first()
                if product:
                    product_serializer = ProductListSerializer(product)
                    data.append(product_serializer.data)
            return Response(data=data)
        except Exception as e:
            return Response({'detail': str(e)})


class GetTopProductsByCategoryAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductListSerializer

    def get(self, request, category_id):
        try:
            product = Product.objects.filter(category_id=category_id).order_by('-sold_quantity')
            product_serializer = self.serializer_class(product, many=True)
            return Response(product_serializer.data)
        except Exception as e:
            return Response({'error': f'{e}'})


class GetNewArrivalsProductAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductListSerializer

    def get(self, request):
        try:
            three_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
            data = Product.objects.filter(created_at__gte=three_days_ago)
            data_serializer = self.serializer_class(data, many=True)
            return Response(data_serializer.data)
        except Exception as e:
            return Response({'detail': str(e)})


class GetPopularProductAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductListSerializer

    def get(self, request):
        try:
            data = Product.objects.filter(rate__gte=3).order_by('-rate')
            product_serializer = self.serializer_class(data, many=True)
            return Response(product_serializer.data)
        except Exception as e:
            return Response({'error': f'{e}'})


class AddToShoppingCartAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AddToShoppingCartSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            user = request.user.id
            if Shoping_cart.objects.filter(product_id=product_id, user_id=user).exists():
                return Response({"message": "Product already exists in the shopping cart."},
                                status=status.HTTP_400_BAD_REQUEST)
            Shoping_cart.objects.create(product_id=product_id, user_id_id=user)
            return Response({"message": "Product added to the shopping cart successfully."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartListUpdateDelete(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToShoppingCartSerializer


    def get(self, request):
        user_id = request.user.id
        shopping_cart_detail = Shoping_cart.objects.filter(user_id=user_id)
        print(shopping_cart_detail.values())
        if shopping_cart_detail:
            data = []
            for item in shopping_cart_detail.values():
                product = Product.objects.get(id=item.get('product_id_id'))
                if product:
                    product_serializer = ProductListSerializer(product)
                    data.append(product_serializer.data)
            return Response(data=data)
        else:
            return Response({"message": "Shopping cart is empty."}, status=404)


class DeleteShoppingCartAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AddToShoppingCartSerializer

    def delete(self, request, product_id):
        user_id = request.user.id
        if product_id:
            if Shoping_cart.objects.filter(product_id=product_id, user_id=user_id).exists():
                try:
                    Shoping_cart.objects.get(Q(user_id_id=user_id) & Q(product_id=product_id)).delete()
                    return Response(status=201)
                except Exception as e:
                    return Response({'message': 'Product not found', 'error': f'{e}'}, status=404)
            else:
                return Response({'message': 'Product in Shopping cart not found !'})
        else:
            return Response({'message': 'product_id invalid !'})


class SearchCategoryAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = CategorySerializer

    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({'message': 'Query not provided'}, status=400)

        categories = Category.objects.filter(name__icontains=query)
        if categories.exists():
            serializer = self.serializer_class(categories, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No categories found for the query'}, status=404)


class FilterProductsAPIView(GenericAPIView):
    serializer_class = ProductListSerializer

    @swagger_auto_schema(query_serializer=FilterQuerySerializer)
    def get(self, request):
        category_id = request.GET.get('category_id')
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        sort = request.GET.get('sort')
        rate = request.GET.get('rate')

        query = Product.objects.all()

        try:
            if category_id:
                query = query.filter(category_id=category_id)
            if start_price and end_price:
                query = query.filter(price__gte=start_price, price__lte=end_price)
            if sort:
                if sort == 'New_Today':
                    query = query.filter(created_at__day=datetime.datetime.now() - datetime.timedelta(days=1))
                elif sort == 'New_This_Week':
                    query = query.filter(created_at__day=datetime.datetime.now() - datetime.timedelta(days=7))
                elif sort == 'Top_sellers':
                    query = query.filter(sold_quantity__gte=2).order_by('-sold_quantity')
            if rate:
                query = query.filter(rate__gte=rate)
            query_serializer = self.serializer_class(query, many=True)
            return Response(query_serializer.data)
        except Exception as e:
            return Response({'error': str(e)})


class PromoCodeAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PromoCodeSerializer

    @swagger_auto_schema(query_serializer=QuerySerializer)
    def get(self, request):
        query = request.query_params.get('query')
        try:
            promo_code = PromoCode.objects.get(code=query)
        except PromoCode.DoesNotExist:
            return Response({'message': 'PromoCode not found'}, status=status.HTTP_404_NOT_FOUND)

        if promo_code.start_date > timezone.now():
            return Response({'message': 'PromoCode is not active yet'}, status=status.HTTP_400_BAD_REQUEST)

        if promo_code.end_date < timezone.now():
            return Response({'message': 'PromoCode expired'}, status=status.HTTP_400_BAD_REQUEST)
        promo_code.current_usage += 1
        promo_code.save()
        data_serializer = self.serializer_class(promo_code)
        return Response(data_serializer.data)
























