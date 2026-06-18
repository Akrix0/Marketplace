from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from .models import Account


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    pass


class AnonymousRequiredMixin:
    """Redirect authenticated users away from login/register pages."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.user.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class AccountOwnerRequiredMixin(LoginRequiredMixin):
    """Restrict access to the account owner."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.account = get_object_or_404(
            Account, slug=kwargs['slug'], pk=request.user.pk
        )
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
