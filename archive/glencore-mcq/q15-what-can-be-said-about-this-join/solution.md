**Réponses : A et C**

- `JOIN` is equivalent to `INNER JOIN`
- The query will only output `product_id` with corresponding `order_id`

### Pourquoi

`JOIN` sans précision est un `INNER JOIN` : il ne garde que les lignes qui ont une correspondance des deux côtés. Un produit jamais commandé (absent d'`order_product`) n'apparaît pas dans le résultat.

### Pourquoi pas B et D

- Un `LEFT JOIN` garderait **tous** les produits, avec `order_id = NULL` pour ceux jamais commandés. C'est la situation décrite par D, qui ne peut arriver qu'avec un `LEFT JOIN`.

### Bonus oral

- Un même `product_id` peut apparaître plusieurs fois s'il figure dans plusieurs commandes (une ligne par couple produit/commande).
- Pour lister les produits jamais commandés : `LEFT JOIN ... WHERE op.order_id IS NULL`.
