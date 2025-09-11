from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

STATUS_CHOICES = (
    ("basket", "Статус корзины"),
    ("new", "Новый"),
    ("confirmed", "Подтвержден"),
    ("assembled", "Собран"),
    ("sent", "Отправлен"),
    ("delivered", "Доставлен"),
    ("canceled", "Отменен"),
)

USER_TYPE_CHOICES = (
    ("shop", "Магазин"),
    ("buyer", "Покупатель"),
)


class Shop(models.Model):
    """
        Модель магазина.

        Атрибуты:
            name (str): Название магазина.
            url (str): URL-адрес магазина (необязательный).
            user (User): Пользователь, связанный с магазином.
            filename (str): Имя файла с загруженными данными.
    """

    name = models.CharField(max_length=50, verbose_name="Название")
    url = models.URLField(verbose_name="Ссылка", null=True, blank=True)
    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    filename = models.CharField(max_length=50, verbose_name="Filename")

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Список магазинов"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
        Модель категории товаров.

        Атрибуты:
            shops (QuerySet[Shop]): Магазины, в которых есть данная категория.
            name (str): Название категории.
            slug (str): URL-friendly идентификатор категории.
    """

    shops = models.ManyToManyField(
        Shop, verbose_name="Магазины", related_name="categories", blank=True
    )
    name = models.CharField(max_length=40, verbose_name="Название")
    slug = models.SlugField(max_length=200, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "Категория"
        verbose_name_plural = "Список категорий"
        ordering = ("-name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
                Возвращает абсолютный URL категории для построения ссылок.

                Returns:
                    str: URL страницы с товарами данной категории.
        """

        return reverse("orders_app:product_list_by_category", args=[self.slug])


class Product(models.Model):
    """
        Модель продукта.

        Атрибуты:
            category (Category): Категория товара.
            name (str): Название продукта.
            slug (str): URL-friendly идентификатор продукта.
    """

    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="products",
        blank=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=80, verbose_name="Название")
    slug = models.SlugField(max_length=200, null=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Список продуктов"
        ordering = ("-name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
                Возвращает абсолютный URL продукта для построения ссылок.

                Returns:
                    str: URL страницы с деталями продукта.
        """

        return reverse("orders_app:product_detail", args=[self.id, self.slug])


class ProductInfo(models.Model):
    """
        Дополнительная информация о продукте в магазине.

        Атрибуты:
            product (Product): Продукт, к которому относится информация.
            shop (Shop): Магазин, где представлен продукт.
            model (str): Модель товара.
            quantity (int): Количество на складе.
            price (int): Цена товара.
            price_rrc (int): Рекомендуемая розничная цена.
    """

    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        related_name="product_infos",
        blank=True,
        on_delete=models.CASCADE,
    )
    shop = models.ForeignKey(
        Shop,
        verbose_name="Магазин",
        related_name="product_infos",
        blank=True,
        on_delete=models.CASCADE,
    )
    model = models.CharField(max_length=80, verbose_name="Модель")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.PositiveIntegerField(verbose_name="Цена")
    price_rrc = models.PositiveIntegerField(verbose_name="Рекомендуемая розничная цена")

    class Meta:
        verbose_name = "Информация о продукте"
        verbose_name_plural = "Информационный список о продуктах"


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название")

    class Meta:
        verbose_name = "Имя параметра"
        verbose_name_plural = "Список имен параметров"
        ordering = ("name",)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    """
        Модель значения параметра для конкретного товара.

        Атрибуты:
            product_info (ProductInfo): Ссылка на информацию о продукте.
            parameter (Parameter): Название параметра.
            value (str): Значение параметра (например, "синий", "42").
    """

    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name="Информация о продукте",
        related_name="product_parameters",
        blank=True,
        on_delete=models.CASCADE,
    )
    parameter = models.ForeignKey(
        Parameter,
        verbose_name="Параметр",
        related_name="product_parameters",
        blank=True,
        on_delete=models.CASCADE,
    )
    value = models.CharField(verbose_name="Значение", max_length=100)

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Список параметров"
