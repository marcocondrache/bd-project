from typing import List

from app.modules.buyers.models import Buyer
from app.modules.orders.models import OrderReport
from app.modules.products.models import Product
from app.modules.reviews.models import ProductReview

from app.modules.products.handlers import get_product_by_guid

from extensions import db

from uuid import UUID


def create_product_review(product_guid: str, rating: int, message: str, buyer: Buyer):
    """
    Create a product review for a product.
    :param product_guid: The product guid.
    :param rating: The rating.
    :param message: The message.
    :param buyer: The buyer
    :return: The product review.
    """
    product_guid = UUID(product_guid)
    product = get_product_by_guid(product_guid)
    if not product:
        raise ValueError("Product not found")

    if not can_be_reviewed(product, buyer):
        raise ValueError("Product can't be reviewed")

    product_review = ProductReview(
        product=product,
        current_rating=rating,
        current_message=message,
        buyer=buyer,
    )
    db.session.add(product_review)
    db.session.commit()
    return product_review


def get_product_review(product: Product, buyer: Buyer) -> ProductReview | None:
    """
    Get a product review for a product.
    :param product: The product.
    :param buyer: The buyer.
    :return: The product review.
    """
    return ProductReview.query.filter_by(product=product, buyer=buyer).first()


def can_be_reviewed(product: Product, buyer: Buyer) -> bool:
    """
    If exists a buyer order 
    :param product: the product to be reviewed
    :param buyer: the buyer
    :return: True if the product can be reviewed, False otherwise
    """
    filtered_order_reports: List[OrderReport] = OrderReport.query.filter_by(buyer_id=buyer.id, seller_id=product.seller.id).all()
    return any(order_report.seller_order.shipment.is_delivered()
               for order_report in filtered_order_reports if order_report.seller_order.shipment is not None) and \
        not get_product_review(product, buyer)
