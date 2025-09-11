from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from orders_app.models import Product

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """
    Представление для добавления товара в корзину.

    Получает объект продукта по его ID, валидирует форму CartAddProductForm
    и добавляет товар в корзину (с указанным количеством и параметром
    перезаписи количества).

    Args:
        request (HttpRequest): Объект запроса (должен содержать POST-данные).
        product_id (int): ID продукта, который нужно добавить.

    Returns:
        HttpResponseRedirect: перенаправление на страницу корзины
        ("cart:cart_detail").
    """

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, quantity=cd["quantity"], override_quantity=cd["override"]
        )
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """
    Представление для удаления товара из корзины.

    Получает объект продукта по его ID и удаляет его из корзины.

    Args:
        request (HttpRequest): Объект запроса.
        product_id (int): ID продукта, который нужно удалить.

    Returns:
        HttpResponseRedirect: перенаправление на страницу корзины
        ("cart:cart_detail").
    """

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    """
    Представление для отображения содержимого корзины.

    Для каждого товара в корзине добавляется форма обновления количества.
    Возвращает страницу с деталями корзины.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: шаблон "cart/detail.html" с данными корзины.
    """

    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(request, "cart/detail.html", {"cart": cart})
