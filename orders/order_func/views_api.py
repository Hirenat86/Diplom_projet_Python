from rest_framework import viewsets

from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Полноценный CRUD для заказов:
    GET /orders_func/orders/      — список заказов
    POST /orders_func/orders/     — создать заказ
    GET /orders_func/orders/{id}/ — получить один заказ
    PUT /orders_func/orders/{id}/ — обновить заказ
    DELETE /orders_func/orders/{id}/ — удалить заказ
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD для позиций заказа
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
