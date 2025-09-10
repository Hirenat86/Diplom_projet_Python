import yaml
from django.core.management.base import BaseCommand
from orders_app.models import (Category, Parameter, Product, ProductInfo,
                               ProductParameter, Shop)
from pytils.translit import slugify
from yaml.loader import SafeLoader


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        file_name = "orders/shop1.yaml"
        with open(file_name, "r", encoding="utf-8") as file:
            data = yaml.load(file, Loader=SafeLoader)

        shop, _ = Shop.objects.update_or_create(
            name=data["shop"],
        )

        for item in data["categories"]:
            category, _ = Category.objects.update_or_create(
                id=item["id"], name=item["name"], slug=slugify(item["name"])
            )
            category.shops.add(shop.id)
            category.save()

        for item in data["goods"]:
            try:
                category = Category.objects.get(id=item["category"])
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"Категория с id={item['category']} не найдена. Пропускаем товар id={item['id']}"
                    )
                )
                continue

            Product.objects.update_or_create(
                id=item["id"],
                category=category,
            )

        # наполняем модель ProductInfo
        for item in data["goods"]:
            try:
                category = Category.objects.get(id=item["category"])
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"Категория с id={item['category']} не найдена. Пропускаем товар id={item['id']}"
                    )
                )
                continue

            product, created = Product.objects.update_or_create(
                id=item["id"],
                defaults={
                    "category": category,
                    "name": item["name"],
                    "slug": slugify(item["name"]),
                },
            )
            product_info, _ = ProductInfo.objects.update_or_create(
                product_id=product.id,
                shop_id=shop.id,
                model=item["model"],
                quantity=item["quantity"],
                price=item["price"],
                price_rrc=item["price_rrc"],
            )

        for name, value in item["parameters"].items():
            parameter, _ = Parameter.objects.update_or_create(name=name)
            ProductParameter.objects.update_or_create(
                product_info_id=product_info.id, parameter_id=parameter.id, value=value
            )
