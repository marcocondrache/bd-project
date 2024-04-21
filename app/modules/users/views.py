from flask import request

from app.modules.sellers.handlers import update_seller
from app.modules.buyers.handlers import update_buyer
from app.modules.users import users
from app.modules.users.handlers import update_user


@users.route('/<guid>', methods=['PUT'])
def edit_user(guid):
    password = request.form.get('password')
    destination_address = request.form.get('destination_address')
    card_number = request.form.get('card_number')
    iban = request.form.get('iban')
    show_sold_products = request.form.get('show_sold_products') == 'on'
    if not password and not destination_address and not card_number and not iban and not show_sold_products:
        return {'message': 'no data provided'}, 400

    user = update_user(guid, password)
    if not user:
        return {'message': 'user not found'}, 404

    buyer = update_buyer(guid, destination_address, card_number)
    if not buyer:
        return {'message': 'buyer not found'}, 404

    seller = update_seller(guid, iban, show_sold_products)
    if not seller:
        return {'message': 'seller not found'}, 404

    return {'message': 'user updated'}, 200
