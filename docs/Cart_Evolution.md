# Cart Evolution
The behaviour of the carts created by users are handled via a *promotion* flow 
defined as follows.

```mermaid
graph
    A[Cart] --> B[Order]
    B --> C[Shipment]
```

## Cart creation
If there's no carts associated to the current user session marked as *created* 
and the user adds a new product to the cart, then a new cart is created in the 
database; otherwise the product is added to the existing cart.

```mermaid
flowchart
    User[User session] --> A[Adds product to cart]
    A --> B{Is there any cart?}
    B -->|Yes| C[Add product to cart]
    B ---->|No| E[Create new cart]
    E --> C
```

## Cart checkout
When the user decides to check out the cart, it will be marked as *finalized* 
(no more editable) and an associated order will be created.

```mermaid
flowchart
    User[User session] --> A[Checkout cart]
    A --> C[Finalize cart]
    C --> D[Create order]
```

## Order completion
When the user decides to complete the order, the availability of the requested 
products quantity is checked via the `sequence` field of the `product_history` 
table. If the quantity is sufficient then the order is marked as *completed* 
and the products quantity are updated, otherwise the user is notified, the order 
is marked as *failed*, if the user approves the notification then a new cart 
is created with the new quantity and the order is marked as *completed* and a 
new shipment for the order is created, otherwise the order is marked as 
*cancelled*.

```mermaid
flowchart
    User[User session] --> A[Complete order]
    A --> B{Is the quantity sufficient?}
    B -->|Yes| C[Mark order as in payment]
    C --> H[Create shipment]
    B ---->|No| D[Ask user to accept remaining quantity]
    D --> E{User approves?}
    E -->|Yes| F[Mark order as failed]
    F --> G[Create new cart and new order]
    G --> I[Mark order as in payment]
    I --> H[Create shipment]
    E ---->|No| M[Mark order as cancelled]
```

## Shipment management
When an `order` is completed it will be *promoted* to `shipment` and it can be managed by the seller. Each time the shipment status changes, a notification is 
sent to the user buyer.

The status of the shipment can be:
- *processing*
- *shipped*
- *in delivery*
- *delivered*
