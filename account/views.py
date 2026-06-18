from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import AccountAuthenticationForm, AccountCreationForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:account')
        return render(request, 'account/login.html', {
            'form': AccountAuthenticationForm(),
        })

    def post(self, request):
        form = AccountAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('account:account')
        messages.error(request, 'Invalid credentials')
        return render(request, 'account/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:account')
        return render(request, 'account/register.html', {
            'form': AccountCreationForm(),
        })

    def post(self, request):
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('account:account')
        return render(request, 'account/register.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('account:login')

    def get(self, request):
        logout(request)
        return redirect('account:login')


class AccountView(View):
    @method_decorator(login_required)
    def get(self, request):
        products = request.user.products.prefetch_related('images').order_by('-created_at')
        return render(request, 'account/account.html', {
            'products': products,
        })
