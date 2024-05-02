from app.modules.carts.models import CartStatus, Cart, ProductReservation
from app.modules.products.models import Product
from extensions import db


def get_cart_by_buyer(buyer_id: int) -> Cart | None:
    return Cart.query.filter_by(owner_buyer_id=buyer_id, status=CartStatus.ACTIVE).first()


def get_cart_or_create(buyer_id: int) -> Cart | None:
    cart = get_cart_by_buyer(buyer_id)
    if not cart:
        cart = Cart(owner_buyer_id=buyer_id)
        db.session.add(cart)
    return cart


def get_cart_products(cart: Cart) -> list[Product]:
    if not cart:
        return []
    return [r.product for r in cart.reservations if r.deleted_at is None]


def get_cart_product(buyer_id: int, product: Product) -> ProductReservation | None:
    cart = get_cart_by_buyer(buyer_id)
    if not cart:
        return None

    return ProductReservation.query.filter_by(product_id=product.id, cart=cart, deleted_at=None).first()


def update_cart(buyer_id: int, product: Product, quantity: int) -> (Cart | None, Product | None):
    cart = get_cart_or_create(buyer_id)
    product_reservation = ProductReservation.query.filter_by(product_id=product.id, cart=cart, deleted_at=None).first()
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

    if product.sequence != product_reservation.product_sequence:
        product_reservation.deleted_at = db.func.now()
        return None, product

    product_reservation.quantity = quantity
    db.session.commit()
    return cart, None


def remove_from_cart(buyer_id: int, product: Product) -> Cart | None:
    cart = get_cart_by_buyer(buyer_id)
    if not cart:
        return None

    product_reservation = ProductReservation.query.filter_by(product_id=product.id, cart=cart, deleted_at=None).first()
    if not product_reservation:
        return None

    product_reservation.deleted_at = db.func.now()
    db.session.commit()
    return cart
