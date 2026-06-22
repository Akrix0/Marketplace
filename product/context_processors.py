from django.db.models import Sum

from .models import Cart


def cart_summary(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    return {'cart_item_count': cart_item_count}
