from django.shortcuts import get_object_or_404

from account.mixins import LoginRequiredMixin

from .models import Product


class ProductOwnerRequiredMixin(LoginRequiredMixin):
    """Restrict access to the user who created the product."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.product = get_object_or_404(
            Product, pk=kwargs['pk'], user=request.user
        )
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
