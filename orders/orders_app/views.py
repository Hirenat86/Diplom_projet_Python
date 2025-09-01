from rest_framework.viewsets import ModelViewSet
from .models import ProductInfo, Product
from .serializers import ProductInfoSerializer


class ProductInfoViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer