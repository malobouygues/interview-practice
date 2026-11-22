### Vérification sur les exemples

| Appel | `i == 1` | `j == 1` | `i + j == 1` | Résultat |
|---|---|---|---|---|
| `is_bool(1, 5)` | oui | non | non | `True` |
| `is_bool(2, 3)` | non | non | non (5) | `False` |
| `is_bool(-3, 4)` | non | non | oui (1) | `True` |

### Points à défendre à l'oral

- L'expression `or` renvoie directement un booléen, une seule ligne suffit.
- `or` court-circuite : dès qu'une condition est vraie, les suivantes ne sont pas évaluées.
