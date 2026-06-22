from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.core.paginator import Paginator

from Marketplace.pagination import get_compact_page_range
from account.mixins import LoginRequiredMixin

from .forms import ProductForm
from .mixins import CartOwnerRequiredMixin, ProductOwnerRequiredMixin
from .models import Image, Product, Cart, CartItem


def _is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


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
    def get(self, request, product_pk):
        product = get_object_or_404(
            Product.objects.select_related('user').prefetch_related('images'),
            pk=product_pk,
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
    def get(self, request, product_pk):
        return render(request, 'product/product_update.html', {
            'product_form': ProductForm(instance=self.product),
            'product': self.product,
        })

    def post(self, request, product_pk):
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
    def get(self, request, product_pk):
        return render(request, 'product/product_confirm_delete.html', {
            'product': self.product,
        })

    def post(self, request, product_pk):
        self.product.delete()
        return redirect('product_list')

class MyCartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return redirect('cart_detail', cart_pk=cart.pk)


class CartDetailView(CartOwnerRequiredMixin, View):
    def get(self, request, cart_pk):
        cart = Cart.objects.prefetch_related(
            'items',
            'items__product',
            'items__product__images',
        ).get(pk=self.cart.pk)

        return render(request, 'product/cart_detail.html', {
            'cart': cart,
            'items': cart.items.all(),
        })


class CartItemUpdateView(CartOwnerRequiredMixin, View):
    def post(self, request, cart_pk, item_pk):
        item = get_object_or_404(CartItem, pk=item_pk, cart=self.cart)

        try:
            quantity = int(request.POST.get('quantity', item.quantity))
        except (TypeError, ValueError):
            if _is_ajax(request):
                return JsonResponse({'ok': False, 'error': 'Invalid quantity'}, status=400)
            return redirect('cart_detail', cart_pk=cart_pk)

        if quantity <= 0:
            item.delete()
            cart_count = self.cart.total_items()
            if _is_ajax(request):
                return JsonResponse({
                    'ok': True,
                    'removed': True,
                    'cart_count': cart_count,
                })
            return redirect('cart_detail', cart_pk=cart_pk)

        item.quantity = quantity
        item.save()
        cart_count = self.cart.total_items()
        subtotal = item.product.price * item.quantity

        if _is_ajax(request):
            return JsonResponse({
                'ok': True,
                'quantity': item.quantity,
                'cart_count': cart_count,
                'subtotal': str(subtotal),
                'currency': item.product.get_currency_display(),
            })
        return redirect('cart_detail', cart_pk=cart_pk)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.add_product(product)
        cart_count = cart.total_items()

        if _is_ajax(request):
            return JsonResponse({
                'ok': True,
                'cart_count': cart_count,
                'product_title': product.title,
            })

        return redirect(product.get_absolute_url())