from django.shortcuts import get_object_or_404

from account.mixins import LoginRequiredMixin

from .models import Product, Cart


class ProductOwnerRequiredMixin(LoginRequiredMixin):
    """Restrict access to the user who created the product."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.product = get_object_or_404(
            Product, pk=kwargs['product_pk'], user=request.user
        )
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class CartOwnerRequiredMixin(LoginRequiredMixin):
    """Restrict access to the user who created the cart."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.cart = get_object_or_404(
            Cart, pk=kwargs['cart_pk'], user=request.user
        )
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

