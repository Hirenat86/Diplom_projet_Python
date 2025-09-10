from rest_framework.routers import DefaultRouter

from .views_api import (CategoryViewSet, ProductInfoViewSet,
                        ProductParameterViewSet, ProductViewSet, ShopViewSet)

router = DefaultRouter()
router.register(r"shops", ShopViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"product_infos", ProductInfoViewSet)
router.register(r"product_parameters", ProductParameterViewSet)

urlpatterns = router.urls
