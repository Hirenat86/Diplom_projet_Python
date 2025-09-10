from rest_framework.routers import DefaultRouter
from .views_api import CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = router.urls

