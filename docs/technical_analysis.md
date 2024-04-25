# Technical Analysis

The following is an analysis of the project requirements and the technical implementation.
It's organized by the entities in action and the actions
that can be performed for each entity.
Each action has:
- a description of the input parameters (required or not)
- the result of the action 
- the context from which the action can be performed;
- the flow of the action, divided into steps 
(with the italicized steps being the changes in the database).

# Auth flow
The user can do the following actions:
## Register
**Input**: (email*, password*, given name*, family name*, card number*, destination address*)

**Output**: Redirect

**From**: welcome page

**Flow**:
- The user must provide an email, password, given name, family name, a card number, destination address.
- _A new user entity is created._
- _A new buyer entity is created._
- _A new session is created._
- The user is logged in and redirected to the home page.

## Register as a seller
**Input**: (IBAN*, "show sold-out products" options)

**Output**: User

**From**: profile page, "become a seller" page

**Flow**:
- The user must provide an IBAN, optionally the "show sold-out products" option.
- _A new seller entity is created._

## Login
**Input**: (email*, password*)

**Output**: Redirect

**From**: welcome page, "login" form

**Flow**:
- The user must provide an email and password.
- _A new session is created._
- The user is logged in and redirected to the home page.

## Logout
**Input**: None

**Output**: Redirect

**From**: any protected page

**Flow**:
- _The session is deleted._
- The user is redirected to the welcome page.

# User
The user can do the following actions:
## Update profile
**Input**: (password, IBAN, show sold-out products, card number, destination address)

**Output**: User

**From**: profile page

**Flow**:
- If the user is a seller, the IBAN and show sold-out products options are shown.
- If the user is a buyer, the card number and destination address options are shown.
- The user can update the password and the other options according to the role.
- _The user entity is updated._
- _The buyer or seller entity is updated._

> Update: the password cannot be updated.

## Delete profile
**Input**: (guid*)

**Output**: None

**From**: profile page

**Flow**:
- The user must confirm the deletion.
- _Deleted_at is set to the current timestamp._
- _The session is deleted._
- The user is redirected to the welcome page.
## Search for other users (?)

# Product
The user can do the following actions:
## Create product
**Input**: 
(name*, price*, quantity*, categories*, description, brand, is second-hand)

**Output**: Product

**From**: product creation page, **only for sellers**

**Flow**:
- The user must provide a name, price, quantity, categories.
- Optionally, the user can provide a description, brand, "is second-hand" option.
- The currency is defaulted to the EURO.
- _A new product entity is created._
- _The keywords in the product text fields are saved._
- If the categories do not exist, _new category entities are created._
- _New product-category associations are created._

## Update product
**Input**: (price, quantity, categories, description)

**Output**: Product

**From**: product page, **only for sellers**

**Flow**:
- The user can update the price, quantity, categories, description.
- _The product entity is updated._
- _The product sequence is incremented._ (for the product reservation)
- If the categories do not exist, _new category entities are created._
- _New product-category associations are created._
- _The history is triggered._

## Delete product
**Input**: (guid)

**Output**: None

**From**: product page, **only for sellers**

**Flow**:
- The user must confirm the deletion.
- _Deleted_at is set to the current timestamp._
- _The product sequence is incremented._
- _The history is triggered._

## Search for products
**Input**: (query*, categories, brand, price range, amount range)

**Output**: List of products

**From**: home page, search bar

**Flow**:
- The user can search for products by providing a query.
- _The query is broken up into keywords._
- _The products are filtered by the keywords._
- The list of products is displayed, along with optional filters.
- The user can filter the products by categories, brand, price range, amount range.
- _The displayed products are filtered by the filters._

# Cart
**Only a buyer** can do the following actions:

## Create a cart (add one product)
**Input**: (product_guid*, quantity*)

**Output**: Cart

**From**: product page

**Flow**:
- The user adds a product to its cart, specifying the quantity.
- _A new cart entity is created, with status "created"_
- _A new products reservation is created with the same sequence as the product._

## Update a cart (add/remove products)
**Input**: (product_guid*, quantity*)

**Output**: Cart

**From**: cart page

**Flow**:
- The user can add products from the cart, specifying the quantity.
- _A new products reservation is created with the same sequence as the product._
- The user can modify the quantity of the products in the cart.
- _The products' reservation is updated._
- The user can remove products from the cart.
- _The products' reservation is deleted._
- **check sequence**: _If the products' reservation sequence is different from the product sequence, the transaction is aborted._ 
  - If the stock is not enough, the user can choose to remove the product from the cart or update the quantity.
  - If the user chooses to remove the product, _the products' reservation is deleted._
  - If the user chooses to update the quantity, _the products' reservation is updated, updating the sequence to the product sequence._
- _The history is triggered._
