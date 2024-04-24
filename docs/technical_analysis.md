# Technical Analysis

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
The seller can do the following actions:
## Create product
**Input**: 
(name*, price*, quantity*, categories*, description, brand, is second-hand)

**Output**: Product

**From**: product creation page

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

**From**: product page

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

**From**: product page

**Flow**:
- The user must confirm the deletion.
- _Deleted_at is set to the current timestamp._
- _The product sequence is incremented._
- _The history is triggered._
