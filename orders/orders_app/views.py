from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


@login_required()
def product_list(request, category_slug=None):
    """
    Представление списка продуктов.

    Отображает список всех продуктов или фильтрует их
    по категории, если передан `category_slug`.

    Args:
        request (HttpRequest): Объект запроса.
        category_slug (str, optional): slug категории для фильтрации.
            По умолчанию None.

    Returns:
        HttpResponse: Отрендеренный шаблон product/list.html
        с данными:
            - category: выбранная категория (или None)
            - categories: все доступные категории
            - products: список продуктов
    """

    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        "orders_app/product/list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, slug):
    """
        Представление деталей продукта.

        Отображает карточку выбранного продукта и форму
        для добавления его в корзину.

        Args:
            request (HttpRequest): Объект запроса.
            id (int): ID продукта.
            slug (str): slug продукта.

        Returns:
            HttpResponse: Отрендеренный шаблон product/detail.html
            с данными:
                - product: выбранный продукт
                - cart_product_form: форма для добавления продукта в корзину
    """

    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        "orders_app/product/detail.html",
        {"product": product, "cart_product_form": cart_product_form},
    )
