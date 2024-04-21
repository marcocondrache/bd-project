from flask import request
from flask_login import login_required, current_user

from app.modules.sellers.handlers import update_seller
from app.modules.buyers.handlers import update_buyer
from app.modules.users import users
from app.modules.users.handlers import update_user


@users.route('/', methods=['PUT'])
@login_required
def edit_user():
    password = request.form.get('password')
    destination_address = request.form.get('destination_address')
    card_number = request.form.get('card_number')
    iban = request.form.get('iban')
    show_sold_products = request.form.get('show_sold_products') == 'on'
    if not password and not destination_address and not card_number and not iban and not show_sold_products:
        return {'message': 'no data provided'}, 400

    buyer = update_buyer(current_user.id, destination_address, card_number)
    if not buyer:
        return {'message': 'buyer not found'}, 404

    seller = update_seller(current_user.id, iban, show_sold_products)
    if not seller:
        return {'message': 'seller not found'}, 404

    return {'message': 'user updated'}, 200
