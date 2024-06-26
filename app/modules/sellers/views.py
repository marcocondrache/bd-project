from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.modules.sellers import sellers
from app.modules.sellers.handlers import create_seller
from extensions import csrf


@sellers.route('/register', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def register_view():
    """
    Register a seller. The user must not be a seller.
    :return:
    """
    # handling form submission
    if request.method == 'POST':
        iban = request.form.get('iban')
        show_sold_products = request.form.get('show_sold_products') == 'on'

        # create seller
        seller = create_seller(current_user.id, iban, show_sold_products)
        if not seller:
            flash('An error occurred, seller not created')
        else:
            return redirect(url_for('home.index_view'))

    if current_user.sellers:
        return redirect(url_for('home.index_view'))

    return render_template('sellers/register.html')
