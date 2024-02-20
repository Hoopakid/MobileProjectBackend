import os
import hashlib

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveDestroyAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Product, Color, Category, Size, File, ProductSizes, ProductColors
from .serializers import CreateProductSerializer, ProductListSerializer, CategorySerializer, ColorSerializer, \
    SizeSerializer, FileUploadSerializer, ProductSizesSerializer, ProductAddSizesSerializer, ProductColorsSerializer, \
    ProductAddColorSerializer


class CreateProductAPIView(CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = ()
    serializer_class = CreateProductSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = ()
    serializer_class = ProductListSerializer


class GetProductByIdAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductListSerializer

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        product_serializer = ProductListSerializer(product)
        return Response(product_serializer.data)


class ProductUpdateAPIView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = ()
    serializer_class = CreateProductSerializer


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


class GetProductSizes(APIView):
    permission_classes = ()
    serializer_class = ProductSizesSerializer

    def get(self, request, pk):
        sizes = ProductSizes.objects.filter(product_id=pk)
        sizes_serializer = ProductSizesSerializer(sizes, many=True)
        return Response(sizes_serializer.data)
