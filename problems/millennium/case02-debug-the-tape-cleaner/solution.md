### Diagnostic

Le code fourni viole trois points du contrat :

| # | Bug | Conséquence |
|---|---|---|
| 1 | `ffill()` exécuté avant le tri | le prix reporté vient de la ligne précédente dans l'ordre d'arrivée, pas dans l'ordre chronologique → fills périmés au mauvais moment |
| 2 | `keep='last'` dans `drop_duplicates` | le contrat demande la première occurrence après tri |
| 3 | Les prix <= 0 ne sont jamais invalidés | zéros et négatifs atteignent le book |

### Correction

{{code}}

### Points à défendre à l'oral

- L'ordre des quatre opérations est le contrat : ffill avant tri et invalidation avant ffill ne sont pas des détails de style.
- `keep='first'` n'a de sens que si le tri est stable — d'où `kind='mergesort'`, sinon « la première occurrence » dépend de l'implémentation du tri.
- Règle 5 (NaN de tête) sort gratuitement : `ffill()` laisse un NaN tant qu'aucune valeur valide ne précède.
- `copy()` en entrée = pas de mutation de l'input, exigée explicitement.
