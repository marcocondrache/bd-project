from flask import request, url_for, redirect
from flask_login import current_user

from app.modules.reviews import reviews
from app.modules.reviews.handlers import create_or_update_product_review
from app.modules.shared.utils import buyer_required


@reviews.route("/products/<product_guid>", methods=["POST"])
@buyer_required
def create_product_review_view(product_guid: str):
    """
    Create a product review for a product.
    :param product_guid: The product guid.
    :return: The product review if created, an error otherwise.
    """
    rating = int(request.form["rating"])
    message = request.form["content"]
    buyer = current_user.buyers[0]

    try:
        review = create_or_update_product_review(product_guid, rating, message, buyer)
        return redirect(url_for("products.product_view", product_guid=product_guid))
    except ValueError as e:
        return {"error": str(e)}, 400
