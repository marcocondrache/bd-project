from flask import request
from flask_login import login_required, current_user

from app.modules.buyers.handlers import update_buyer
from app.modules.sellers.handlers import update_seller
from app.modules.users import users


@users.route('', methods=['PUT'])
@login_required
def edit_user():
    """
    Edit the user. The user can be a buyer or a seller.
    :return: the updated user
    """
    destination_address = request.json.get('destination_address')
    card_number = request.json.get('card_number')
    iban = request.json.get('iban')
    show_sold_products = request.json.get('show_soldout')

    # Update the buyer
    buyer = update_buyer(current_user.id, destination_address, card_number)
    if not buyer:
        return {'message': 'buyer not found'}, 404

    # Update the seller if the user is a seller
    if current_user.sellers:
        seller = update_seller(current_user.id, iban, show_sold_products)
        if not seller:
            return {'message': 'seller not found'}, 404

    return {'message': 'user updated'}, 200
