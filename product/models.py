from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.urls import reverse
from account.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def add_product(self, product):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    def total_items(self):
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0

class Product(BaseModel):
    MAX_IMAGES = 20

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
        return reverse('product_detail', kwargs={'product_pk': self.pk})

    def remaining_image_slots(self):
        if not self.pk:
            return self.MAX_IMAGES

        return max(self.MAX_IMAGES - self.images.count(), 0)

class Image(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"Image for {self.product.title}"

    def clean(self):
        super().clean()

        if not self.product_id:
            return

        images = self.product.images.all()
        if self.pk:
            images = images.exclude(pk=self.pk)

        if images.count() >= Product.MAX_IMAGES:
            raise ValidationError({
                'image': f'A product can have up to {Product.MAX_IMAGES} images.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_cart_product',
            ),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in {self.cart.user.username}'s cart"