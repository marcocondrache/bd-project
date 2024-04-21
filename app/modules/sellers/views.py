from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.modules.sellers import sellers
from app.modules.sellers.handlers import create_seller


@sellers.route('/register', methods=['GET', 'POST'])
@login_required
def seller_registration():
    if request.method == 'POST':
        iban = request.form.get('iban')
        show_sold_products = request.form.get('show_sold_products') == 'on'

        # create seller
        seller = create_seller(current_user.id, iban, show_sold_products)
        if not seller:
            flash('Seller not created')
        else:
            return redirect(url_for('home.index'))
    return render_template('sellers/register.html')
