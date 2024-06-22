from flask import render_template, request, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm

from app.modules.shared.utils import seller_required
from app.modules.shipments import shipments
from app.modules.shipments.handlers import get_shipments_by_seller, get_shipment_by_uuid, update_shipment_status


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


@shipments.route("/<shipment_guid>", methods=['GET', 'POST'])
@login_required
@seller_required
def details_view(shipment_guid: str):
    """
    Shows the shipment detail view.
    :param shipment_guid: The shipment UUID.
    :return: The shipment detail view.
    """

    form = FlaskForm()
    shipment = get_shipment_by_uuid(shipment_guid, current_user.sellers[0].id)
    if not shipment:
        abort(404)

    if request.method == 'POST':
        shipment = update_shipment_status(shipment)

    return render_template(
        'shipments/details.html',
        shipment=shipment,
        form=form,
    )
