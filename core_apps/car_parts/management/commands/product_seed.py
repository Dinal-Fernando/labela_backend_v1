from django.core.management.base import BaseCommand
import random
import decimal

from core_apps.car_parts.models import Product


class Command(BaseCommand):
    help = 'Seeds the database with Product data'

    def handle(self, *args, **kwargs):
        for _ in range(10):
            name = f'Product {_}'
            description = f'Description for Product {_}'
            price = decimal.Decimal(random.randrange(100, 10000)) / 100
            quantity = random.randint(1, 100)

            Product.objects.create(name=name, description=description, price=price, quantity=quantity)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with products'))
