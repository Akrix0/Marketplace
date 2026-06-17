from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Image
from django.views.generic import View
from .forms import ProductForm

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product/product_list.html', {
            'products': products
            })

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'product/product_detail.html', {
            'product': product
            })

class ProductCreateView(View):
    def get(self, request):
        return render(request, 'product/product_create.html', {
            'product_form': ProductForm(),
        })

    def post(self, request):
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product = product_form.save()

            for image in request.FILES.getlist('image'):
                Image.objects.create(
                    product=product,
                    image=image
                )

            return redirect(
                'product_detail',
                pk=product.pk
            )

        return render(request, 'product/product_create.html', {
            'product_form': product_form,
        })