from django.db import models

from core_apps.car_parts.models import Product


class Cart(models.Model):
    session_key = models.CharField(max_length=40)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart: {self.id} , Session: {self.session_key}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class Order(models.Model):
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_email = models.EmailField(default=None, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ordered_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()

    def __str__(self):
        return f'Order {self.id} - {self.ordered_at.strftime("%Y-%m-%d")}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
