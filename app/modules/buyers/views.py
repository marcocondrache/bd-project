from app.modules.buyers import buyers
from app.modules.buyers.handlers import update_buyer

from flask_login import login_required, current_user
from flask import request


@buyers.route('', methods=['PUT'])
@login_required
def edit_buyer():
    current_user_id = current_user.id
    data = request.get_json()
    destination_address = data.get('destination_address')
    card_number = data.get('card_number')
    if not destination_address or not card_number:
        return {'message': 'destination_address and card_number are required'}, 400
    buyer = update_buyer(current_user_id, destination_address, card_number)
    if not buyer:
        return {'message': 'buyer not found'}, 404
    
    return {'message': 'buyer updated'}, 200
