from rest_framework import serializers
from .models import Order, OrderItem  # Проверь реальные названия моделей у тебя

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
