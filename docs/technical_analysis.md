# Technical Analysis

# Auth flow
The user can do the following actions:
- ## Register
  - From welcome page
  - The user must provide an email, password, given name, family name. 
  - The user choose a role (buyer or seller).
    - If the user chooses the seller role, it must provide an IBAN, optionally "show sold-out products" options.
    - If the user chooses the buyer role, it must provide a card number, destination address.
  - _A new user entity is created._
  - _A new buyer or seller entity is created._
  - _A new session is created._
  - The user is logged in and redirected to the home page.
- ## Login
  - From welcome page 
  - The user must provide an email and password.
  - _A new session is created._
  - The user is logged in and redirected to the home page.
- ## Logout
  - From any protected page
  - _The session is deleted._
  - The user is redirected to the welcome page.

# User
The user can do the following actions:
- ## Update profile
  - Input: (given name, family name, password, IBAN, show sold-out products, card number, destination address)
  - Output: User
  - From: the profile page
  - Flow:
    - If the user is a seller, the IBAN and show sold-out products options are shown.
    - If the user is a buyer, the card number and destination address options are shown.
  - The user can update the given name, family name, password and the other options according to the role.
  - _The user entity is updated._
  - _The buyer or seller entity is updated._
- ## Delete profile
  - Input: (guid)
  - Output: None
  - From: the profile page
  - Flow:
  - The user must confirm the deletion.
  - _The user entity is deleted._
  - _The buyer or seller entity is deleted._
  - _The session is deleted._
  - The user is redirected to the welcome page.
- ## Search for other users (?)

# Product
The seller can do the following actions:
- ## Create product
  - Input: (name*, price*, quantity*, categories*, description, brand, is second-hand)
  - Output: Product
  - From: the product creation page
  - Flow:
  - The user must provide a name, price, quantity, categories.
    - Optionally, the user can provide a description, brand, "is second-hand" option.
    - The currency is defaulted to the EURO.
  - _A new product entity is created._
  - _The keywords in the product text fields are saved._
  - If the categories do not exist, _new category entities are created._
  - _New product-category associations are created._
- ## Update product
  - Input: (price, quantity, categories, description)
  - Output: Product
  - From: the product page
  - Flow:
  - The user can update the price, quantity, categories, description.
  - _The product entity is updated._
  - _The product sequence is incremented._ (for the product reservation)
  - If the categories do not exist, _new category entities are created._
  - _New product-category associations are created._
  - _The history is triggered._
- ## Delete product
  - Input: (guid)
  - Output: None
  - From: the product page
  - Flow:
  - The user must confirm the deletion.
  - _Deleted_at is set to the current timestamp._
  - _The product sequence is incremented._
  - _The history is triggered._
