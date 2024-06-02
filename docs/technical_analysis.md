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

- The user can update the price, quantity, categories, description.
- **Clean locks**: for each `buyer_order` with status "created", whose creation
  date is older than the timeout:
    - `deleted_at` is set to the current timestamp.
    - For each product in the `buyer_order` cart:
        - The `locked_stock` is decreased by the `reservation` quantity.
- **Checks locks**: if the product is locked by a non-zero `locked_stock`, the
  user **cannot** update the product.
- The product entity is updated.
- The product `sequence` is incremented.
- If the categories do not exist, new `category` entities are created.
- New product-category `associations` are created.
- The history is triggered.

> As a result, the product's `product_reservation` becomes invalid

### Delete product

**Input**: (guid)

**Output**: None

**From**: product page, **only for sellers**

**Flow**:

- The user must confirm the deletion.
- **Clean locks**: for each `buyer_order` with status "created", whose creation
  date is older than the timeout:
    - `deleted_at` is set to the current timestamp.
    - For each product in the `buyer_order` cart:
        - The `locked_stock` is decreased by the `reservation` quantity.
- **Checks locks**: if the product is locked by a non-zero `locked_stock`, the
  user **cannot** delete the product.
- `deleted_at` is set to the current timestamp.
- The product sequence is incremented.
- The history is triggered.

> As a result, the product's `product_reservation` becomes invalid

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
- A new `cart` entity is created, with status "active"
- A new `products reservation` is created with the same sequence as
  the `product`.

### Update a cart (add more products/modify existing products)

**Input**: (buyer_guid*, product_guid*, quantity*)

**Output**: Cart

**From**: cart page

**Flow**:

- The user can add products from the cart, specifying the quantity.
- A new `products reservation` to the only "active" `cart` is created with the
  same sequence as the `product`.


- The user can modify the quantity of the products in the cart.
- **Check sequence**: If the `products reservation` sequence is different from
  the `product` sequence, the `products reservation` is deleted and the new
  `product` is returned.
    - If the new stock is enough, a new `products reservation` is automatically
      created with the same sequence as the `product`.
    - If the new stock is enough and the user chooses to accept the new amount,
      a new `products reservation` is created with the same sequence as the
      `product`.
    - If the product is sold out, the user is notified.
- The `products reservation` is updated.
- The history is triggered.

### Delete from cart (remove products)

**Input**: (product_guid*)

**Output**: Cart

**From**: cart page

**Flow**:

- The user can remove products from the cart.
- `deleted_at` is set to the current timestamp.

### Get the cart

**Input**: (buyer_guid*)

**Output**: Cart

**From**: cart page

**Flow**:

- The user enters the cart page.
- Only the buyer's `cart` entity with status "active" containing all the
  product reservations, is returned.

## Buyer Order

**Only a buyer** can do the following actions:

### Create a buyer order

**Input**: (buyer_guid*)

**Output**: Buyer Order

**From**: cart page

**Flow**:

- The user create an order for the "active" cart.
- **Clean locks**: for each `buyer_order` with status "created", whose creation
  date is older than the timeout:
    - `deleted_at` is set to the current timestamp.
    - For each product in the `buyer_order` cart:
        - The `locked_stock` is decreased by the `reservation` quantity.
- **Checks locks**: for each product in the cart, if any of the product is
  locked by a non-zero `locked_stock`, the process is aborted.
  > TODO: evaluate abort only if
  `product` stock - `locked_stock` < `reservation` quantity
- If the user already has a "created" order, the process is aborted.
- **Check sequence**: for each `products reservation` in the cart whose sequence
  is different from the `product` sequence:
    - `deleted_at` is set to the current timestamp.
- Every product for which the check sequence failed is returned.
    - The user, for each product, can accept the new amount or leave it.
    - If the user accepts the new amount, it's responsibility of the Frontend
      to create a new `products reservation` and retry to create the order.
- A new `buyer_order` entity is created, with status "created"
- for each product in the cart:
    - The `locked_stock` is increased by the `reservation` quantity.
- The timeout for the user to complete the order is started.
- The user is redirected to the order page.

### Complete a buyer order

**Input**: (order_guid*)

**Output**: Buyer Order

**From**: order page

**Flow**:

- The user completes the order, i.e., pays for the products.
- If the timeout was reached:
    - `deleted_at` is set to the current timestamp.
    - for each product in the `buyer_order` cart:
        - The `locked_stock` is decreased by the `reservation` quantity.
- The `buyer_order` entity is updated to "finalized"
- The `cart` entity is updated to "finalized"
- The `product` amount and locked amount is decreased
- For each product in the `buyer_order` cart:
    - The `locked_stock` is decreased by the `reservation` quantity.
- For each seller:
    - A new `seller_order` entity with the sellers' products present in the
      cart is created, with status "created"
- The user is redirected to the home page.

### Get the buyers' orders

**Input**: (buyer_guid*)

**Output**: List of Buyer Orders

**From**: orders' page

**Flow**:

- The user enters the orders' page.
- **Clean locks**: for each `buyer_order` with status "created", whose creation
  date is older than the timeout:
  - `deleted_at` is set to the current timestamp.
  - For each product in the `buyer_order` cart:
    - The `locked_stock` is decreased by the `reservation` quantity.
- All the `buyer_order` entities both with status "created"
  (even though they exist for a limited time) and "finalized"
  containing the cart's `products` are returned.

## Seller Order

**Only a seller** can do the following actions:

### Get the sellers' orders

**Input**: (seller_guid*)

**Output**: List of orders

**From**: orders' page

**Flow**:

- The user enters the orders' page.
- All the `sellers_order` entities both with statuses "created" and "finalized"
  containing the seller's products and the ordered amounts are returned.

## Shipment

**Only a seller** can do the following actions:

### Create a shipment

> TODO

**Input**: (seller_guid*, order_guid*[])

**Output**: Shipment

**From**: shipment page

**Flow**:

- The user creates a shipment, selecting the orders to include.
- A new `shipment` entity is created, with status "created"
- The `sellers_order` is linked to the `shipment`

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
- The `shipment` entity is updated to the new status.

## Reviews

> TODO