# Technical Analysis

The following is an analysis of the project requirements and the technical
implementation.
It's organized by the entities in action and the actions
that can be performed for each entity.
Each action has:

- a description of the input parameters (required or not)
- the result of the action
- the context from which the action can be performed;
- the flow of the action, divided into steps
  (with the italicized steps being the changes in the database).

## Auth flow

The user can do the following actions:

### Register

**Input**: (email*, password*, given name*, family name*, card number*,
destination address*)

**Output**: Redirect

**From**: welcome page

**Flow**:

- The user must provide an email, password, given name, family name, a card
  number, destination address.
- _A new user entity is created._
- _A new buyer entity is created._
- _A new session is created._
- The user is logged in and redirected to the home page.

### Register as a seller

**Input**: (IBAN*, "show sold-out products" options)

**Output**: User

**From**: profile page, "become a seller" page

**Flow**:

- The user must provide an IBAN, optionally the "show sold-out products" option.
- _A new seller entity is created._

### Login

**Input**: (email*, password*)

**Output**: Redirect

**From**: welcome page, "login" form

**Flow**:

- The user must provide an email and password.
- _A new session is created._
- The user is logged in and redirected to the home page.

### Logout

**Input**: None

**Output**: Redirect

**From**: any protected page

**Flow**:

- _The session is deleted._
- The user is redirected to the welcome page.

## User

The user can do the following actions:

### Update profile

**Input**: (password, IBAN, show sold-out products, card number, destination
address)

**Output**: User

**From**: profile page

**Flow**:

- If the user is a seller, the IBAN and show sold-out products options are
  shown.
- If the user is a buyer, the card number and destination address options are
  shown.
- The user can update the password and the other options according to the role.
- _The user entity is updated._
- _The buyer or seller entity is updated._

> Update: the password cannot be updated.

### Delete profile

**Input**: (guid*)

**Output**: None

**From**: profile page

**Flow**:

- The user must confirm the deletion.
- _Deleted_at is set to the current timestamp._
- _The session is deleted._
- The user is redirected to the welcome page.

### Search for other users (?)

## Product

The user can do the following actions:

### Create product

**Input**:
(name*, price*, quantity*, categories*, description, brand, is second-hand)

**Output**: Product

**From**: product creation page, **only for sellers**

**Flow**:

- The user must provide a name, price, quantity, categories.
- Optionally, the user can provide a description, brand, "is second-hand"
  option.
- The currency is defaulted to the EURO.
- _A new product entity is created._
- _The keywords in the product text fields are saved._
- If the categories do not exist, _new category entities are created._
- _New product-category associations are created._

### Update product

**Input**: (price, quantity, categories, description)

**Output**: Product

**From**: product page, **only for sellers**

**Flow**:

- If the product is not locked by a non-zero `locked_stock`, the user can
  update the product.
- The user can update the price, quantity, categories, description.
- _The product entity is updated._
- _The product sequence is incremented._ (for the product reservation)
- If the categories do not exist, _new category entities are created._
- _New product-category associations are created._
- _The history is triggered._

> The product's `product_reservation` becomes invalid

### Delete product

**Input**: (guid)

**Output**: None

**From**: product page, **only for sellers**

**Flow**:

- If the product is not locked by a non-zero `locked_stock`, the user can
  delete the product.
- The user must confirm the deletion.
- _Deleted_at is set to the current timestamp._
- _The product sequence is incremented._
- _The history is triggered._

> The product's `product_reservation` becomes invalid

### Search for products

**Input**: (query*, categories, brand, price range, amount range)

**Output**: List of products

**From**: home page, search bar

**Flow**:

- The user can search for products by providing a query.
- _The query is broken up into keywords._
- _The products are filtered by the keywords._
- The list of products is displayed, along with optional filters.
- The user can filter the products by categories, brand, price range, amount
  range.
- _The displayed products are filtered by the filters._

## Cart

**Only a buyer** can do the following actions:

### Create a cart (add the first product)

**Input**: (buyer_guid*, product_guid*, quantity*)

**Output**: Cart

**From**: product page

**Flow**:

