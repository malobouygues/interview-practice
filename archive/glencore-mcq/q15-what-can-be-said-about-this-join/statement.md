You are working with the following tables (<u>underlined</u> columns are the primary key):

**product_category**

| Column | Type |
|---|---|
| <u>product_category_id</u> | INTEGER |
| name | VARCHAR(50) |
| description | VARCHAR(255) |

**product**

| Column | Type |
|---|---|
| <u>product_id</u> | INTEGER |
| product_category_id | INTEGER → product_category |
| name | VARCHAR(50) |
| description | VARCHAR(255) |
| price | DECIMAL(5,2) |
| available_stock | INTEGER |

**customer**

| Column | Type |
|---|---|
| <u>customer_id</u> | INTEGER |
| firstname | VARCHAR(50) |
| lastname | VARCHAR(50) |
| birth_date | DATE |
| address | VARCHAR(255) |
| zipcode | VARCHAR(5) |
| city | VARCHAR(50) |
| phone_number | VARCHAR(20) |

**purchase_order**

| Column | Type |
|---|---|
| <u>order_id</u> | INTEGER |
| customer_id | INTEGER → customer |
| date | DATE |

**order_product**

| Column | Type |
|---|---|
| <u>order_id</u> | INTEGER → purchase_order |
| <u>product_id</u> | INTEGER → product |

What can be said regarding the following join?

```sql
SELECT
    p.product_id,
    op.order_id
FROM
    product p
    JOIN order_product op ON p.product_id = op.product_id
```
