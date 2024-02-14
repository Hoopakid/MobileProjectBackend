import hashlib

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Product, Color, Category, Size, File, ProductSizes, ProductColors
from .serializers import CreateProductSerializer, ProductListSerializer, CategorySerializer, ColorSerializer, \
    SizeSerializer, FileUploadSerializer, ProductSizesSerializer, ProductAddSizesSerializer, ProductColorsSerializer, \
    ProductAddColorSerializer


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


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = ()
    serializer_class = ProductListSerializer


class ProductUpdateAPIView(RetrieveUpdateAPIView):
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
    serializer_class = CategorySerializer


class CategoryGetUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = ()
    serializer_class = CategorySerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = ()
    serializer_class = CategorySerializer


class GetCategoryByIdAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = CategorySerializer

    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        category_serializer = CategorySerializer(category)
        return Response(category_serializer.data)


class CreateColorAPIView(CreateAPIView):
    queryset = Color.objects.all()
    permission_classes = ()
    serializer_class = ColorSerializer


class ColorListAPIView(ListAPIView):
    queryset = Color.objects.all()
    permission_classes = ()
    serializer_class = ColorSerializer


class GetColorByIdAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ColorSerializer

    def get(self, request, pk):
        color = Color.objects.get(pk=pk)
        color_serializer = ColorSerializer(color)
        return Response(color_serializer.data)


class ColorGetUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Color.objects.all()
    permission_classes = ()
    serializer_class = ColorSerializer


class CreateSizeAPIView(CreateAPIView):
    queryset = Size.objects.all()
    permission_classes = ()
    serializer_class = SizeSerializer


class GetSizeByCategoryIdAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = SizeSerializer

    def get(self, request, pk):
        size = Size.objects.filter(category=pk)
        if size:
            size_serializer = SizeSerializer(size, many=True)
            return Response(size_serializer.data)
        else:
            return Response({'message': 'Not Found!'})


class SizeListAPIView(ListAPIView):
    queryset = Size.objects.all()
    permission_classes = ()
    serializer_class = SizeSerializer


class SizeGetUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
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


class ProductFileGetDelete(APIView):
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


class GetProductSizes(APIView):
    permission_classes = ()
    serializer_class = ProductSizesSerializer

    def get(self, request, pk):
        sizes = ProductSizes.objects.filter(product_id=pk)
        sizes_serializer = ProductSizesSerializer(sizes, many=True)
        return Response(sizes_serializer.data)