- The user adds a product to its cart, specifying the quantity.
- _A new `cart` entity is created, with status "active"_
- _A new `products reservation` is created with the same sequence as
  the `product`._

### Update a cart (add more products)

**Input**: (buyer_guid*, product_guid*, quantity*)

**Output**: Cart

**From**: cart page

**Flow**:

- The user can add products from the cart, specifying the quantity.
- _A new `products reservation` to the only "active"
  `cart` is created with the same sequence as the `product`._


- The user can modify the quantity of the products in the cart.
- _The products' reservation is updated._
- **check sequence**: _If the `products reservation` sequence is different from
  the `product` sequence, the `products reservation` is deleted and the new
  `product` is returned._
    - If the new stock is enough, a new `products reservation` is automatically
      created with the same sequence as the `product`.
    - If the new stock is enough and the user chooses to accept the new amount,
      _a new `products reservation` is created with the same sequence as the
      `product`._
    - If the product is sold out, the user is notified.
- _The history is triggered._

### Delete from cart (remove products)

**Input**: (product_guid*)

**Output**: Cart

**From**: cart page

**Flow**:

- The user can remove products from the cart.
- _`deleted_at` is set to the current timestamp._

> Note: the carts cannot be deleted, only the products in it.

### Get the cart

**Input**: (buyer_guid*)

**Output**: Cart

**From**: cart page

**Flow**:

- The user enters the cart page.
- _Only the buyer's `cart` entity with status "active" containing all the
  product reservations, is returned._

## Buyer Order

**Only a buyer** can do the following actions:

### Create a buyer order

> TODO

**Input**: (buyer_guid*)

**Output**: Order

**From**: cart page

**Flow**:

- The user finalizes the "active" cart.
- for each product in the cart:
    - **check sequence**: _If the `products reservation` sequence is different
      from the `product` sequence, the `products reservation` is deleted._
    - Every product for which the check sequence failed is returned.
    - The user, for each product, can accept the new amount or leave it.
    - If the user accepts the new amount, it's responsibility of the Frontend
      to create a new `products reservation` and retry to create the order.
- Also for each product in the cart,
  if any of the product is locked by a non-zero `locked_stock`,
  the process is aborted.
- _A new `buyer_order` entity is created, with status "created"_
- for each product in the cart:
    - _The `locked_stock` is increased by the `reservation` quantity._
- The timeout for the user to complete the order is started.

### Complete a buyer order

> TODO

**Input**: (order_guid*)

**Output**: Order

**From**: order page

**Flow**:

- The user completes the order, i.e., pays for the products.
- _The `buyer_order` entity is updated to "finalized"_
- _The `cart` entity is updated to "finalized"_
- _The `product` amount and locked amount is decreased_
- For each seller,
    - _A new `seller_order` entity with the sellers' products present in the
      cart
      is created, with status "created"_

### Get the buyers' orders

> TODO

**Input**: (buyer_guid*)

**Output**: List of orders

**From**: orders' page

**Flow**:

- The user enters the orders' page.
- _All the `buyer_order` entities both with status "created"
  (even though they exist for a limited time) and "finalized"
  containing the cart's `products` are returned._

## Seller Order

**Only a seller** can do the following actions:

### Get the sellers' orders

> TODO

**Input**: (seller_guid*)

**Output**: List of orders

**From**: orders' page

**Flow**:

- The user enters the orders' page.
- _All the `sellers_order` entities both with statuses "created" and "finalized"
  containing the seller's products and the ordered amounts are returned._

## Shipment

**Only a seller** can do the following actions:

### Create a shipment

> TODO

**Input**: (seller_guid*, order_guid*[])

**Output**: Shipment

**From**: shipment page

**Flow**:

- The user creates a shipment, selecting the orders to include.
- _A new `shipment` entity is created, with status "created"_
- _The `sellers_order` is linked to the `shipment`_

### Progress the shipment

> TODO

**Input**: (shipment_guid*, status*)

**Output**: Shipment

**From**: shipment page

**Flow**:

- The seller can change the shipment status following the states:
    - accepted
    - shipped
    - in delivery
    - delivered
- _The `shipment` entity is updated to the new status._

## Reviews

> TODO