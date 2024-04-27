# Functional Analysis

## sets

- Users
- Products
- Carts
- Orders
- Shipments
- Reviews
- Sessions

## relations

- One User sells N Products

- One user has N sessions
- One session has N Carts
- One Cart has N Products

- One User has N Orders
- One Order has One (finalized) Cart
- One Shipment has One (completed) Order

- One User has one Profile

## Authorizations

The users cannot search and buy for their own products

## Authentication

The user isn't required to log in ("anonymous" session) to use a cart

- If logged in, then the cart belongs to the user
- If not belong to an anonymous session

New set: session (instances of users or "anonymous")

_We do not require an anonymous session,
but it can be highlighted in the report_

> One table, Sessions

## Users

Creation process.
The user declares himself as a seller or not.
If is a seller, the IBAN is required.
If is a buyer, the card number is required.

> Two tables, Buyers and Sellers, with a common table Users

A user has a profile which contains variable information
such as address (street, city...), card number, etc.

The users (either buyer or seller) have permissions.
This can be identified as buyer permissions and seller permissions

> Two tables, PermissionsBuyer and PermissionsSeller

## Products

Human id: product code
Technical id: product id

The product has a category subset.

- Implicitly, the sellers create the categories i.e.,
  the category is a subset of the users.
  So we don't want a series of equivalent categories.
  One product can belong to one or more categories.

The product information (name, description, etc.) has a language.

- so each info is a pair (language, value)

The product has a price in a specific timestamp, bounded in a range.
The product price has a unit of measure, the currency.
So the product price is a structure (price, currency)

_We do not need to store the price history, but It can be highlighted in the
report_

_We can default the currency to EURO_

The product can have images, timestamps, etc.

The product amount can be a series of alternatives structured in a pair
(amount, unit of measure)

_We do not need to create alternatives. We can use Natural Numbers.
It still can be highlighted in the report_

If a product is sold out, then the product can either be shown or not.
The user should decide.

_We do not need to implement this, we can default it out_

> One table, Products

## Carts

The buyer instantiates the cart as soon
as the user selects a product with an amount.
That cart will be associated with a session.
It has to have at least one product.
It cannot surpass a threshold of capacity for the delivery.
The delivery can be organized based on the weight.
The cart will never be deleted.
It has a createdAt so that after a certain time
the cart will expire.

When the cart has a product, it has booked a certain amount of the product.
That amount cannot be greater than the product amount.

The product has a subset: booked amount.
The booked amount can be greater than the product amount (overbooking)

When the user buys a booked product
when the real amount has decreased to less than the booked amount,
the user can either accept the remaining amount or cancel the order.

When the user buys, the real amount will be decreased.

_Do we need to store the booked amount?_

> Transaction in READ_COMMITTED isolation level
>
> One table, Carts

## Orders

When the user buys the cart:

- A new order is created
- The user has to have a card number
- The product has to have a sufficient amount
- The booked amount is more probable to be sellable:
  that amount is reserved and the order has to be complete in a timeout

When the user wants to complete the order,
it has to check if the real amount has not changed.
(optimistic lock, use an only-increasing value to save the state of transaction)
If it has changed then the "accept the difference or leave it" process starts

The user can assess the history of the orders, only the finalized orders.
The cart related to the order will not be shown, only its products.

## Shipments

When the order is completed:

- A new shipment is created

The shipment has four states:

- presa in carico (accepted)
- spedito (shipped)
- in consegna (in delivery)
- consegnato (delivered)

When the shipment changes state, a notification is sent to the user.

The seller can change the shipment state.

The buyers have the completed (paid) orders list, with the shipment state
the seller and the products can be shown.
The sellers have the sold orders list, with options to change the shipment state
the buyer and the products can be shown.

> ## States
> - Cart
>   - created (from one product)
>   - finalized
> - Order
>   - created (from cart)
>   - finalized
> - Shipment
>   - created (from order)
>   - accepted
>   - shipped
>      - in delivery
>      - delivered
>      - accepted
>           - rejected
>           - returned
>
> If the shipment is not delivered, the order must be refunded.
> When the shipment is delivered, the order is resolved.
>
> If the product is damaged,
> or the user is not satisfied, the order can be refunded.
>
> _We will not implement the final three states of the shipment._

# Reviews

The product has reviews, which are pairs (ratings, review) with one required.
The review has a created_at timestamp.

Only the shipped products (the products that belong to a shipment)
can be reviewed.

The review is related to a product and the order of that product.

The buyers can see the reviews of the product, order by created_at and rating.
Optionally, also the sellers.

# Searches

We cannot avoid that semantically equivalent categories are created.
We can mitigate this by using a search engine that can search for already
created categories.
The sellers can search for categories while creating a product.
The sellers can change the product category.

THERE IS ALWAYS A DEFAULT SORTING

The user can search for products.
The user can search for categories by selecting from the category list.

- multi selection is allowed
- max n categories

> UNION of select for categories without repetition
>  - apply only at technical id and JOIN with products

The user can search for keywords:

- words in text fields (name, description, etc.)
- brand
- price range
- amount range

> when creating a product  
> 
> separators = new char[] { ' ', '.', ',', ';', ':', '-', '!', '?', '\t', '\n' }
> 
> string[] keys = text.split(separators).filter(word => word.length > 3)
> 
> insert into keywords (key, reference_count) values (key, 1) on conflict (key)
> do update set reference_count = reference_count + 1