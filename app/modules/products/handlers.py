from uuid import UUID

from app.modules.products.models import Product, ProductCategory, Keyword
from app.modules.sellers.models import Seller
from extensions import db

separators = "|".join([' ', '.', ',', ';', ':', '-', '!', '?', '\t', '\n'])


def get_all_product_categories():
    return ProductCategory.query.all()


# TODO: Implement paginated query
def get_products(seller_id: int = None):
    return Product.query.filter_by(owner_seller_id=seller_id).all()


def get_product_by_guid(guid: UUID):
    return Product.query.filter_by(guid=guid).first()


def get_seller_products(seller_id: int, show_sold_out: bool = False, page: int = 1, per_page: int = 10):
    query = Product.query.filter_by(owner_seller_id=seller_id).order_by(Product.created_at.desc())

    if not show_sold_out:
        query = query.filter(Product.stock > 0)

    return query.paginate(page=page, per_page=per_page)


def create_product(seller_id: int, name: str, price: float, stock: int, categories: list, description: str = None,
                   brand: str = None, is_second_hand: bool = False):
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
    keywords = [k for k in (
        name.split(separators) +
        description.split(separators) if description else [] +
        brand.split(separators) if brand else []
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
    product_id: int, price: float = None, stock: int = None, categories: list = None, description: str = None
):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return None

    if price:
        product.price = price
    if stock:
        product.stock = stock
    if description:
        product.description = description
    if categories:
        product.categories = categories

    product.sequence += 1

    db.session.commit()
    return product


def delete_product(sellers_id: int, product_guid: str):
    product = Product.query.filter_by(owner_seller_id=sellers_id, guid=product_guid).first()
    if not product:
        return None

    product.sequence += 1
    product.deleted_at = db.func.now()

    db.session.commit()
    return product
