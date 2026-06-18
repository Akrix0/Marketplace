from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import ProductForm
from .models import Image, Product

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product/product_list.html', {
            'products': products
            })

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('user'), pk=pk)
        return render(request, 'product/product_detail.html', {
            'product': product
            })

class ProductCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'product/product_create.html', {
            'product_form': ProductForm(),
        })

    @method_decorator(login_required)
    def post(self, request):
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()

            for image in request.FILES.getlist('image'):
                Image.objects.create(
                    product=product,
                    image=image
                )

            return redirect(product.get_absolute_url())

        return render(request, 'product/product_create.html', {
            'product_form': product_form,
        })