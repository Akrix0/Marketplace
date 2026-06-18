from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from Marketplace.pagination import get_compact_page_range

from .forms import AccountAuthenticationForm, AccountCreationForm, AccountUpdateForm
from .mixins import AccountOwnerRequiredMixin, AnonymousRequiredMixin, LoginRequiredMixin
from .models import Account


class LoginView(AnonymousRequiredMixin, View):
    def get(self, request):
        return render(request, 'account/login.html', {
            'form': AccountAuthenticationForm(),
        })

    def post(self, request):
        form = AccountAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(user.get_absolute_url())
        messages.error(request, 'Invalid credentials')
        return render(request, 'account/login.html', {'form': form})


class RegisterView(AnonymousRequiredMixin, View):
    def get(self, request):
        return render(request, 'account/register.html', {
            'form': AccountCreationForm(),
        })

    def post(self, request):
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect(user.get_absolute_url())
        return render(request, 'account/register.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('account:login')

    def get(self, request):
        logout(request)
        return redirect('account:login')


class AccountMeRedirectView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect(request.user.get_absolute_url())


class AccountView(View):
    def get(self, request, slug):
        account = get_object_or_404(Account, slug=slug)
        products = account.products.prefetch_related('images').order_by('-created_at')
        product_paginator = Paginator(products, 8)
        product_page = product_paginator.get_page(request.GET.get('products_page'))
        return render(request, 'account/account.html', {
            'account': account,
            'product_page': product_page,
            'product_page_range': get_compact_page_range(product_page),
            'product_count': product_paginator.count,
            'is_owner': request.user.is_authenticated and request.user.pk == account.pk,
        })


class AccountUpdateView(AccountOwnerRequiredMixin, View):
    def get(self, request, slug):
        return render(request, 'account/account_edit.html', {
            'form': AccountUpdateForm(instance=self.account),
            'account': self.account,
        })

    def post(self, request, slug):
        form = AccountUpdateForm(request.POST, instance=self.account)

        if form.is_valid():
            account = form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect(account.get_absolute_url())

        return render(request, 'account/account_edit.html', {
            'form': form,
            'account': self.account,
        })
