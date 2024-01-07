from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    product_name = serializers.ReadOnlyField(source='product.name')
    each_price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.total_price()

    class Meta:
        model = CartItem
        fields = ['product_id', 'product_name', 'quantity', 'each_price', 'total_price']
