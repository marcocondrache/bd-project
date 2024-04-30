from uuid import UUID

from flask import abort

from app.modules.carts.models import CartStatus, Cart, ProductReservation
from app.modules.products.models import Product
from extensions import db


def get_cart_or_create(buyer_id: int):
    cart = Cart.query.filter_by(owner_buyer_id=buyer_id, status=CartStatus.ACTIVE).first()
    if not cart:
        cart = Cart(owner_buyer_id=buyer_id)
        db.session.add(cart)
    return cart


def update_cart(buyer_id: int, product: Product, quantity: int):
    cart = get_cart_or_create(buyer_id)
    product_reservation = cart.reservations.filter_by(product_id=product.id).first()
    if not product_reservation:
        product_reservation = ProductReservation(
            product_id=product.id,
            product_sequence=product.sequence,
            quantity=quantity,
            cart=cart
        )
        cart.reservations.append(product_reservation)
        db.session.commit()
        return cart

    if product.sequence != product_reservation.product_sequence:
        db.session.rollback()  # Or delete the product_reservation?
        abort(400, "Product sequence has changed")

    product_reservation.quantity = quantity
    db.session.commit()
    return cart
