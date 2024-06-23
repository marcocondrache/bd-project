from flask_sqlalchemy.pagination import QueryPagination

from app.modules.carts.models import CartStatus, Cart, ProductReservation
from app.modules.products.models import Product
from app.modules.shared.consts import DEFAULT_PAGE_SIZE
from extensions import db


def get_cart_by_buyer(buyer_id: int) -> Cart | None:
    """
    Get the cart of a buyer by its id.
    :param buyer_id: the id of the buyer
    :return: the cart of the buyer or None if it doesn't exist
    """
    return Cart.query.filter_by(owner_buyer_id=buyer_id, status=CartStatus.ACTIVE).first()


def get_cart_or_create(buyer_id: int) -> Cart | None:
    """
    Get the cart of a buyer by its id. If it doesn't exist, create a new one.
    :param buyer_id: the id of the buyer
    :return: the cart of the buyer
    """
    cart = get_cart_by_buyer(buyer_id)
    if not cart:
        cart = Cart(owner_buyer_id=buyer_id)
        db.session.add(cart)
    return cart


def get_reservation_by_cart(cart: Cart, page: int = 1, per_page: int = DEFAULT_PAGE_SIZE) -> QueryPagination:
    """
    Get the reservations of a cart. The reservations are paginated.
    :param cart: the cart to get the reservations from
    :param page: the page number
    :param per_page: the number of reservations per page
    :return: the reservations of the cart
    """
    return (ProductReservation.query
            .filter_by(cart=cart, deleted_at=None)
            .order_by(ProductReservation.created_at)
            .paginate(page=page, per_page=per_page))


def get_reservation_by_product(buyer_id: int, product: Product) -> (ProductReservation | None, bool):
    """
    Get the reservation of a product in a cart. If the product is not in the cart, return None.
    :param buyer_id: the id of the buyer
    :param product: the product to get the reservation from
    :return: the reservation of the product in the cart or None if it doesn't exist, and a boolean indicating if the
    reservation has a different sequence than the product
    """
    cart = get_cart_by_buyer(buyer_id)
    if not cart:
        return None, False

    # get the reservation of the product in the cart
    product_reservation = ProductReservation.query.filter_by(product_id=product.id, cart=cart, deleted_at=None).first()
    if not product_reservation:
        return None, False

    # if the product sequence is different from the reservation sequence, delete the reservation and return None, True
    if product.sequence != product_reservation.product_sequence:
        product_reservation.deleted_at = db.func.now()
        db.session.commit()
        return None, True

    # return the reservation and False
    return product_reservation, False


def update_cart(buyer_id: int, product: Product, quantity: int) -> (Cart | None, Product | None):
    """
    Update the cart of a buyer with a product and a quantity.
    :param buyer_id: the id of the buyer
    :param product: the product to add to the cart
    :param quantity: the quantity of the product
    :return: the cart of the buyer and the product if the product has a different sequence than the reservation
    """
    cart = get_cart_or_create(buyer_id)
    product_reservation = ProductReservation.query.filter_by(product_id=product.id, cart=cart, deleted_at=None).first()

    # if the product is not in the cart, create a new reservation
    if not product_reservation:
        product_reservation = ProductReservation(
            product_id=product.id,
            product_sequence=product.sequence,
            quantity=quantity,
            cart=cart
        )
        cart.reservations.append(product_reservation)
        db.session.commit()
        return cart, None

    # if the product sequence is different from the reservation sequence, delete the reservation and return None, product
    if product.sequence != product_reservation.product_sequence:
        product_reservation.deleted_at = db.func.now()
        db.session.commit()
        return None, product

    # update the quantity of the reservation
    product_reservation.quantity = quantity
    db.session.commit()
    return cart, None


def remove_from_cart(buyer_id: int, product: Product) -> Cart | None:
    """
    Remove a product from the cart of a buyer. If the product is not in the cart, return None.
    :param buyer_id: the id of the buyer
    :param product: the product to remove from the cart
    :return: the cart of the buyer or None if the product is not in the cart
    """
    cart = get_cart_by_buyer(buyer_id)
    if not cart:
        return None

    # get the reservation of the product in the cart
    product_reservation = ProductReservation.query.filter_by(product_id=product.id, cart=cart, deleted_at=None).first()
    if not product_reservation:
        return None

    # delete the reservation
    product_reservation.deleted_at = db.func.now()
    db.session.commit()
    return cart
