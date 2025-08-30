import yaml
from yaml.loader import SafeLoader

from django.core.management.base import BaseCommand
from orders.orders_app.models import Shop, Category, Product, ProductInfo, Parameter, \
    ProductParameter


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        file_name = 'shop1.yaml'
        with open(file_name, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=SafeLoader)

        # наполняем модель Shop
        Shop.objects.create(
            name=data['shop'],
            filename=file_name,)

        # наполняем модель Category
        for item in data['categories']:
            Category.objects.create(
                id=item['id'],
                name=item['name'],
                #shops= ?
            )

        # наполняем модель Product
        for item in data['goods']:
            Product.objects.create(
                id=item['id'],
                category=item['category'],
            )

        # наполняем модель ProductInfo
        for item in data['goods']:
            ProductInfo.objects.create(
                # product= ?
                # shop= ?
                # name = ?
                model=item['model'],
                quantity=item['quantity'],
                price=item['price'],
                price_rrc=item['price_rrc']
            )

        # наполняем модель Parameter, ProductParameter
        for item in data['goods']:

            params_dict = item['parameters']
            for parameter in list(params_dict.keys()):
                Parameter.objects.create(
                    name=parameter
                )

                ProductParameter.objects.create(
                    # product_info = ?
                    # parameter = ?
                    value=params_dict[parameter]
                )