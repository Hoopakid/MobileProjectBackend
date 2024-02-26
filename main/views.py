import os
import hashlib

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from opencv.utils import check_image_similarity
from .models import Product, Color, Category, Size, File, ProductSizeColor
from .serializers import CreateProductSerializer, ProductListSerializer, CategorySerializer, ColorSerializer, \
    SizeSerializer, FileUploadSerializer, ProductAddSizeColorSerializer, \
    GetProductSizeColorSerializer, AddCategorySerializer, GetSizeColorSerializer, GetProductSizeSerializer, \
    TemporarilyPhotosSerializer


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


class FileUploadAPIView(GenericAPIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
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


class ProductFileGetDelete(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = ()
    serializer_class = FileUploadSerializer

    def get(self, request, pk):
        files = File.objects.filter(product=pk)
        files_serializer = self.serializer_class(files, many=True)
        return Response(files_serializer.data)

    def delete(self, request, pk):
        try:
            file_instance = File.objects.get(pk=pk)
        except File.DoesNotExist:
            return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        file_path = file_instance.file.path
        if os.path.exists(str(file_path)):
            os.remove(str(file_path))

        file_instance.delete()

        return Response({"message": "File deleted successfully", "status": status.HTTP_204_NO_CONTENT})


class GetProductSizes(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductAddSizeColorSerializer

    def get(self, request, pk):
        try:
            product_detail = ProductSizeColor.objects.filter(product_id=pk)
            product_detail_serializer = GetProductSizeSerializer(product_detail, many=True)
            return Response(product_detail_serializer.data)
        except Exception as e:
            return Response({'detail': f'{e}'}, status=401)


class GetColorByProductSizeId(APIView):
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


class AddProductSizeColor(GenericAPIView):
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


class AllProductSizeColor(GenericAPIView):
    permission_classes = ()
    serializer_class = GetProductSizeColorSerializer

    def get(self, request):
        data = ProductSizeColor.objects.all()
        data_serializer = self.serializer_class(data, many=True)
        return Response(data_serializer.data)


# @receiver(post_save, sender=Product)
# def update_category_count(sender, instance, created, **kwargs):
#     if created:
#         category = instance.category
#         if category:
#             category.count_product = Product.objects.filter(category=category).count()
#             category.save()
#
#         sizes = ProductSizes.objects.filter(product_id=pk)
#         sizes_serializer = ProductSizesSerializer(sizes, many=True)
#         return Response(sizes_serializer.data)


class GetSimilarProductsAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = TemporarilyPhotosSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                uploaded_file = serializer.validated_data['file']
                file_content = uploaded_file.read()
                with open(f'media/temporarily/{uploaded_file.name}', 'wb') as f:
                    f.write(file_content)
                similarity_percentage = check_image_similarity(uploaded_file.name)
                similar_products = []
                for products in similarity_percentage:
                    if float(list(products.values())[0]) > 50.0:
                        similar_products.append(products)

                similar_product_ids = []
                for filename in similar_products:
                    file_name = f'file/{list(filename.keys())[0]}'
                    try:
                        file_obj = File.objects.get(file__icontains=file_name)
                        if file_obj.product_id not in similar_product_ids:
                            similar_product_ids.append(file_obj.product_id)
                    except File.DoesNotExist:
                        pass

                similar_products_data = []
                for product_id in similar_product_ids:
                    try:
                        product = Product.objects.get(pk=product_id)
                        similar_products_data.append(product)
                    except Product.DoesNotExist:
                        pass

                serializer = ProductListSerializer(similar_products_data, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


