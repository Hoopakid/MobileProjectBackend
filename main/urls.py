from django.urls import path

from main.views import CreateProductAPIView, ProductListAPIView, ProductUpdateAPIView, \
    CreateCategoryAPIView, CategoryListAPIView, CategoryGetUpdateDeleteAPIView, CreateColorAPIView, ColorListAPIView, \
    ColorGetUpdateDeleteAPIView, CreateSizeAPIView, SizeListAPIView, SizeGetUpdateDeleteAPIView, GetProductByIdAPIView, \
    GetCategoryByIdAPIView, GetColorByIdAPIView, GetSizeByCategoryIdAPIView, FileUploadAPIView, ProductFileGetDelete, \
    GetProductSizes

urlpatterns = [
    path('add-product', CreateProductAPIView.as_view(), name='add-product'),
    path('add-category', CreateCategoryAPIView.as_view(), name='add-category'),
    path('add-color', CreateColorAPIView.as_view(), name='add-color'),
    path('add-size', CreateSizeAPIView.as_view(), name='add-size'),
    path('product-get-update-delete/<int:pk>', ProductUpdateAPIView.as_view(), name='product-update'),
    path('category-get-update-delete/<int:pk>', CategoryGetUpdateDeleteAPIView.as_view(), name='category-update'),
    path('color-get-update-delete/<int:pk>', ColorGetUpdateDeleteAPIView.as_view(), name='color-update'),
    path('size-get-update-delete/<int:pk>', SizeGetUpdateDeleteAPIView.as_view(), name='size-update'),
    path('get-update-delete-product-size/<int:pk>', GetProductSizes.as_view(), name='get-update-delete-product-size'),
    path('get-products', ProductListAPIView.as_view(), name='get-products'),
    path('get-product-files/<int:pk>', ProductFileGetDelete.as_view(), name='get-product-files'),
    path('get-products-by-id/<int:pk>', GetProductByIdAPIView.as_view(), name='get-products-by-id'),
    path('get-categories', CategoryListAPIView.as_view(), name='get-categories'),
    path('get-category-by-id/<int:pk>', GetCategoryByIdAPIView.as_view(), name='get-category-by-id'),
    path('get-colors', ColorListAPIView.as_view(), name='get-colors'),
    path('get-color-by-id/<int:pk>', GetColorByIdAPIView.as_view(), name='get-color-by-id'),
    path('get-sizes', SizeListAPIView.as_view(), name='get-sizes'),
    path('get-size-by-category-id/<int:pk>', GetSizeByCategoryIdAPIView.as_view(), name='get-size-by-category-id'),
    path('upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
]
