"""
URL configuration for orders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # HTML route
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include("order_func.urls", namespace="order_func")),
    path("", include("orders_app.urls", namespace="orders_app")),
    path("account/", include("account.urls")),
    # REST API route
    path("api/orders_app/", include("orders_app.urls_api")),
    path("api/cart/", include("cart.urls_api")),
    path("api/order_func/", include("order_func.urls_api")),
    path("api/account/", include("account.urls_api")),
]
