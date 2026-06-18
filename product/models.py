from django.db import models
from django.urls import reverse
from account.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=16, choices = [
        ("Euro", "€"),
        ("Dollar", "$"),
        ("Hryvnia", "₴"),
    ], default="Dollar")
    status = models.CharField(max_length=16, choices = [
        ("In stock", "In stock"),
        ("No information", "No information"),
        ("Out of stock", "Out of stock"),
    ], default="No information")
    description = models.TextField(default="No description")


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.title} - {self.price} {self.currency}"
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

class Image(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"Image for {self.product.title}"