from app.modules.products.models import Product
from app.modules.sellers.models import Seller
from extensions import db

separators = "|".join([' ', '.', ',', ';', ':', '-', '!', '?', '\t', '\n'])


# TODO: Implement paginated query
def get_products(seller_id: int = None):
    return Product.query.filter_by(owner_seller_id=seller_id).all()


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
    for category in categories:
        product.categories.append(category)

    # add keywords if not exists
    for keyword in [keywords for keywords in name.split(separators) if len(keywords) > 3]:
        product.keywords.append(keyword)

    db.session.add(product)
    db.session.commit()
    return product
