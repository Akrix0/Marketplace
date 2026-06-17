from django.urls import path
from .views import ProductDetailView, ProductListView, ProductCreateView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail")
]
