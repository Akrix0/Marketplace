from django.db import models
from django.urls import reverse

class Product(models.Model):
    title = models.CharField(max_length=128)
    price = models.SmallIntegerField()
    valute = models.CharField(max_length=16, choices = {
        "Euro": "€",
        "Dollar": "$",
        "Hryvnia": "₴",
    }, default="Euro")
    status = models.CharField(max_length=16, choices = {
        "In stock": "In stock",
        "No information": "No information",
        "Out of stock": "Out of stock",
    }, default="No information")
    description = models.TextField(default="No description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return f"{self.title} - {self.price} {self.valute}"

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        verbose_name = ("Image")
        verbose_name_plural = ("Images")

    def __str__(self):
        return f"Image for {self.product.title}"