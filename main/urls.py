from django.urls import path

from main.views import *

urlpatterns = [
    path('add-product', CreateProductAPIView.as_view(), name='add-product'),
    path('add-category', CreateCategoryAPIView.as_view(), name='add-category'),
    path('add-color', CreateColorAPIView.as_view(), name='add-color'),
    path('add-size', CreateSizeAPIView.as_view(), name='add-size'),
    path('product-get-update-delete/<int:pk>', ProductUpdateAPIView.as_view(), name='product-get'),
    path('category-get/<int:pk>', CategoryGetAPIView.as_view(), name='category-get'),
    path('color-get/<int:pk>', ColorGetAPIView.as_view(), name='color-get'),
    path('size-get/<int:pk>', SizeGetAPIView.as_view(), name='size-get'),
    path('get-product-sizes/<int:pk>', GetProductSizes.as_view(), name='get-product-sizes'),
    path('get-product-color-by-size-id/', GetColorByProductSizeId.as_view(), name='get-product_color-by-size_id'),
    path('add-product-size-color', AddProductSizeColor.as_view(), name='add-product-size-color'),
    path('get-products-by-category_id/<int:category_id>', GetProductsByCategoryIdAPIView.as_view(), name='get-products'),
    path('get-product-files/<int:pk>', ProductFileGetDelete.as_view(), name='get-product-files'),
    path('get-categories', CategoryListAPIView.as_view(), name='get-categories'),
    path('get-colors', ColorListAPIView.as_view(), name='get-colors'),
    path('get-sizes', SizeListAPIView.as_view(), name='get-sizes'),
    path('upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
]
