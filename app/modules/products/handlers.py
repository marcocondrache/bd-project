from uuid import UUID

from flask_sqlalchemy.pagination import QueryPagination
from sqlalchemy import and_, func

from app.modules.products.models import Product, ProductCategory, Keyword
from app.modules.sellers.models import Seller
from app.modules.shared.consts import DEFAULT_PAGE_SIZE
from extensions import db

separators = "|".join([' ', '.', ',', ';', ':', '-', '!', '?', '\t', '\n'])


def get_price_max():
    """
    Get the maximum price of all products.
    :return: the maximum price
    """
    return db.session.query(func.max(Product.price)).scalar()


def get_stock_max():
    """
    Get the maximum stock of all products.
    :return: the maximum stock
    """
    return db.session.query(func.max(Product.stock)).scalar()


def get_all_product_brands():
    """
    Get all product brands.
    :return: the list of product brands
    """
    return db.session.query(Product.brand).distinct().all()


def get_all_product_categories():
    """
    Get all product categories.
    :return: the list of product categories
    """
    return ProductCategory.query.all()


def get_product_by_guid(guid: UUID) -> Product | None:
    """
    Get a product by its guid. If the product doesn't exist, return None.
    :param guid: the guid of the product
    :return: the product or None if it doesn't exist
    """
    return Product.query.filter_by(guid=guid, deleted_at=None).first()


def get_all_products(page: int = 1, per_page: int = DEFAULT_PAGE_SIZE, filters=()) -> QueryPagination:
    """
    Get all products paginated. The products are ordered by name.
    :param page: the page number
    :param per_page: the number of products per page
    :param filters: the filters to apply
    :return: the products paginated
    """
    query = Product.query.filter(*filters).order_by(Product.name)
    return query.paginate(page=page, per_page=per_page)


def get_products_filtered(query_key: str, page: int = 1, per_page: int = DEFAULT_PAGE_SIZE, filters=()) -> QueryPagination:
    """
    Get products filtered by a query key. The products are paginated.
    :param query_key: the query key to filter the products
    :param page: the page number
    :param per_page: the number of products per page
    :param filters: the filters to apply
    :return: the products filtered and paginated
    """
    query = (Product.query.join(Product.keywords)
             .filter(Keyword.key.ilike(f'%{query_key}%'))
             .filter(and_(*filters)).order_by(Product.name))
    return query.paginate(page=page, per_page=per_page)


def get_seller_products(
        seller_id: int, show_sold_out: bool = False,
        page: int = 1, per_page: int = DEFAULT_PAGE_SIZE
) -> QueryPagination:
    """
    Get the products of a seller. The products are paginated. If show_sold_out is False, only products with stock > 0
    :param seller_id: the id of the seller
    :param show_sold_out: whether to show sold out products
    :param page: the page number
    :param per_page: the number of products per page
    :return: the products of the seller paginated
    """
    query = Product.query.filter_by(owner_seller_id=seller_id, deleted_at=None).order_by(Product.name)

    if not show_sold_out:
        query = query.filter(Product.stock > 0)

    return query.paginate(page=page, per_page=per_page)


def create_product(
        seller_id: int, name: str, price: float, stock: int, categories: list,
        description: str = None, brand: str = None, is_second_hand: bool = False
) -> Product | None:
    """
    Create a product. If the seller doesn't exist, return None.
    :param seller_id: the id of the seller
    :param name: the name of the product
    :param price: the price of the product
    :param stock: the stock of the product
    :param categories: the categories of the product
    :param description: the description of the product
    :param brand: the brand of the product
    :param is_second_hand: whether the product is second hand
    :return: the product or None if the seller doesn't exist
    """
    seller = Seller.query.filter_by(id=seller_id).first()
    if not seller:
        return None

    product = Product(
        owner_seller_id=seller_id,
        name=name,
        description=description,
        brand=brand,
        is_second_hand=is_second_hand,
        price=price,
        currency="EUR",
        stock=stock,
    )

    # add categories if not exists
    for category_name in categories:
        category = ProductCategory.query.filter_by(name=category_name).first()
        if not category:
            category = ProductCategory(name=category_name)
            db.session.add(category)
        product.categories.append(category)

    # add keywords if not exists
    keywords = [k.lower() for k in (
        name.split(separators) +
        description.split(separators) if description else [] + brand.split(separators) if brand else []
    ) if len(k) > 2]
    for keyword_key in keywords:
        keyword = Keyword.query.filter_by(key=keyword_key).first()
        if not keyword:
            keyword = Keyword(key=keyword_key, reference_count=1)
            db.session.add(keyword)
        else:
            keyword.reference_count += 1
        product.keywords.append(keyword)

    db.session.add(product)
    db.session.commit()
    return product


def update_product(
        product: Product, price: float, stock: int, categories: list, description: str
):
    """
    Update a product.
    :param product: the product to update
    :param price: the new price
    :param stock: the new stock
    :param categories: the new categories, the categories are created if they don't exist
    :param description: the new description
    :return: the updated product
    """
    product.price = price
    product.stock = stock
    product.description = description

    for category_name in categories:
        category = ProductCategory.query.filter_by(name=category_name).first()
        if category is None:
            category = ProductCategory(name=category_name)
            db.session.add(category)
        if category not in product.categories:
            product.categories.append(category)

    product.sequence += 1

    db.session.commit()
    return product


def delete_product(product: Product):
    """
    Delete a product. The product and its reservations are marked as deleted.
    :param product: the product to delete
    :return: the deleted product
    """
    product.sequence += 1
    product.deleted_at = db.func.now()
    for reservation in product.reservations:
        reservation.deleted_at = db.func.now()

    db.session.commit()
    return product
