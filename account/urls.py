from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.AccountMeRedirectView.as_view(), name='account_me'),
    path('<slug:slug>/edit/', views.AccountUpdateView.as_view(), name='account_edit'),
    path('<slug:slug>/', views.AccountView.as_view(), name='account'),
]
