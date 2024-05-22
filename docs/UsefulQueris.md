# Useful Queries

## 1. Get Users with their Roles
```sql
select
    u.id as user_id,
    u.guid as user_guid,
    u.email as user_email,
    case when b.id is not null then true else false end as is_buyer,
    b.id as buyer_id,
    case when s.id is not null then true else false end as is_seller,
    s.id as seller_id
from users u
left join public.buyers b on u.id = b.user_id
left join public.sellers s on u.id = s.user_id;
```

