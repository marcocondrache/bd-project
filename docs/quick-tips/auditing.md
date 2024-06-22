# Auditing

We decided to handle the auditing of database entities changes via triggers and
a separated table with the suffix `_history`.
Basically, every time a row is updated on its `current_*` column, a new row is
inserted into the `_history` table with the new values and the timestamp of the
change.
This way, we can keep track of all changes made to the database.

The entities that have auditing enabled are:

- `products`
- `product_reservations`
- `carts`
- `orders`
- `shipments`

## Implementation

To summarize, the auditing is implemented in the following way:

- A trigger is created for each entity that we want to audit.
  The trigger is executed every time a row is updated on its `current_*`
  columns.
- The trigger inserts a new row into the `*_history` table with the new values
  and the timestamp of the change.

## Trigger Example

The following trigger example is used to audit the changes made to the
`current_status` column of the `carts` table.

> This should be updated with the real trigger

```sql
-- function definition
CREATE OR REPLACE FUNCTION update_cart_history()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO cart_history(cart_id, new_status, created_at)
    VALUES (NEW.id, NEW.status, NOW());

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- trigger definition
CREATE TRIGGER after_update_cart_status
    AFTER UPDATE OF current_status
    ON carts
    FOR EACH ROW
    WHEN (OLD.status IS DISTINCT FROM NEW.status)
EXECUTE FUNCTION update_cart_history();
```
