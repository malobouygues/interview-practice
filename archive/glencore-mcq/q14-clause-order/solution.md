**Réponse : C**

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
ORDER BY ...
```

### Pourquoi

C'est l'ordre d'**écriture** imposé par la syntaxe SQL. Moyen mnémotechnique : on filtre les lignes (`WHERE`), on les regroupe (`GROUP BY`), puis on trie le résultat final (`ORDER BY`), qui vient toujours en dernier (avant `LIMIT`).

### Bonus oral

- Ordre complet d'écriture : `SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT`.
- Ordre **logique d'exécution** : `FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`. C'est pourquoi on ne peut pas utiliser un alias du `SELECT` dans le `WHERE`, mais on peut dans l'`ORDER BY`.
- `WHERE` filtre les lignes avant agrégation, `HAVING` filtre les groupes après.
