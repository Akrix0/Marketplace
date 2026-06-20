from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.core.paginator import Paginator

from Marketplace.pagination import get_compact_page_range
from account.mixins import LoginRequiredMixin

from .forms import ProductForm
from .mixins import ProductOwnerRequiredMixin
from .models import Image, Product


class ProductListView(View):
    def get(self, request):
        products = Product.objects.prefetch_related('images').order_by('-created_at')
        paginator = Paginator(products, 8)
        product_page = paginator.get_page(request.GET.get('page'))
        return render(request, 'product/product_list.html', {
            'product_page': product_page,
            'product_page_range': get_compact_page_range(product_page),
            'product_count': paginator.count,
        })



class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('user').prefetch_related('images'),
            pk=pk,
        )
        images = list(product.images.all())
        return render(request, 'product/product_detail.html', {
            'product': product,
            'images': images,
            'image_count': len(images),
            'is_owner': request.user.is_authenticated and request.user.pk == product.user_id,
        })


class ProductCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'product/product_create.html', {
            'product_form': ProductForm(),
        })

    def post(self, request):
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()

            for image in request.FILES.getlist('image')[:Product.MAX_IMAGES]:
                Image.objects.create(
                    product=product,
                    image=image,
                )

            return redirect(product.get_absolute_url())

        return render(request, 'product/product_create.html', {
            'product_form': product_form,
        })


class ProductUpdateView(ProductOwnerRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'product/product_update.html', {
            'product_form': ProductForm(instance=self.product),
            'product': self.product,
        })

    def post(self, request, pk):
        product_form = ProductForm(request.POST, instance=self.product)

        if product_form.is_valid():
            product = product_form.save()

            for image in request.FILES.getlist('image')[:product.remaining_image_slots()]:
                Image.objects.create(
                    product=product,
                    image=image,
                )

            return redirect(product.get_absolute_url())

        return render(request, 'product/product_update.html', {
            'product_form': product_form,
            'product': self.product,
        })


class ProductDeleteView(ProductOwnerRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'product/product_confirm_delete.html', {
            'product': self.product,
        })

    def post(self, request, pk):
        self.product.delete()
        return redirect('product_list')
