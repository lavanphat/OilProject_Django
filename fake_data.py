import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'OilProject.settings')

import django

django.setup()

from faker import Faker
from product.models import Category, Brand, Product

fakegen = Faker()


def category(n=5):
    for entry in range(n):
        fake_name = fakegen.name()

        category = Category.objects.get_or_create(title=fake_name)[0]


def brand(n=5):
    for entry in range(n):
        fake_name = fakegen.first_name()
        cate = Category.objects.all()
        brand = Brand.objects.get_or_create(title=fake_name, Category=random.choice(cate))


def product(n=5):
    for entry in range(n):
        fake_name = fakegen.name()
        fake_price_import = int(random.randrange(0, 100)[1])
        fake_price_old = int(random.randrange(0, 100)[1])
        fake_price_new = int(random.randrange(0, 100)[1])
        fake_wage = int(random.randrange(0, 100)[1])
        fake_quality = int(random.randrange(0, 100)[1])
        decription = fakegen.paragraph()
        brand = Brand.objects.all()
        category = Product.objects.get_or_create(Brand=random.choices(brand), title=fake_name, Wage=fake_wage,
                                                 Quality=fake_quality, Price_Import=fake_price_import,
                                                 Decription=decription, Price_Old=fake_price_old,
                                                 Price_New=fake_price_new)


if __name__ == '__main__':
    print('đang fake')
    # brand(5)
    product(20)
    print('xong')
