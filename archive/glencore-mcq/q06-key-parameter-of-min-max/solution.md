**Réponse : B — It provides a function to extract a comparison key from each element.**

### Pourquoi

`key` reçoit une fonction appliquée à chaque élément ; la comparaison se fait sur le résultat, mais c'est l'élément d'origine qui est renvoyé.

```python
max(["aa", "b", "cccc"], key=len)        # 'cccc'
min(people, key=lambda p: p["age"])      # la personne la plus jeune
max(scores, key=scores.get)              # la clé du dict dont la valeur est max
```

### Pièges

- `key` ne convertit pas les éléments : ils sont renvoyés tels quels.
- L'ordre se contrôle avec `reverse=True` dans `sorted`, pas avec `key="desc"` (ça n'existe pas).
