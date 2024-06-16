from flask import render_template, request
from flask_login import login_required, current_user
from app.modules.shared.utils import seller_required
from app.modules.shipments import shipments
from app.modules.shipments.handlers import get_shipments_by_seller


@shipments.route("", methods=['GET'])
@login_required
@seller_required
def index_view():
    """
    Shows the shipments view. The user must be a seller.
    :return: The shipments view.
    """

    page = request.args.get('page', 1, type=int)
    shipment_items = get_shipments_by_seller(current_user.sellers[0].id, page=page)

    return render_template(
        'shipments/list.html',
        shipments=shipment_items,
    )


@shipments.route("/<str:shipment_uuid>", methods=['GET'])
def detail_view(shipment_uuid: str):
    """
    Shows the shipment detail view.
    :param shipment_uuid: The shipment UUID.
    :return: The shipment detail view.
    """

    shipment = get_shipment_by_uuid(shipment_uuid)

    return render_template(
        'shipments/details.html',
        shipment=shipment,
    )
