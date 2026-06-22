from django.urls import path

from .views import (
    AddToCartView,
    CartDetailView,
    CartItemUpdateView,
    MyCartView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:product_pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:product_pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:product_pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:product_pk>/add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', MyCartView.as_view(), name='my_cart'),
    path('carts/<int:cart_pk>/', CartDetailView.as_view(), name='cart_detail'),
    path('carts/<int:cart_pk>/items/<int:item_pk>/', CartItemUpdateView.as_view(), name='cart_item_update'),
]
