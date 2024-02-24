from django.urls import path

from customer.views import (
    DiscountProductAPIView,
    ShippignAddressAPIView,
    MyFavouriteAPIView,
    DiscountProductListAPIView,
    DiscountCategoryListAPIView, DiscountCategoryAPIView
)

urlpatterns = [
    path('Favourites/', MyFavouriteAPIView.as_view(), name='favourites'),
    path('shipping_address/', ShippignAddressAPIView.as_view(), name='shipping-address'),
    path('discount_category/<int:category_id>', DiscountCategoryAPIView.as_view(), name='discount-product'),
    path('discount_category_list/', DiscountCategoryListAPIView.as_view(), name='discount-product'),
    path('discount_product/', DiscountProductAPIView.as_view(), name='discount-product-list'),
    path('discount_product_list/', DiscountProductListAPIView.as_view(), name='discount-category-list')
]