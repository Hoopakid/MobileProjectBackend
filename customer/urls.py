from django.urls import path

from customer.views import DiscountProductAPIView, ShippignAddressAPIView

urlpatterns = [
    path('shipping_address/', ShippignAddressAPIView.as_view(), name='shipping-address'),
    path('discount_product/', DiscountProductAPIView.as_view(), name='discount-product'),
]