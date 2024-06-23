import random
from concurrent.futures import ThreadPoolExecutor
from typing import List

import faker_commerce
from faker import Faker
from sqlalchemy import Connection
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from app.modules.buyers.models import Buyer
from app.modules.products.models import ProductCategory, Product, Keyword
from app.modules.reviews.models import ProductReview
from app.modules.sellers.models import Seller
from app.modules.users.models import User


def create_seller(faker, user: User):
    return Seller(iban=faker.iban(), show_soldout_products=faker.boolean(),
                  user=user)


def create_user(faker: Faker):
    email = faker.safe_email()
    password = faker.password(length=8, special_chars=False)
    print(f"Email: {email}, Password: {password}")

    return User(email=email, given_name=faker.first_name(),
                family_name=faker.last_name(),
                password=generate_password_hash(password))


def create_buyer(faker, user):
    return Buyer(destination_address=faker.address(), card_number=str(faker.credit_card_number()),
                 user=user)


def create_keywords(products: List[Product]) -> List[Keyword]:
    # create a mapping of keywords to products, the keywords are the product name split by spaces
    keywords = {}
    for product in products:
        # include the brand in the keywords and the name of the product itself
        for word in set(product.name.split() + product.brand.split() + [product.name]):
            if word not in keywords:
                keywords[word] = []
            keywords[word].append(product)

    # create the keywords
    for word, products in keywords.items():
        keyword = Keyword(key=word, reference_count=len(products))
        keyword.products = products
        yield keyword


def create_product(faker, seller):
    return Product(owner_seller_id=seller.id,
                   name=faker.ecommerce_name(),
                   description=faker.text(),
                   brand=faker.company(),
                   is_second_hand=faker.boolean(),
                   price=faker.ecommerce_price(),
                   currency="EUR",
                   stock=random.randint(0, 200), )


class Populate(object):
    faker = Faker()

    def __init__(self, db: Connection):
        self.session = sessionmaker(bind=db)()
        self.faker.add_provider(faker_commerce.Provider)
        self.executor = ThreadPoolExecutor()

    def populate(self):
        self.__populate_users()
        self.__populate_categories()
        self.__populate_products()

        self.session.close()

    def __populate_users(self):
        futures = [self.executor.submit(create_user, self.faker) for _ in range(200)]
        users = [future.result() for future in futures]

        futures = [self.executor.submit(create_buyer, self.faker, user) for user in users]
        buyers = [future.result() for future in futures]

        futures = [self.executor.submit(create_seller, self.faker, user) for user in users[:100]]
        sellers = [future.result() for future in futures]

        self.session.add_all(users)
        self.session.add_all(buyers)
        self.session.add_all(sellers)
        self.session.commit()

    def __populate_categories(self):
        categories = self.session.query(ProductCategory).all()

        for category in categories:
            if category.name in faker_commerce.CATEGORIES:
                return

        self.session.add_all([ProductCategory(name=c) for c in faker_commerce.CATEGORIES])
        self.session.commit()

    def __populate_products(self):
        categories = self.session.query(ProductCategory).all()
        sellers = self.session.query(Seller).all()
        products = []

        for seller in sellers:
            for _ in range(20):
                product = create_product(self.faker, seller)
                product.categories = random.choices(categories, k=3)
                self.session.add(product)
                products.append(product)

        keywords = list(create_keywords(products))
        self.session.add_all(keywords)
        self.session.commit()
