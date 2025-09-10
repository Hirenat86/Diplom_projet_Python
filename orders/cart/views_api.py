from django.shortcuts import get_object_or_404
from orders_app.models import Product
from rest_framework import status, viewsets
from rest_framework.response import Response

from .cart import Cart
from .serializers import CartItemSerializer


class CartViewSet(viewsets.ViewSet):
    """
    CRUD корзины через сессии:
    - list: показать корзину
    - create: добавить товар
    - update: изменить количество
    - destroy: удалить товар
    """

    def list(self, request):
        cart = Cart(request)
        items = []
        for item in cart:
            items.append(
                {
                    "product_id": item["product"].id,
                    "name": item["product"].name,
                    "quantity": item["quantity"],
                    "price": item["price"],
                }
            )
        return Response({"cart": items})

    def create(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart(request)
        product = get_object_or_404(Product, id=serializer.validated_data["product_id"])
        cart.add(
            product=product,
            quantity=serializer.validated_data["quantity"],
            override_quantity=True,
        )
        return Response({"status": "added"}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart(request)
        product = get_object_or_404(Product, id=serializer.validated_data["product_id"])
        cart.add(
            product=product,
            quantity=serializer.validated_data["quantity"],
            override_quantity=True,
        )
        return Response({"status": "updated"}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart(request)
        product = get_object_or_404(Product, id=serializer.validated_data["product_id"])
        cart.remove(product)
        return Response({"status": "removed"}, status=status.HTTP_200_OK)
