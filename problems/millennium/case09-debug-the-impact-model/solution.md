### Diagnostic

Les trois défauts correspondent exactement aux trois erreurs classiques citées dans l'énoncé :

| # | Bug | Conséquence |
|---|---|---|
| 1 | `2.0 * signed_spread` sur le premier ordre | le spread est compté deux fois sur la première quote |
| 2 | `impact_term = k * quantity` | oublie le facteur `(1 - liquidity_score)` : un actif liquide bouge autant qu'un illiquide |
| 3 | `+ side_sign * (impact_term * decay)` | le decay ne touche que le nouveau terme, l'état passé ne se résorbe jamais → dérive dès la 3e quote |

### Correction

{{code}}

### Points à défendre à l'oral

- Sur le worked example, le code buggé donne `[200.0, 200.5, 201.0]` : l'état 0.5 n'est jamais décru, donc la 3e quote dérive. Le code corrigé donne `[200.0, 200.5, 200.75]` ✓.
- Le flag `first` disparaît : la formule est la même pour toutes les requêtes, il n'y a aucune raison d'avoir un cas particulier.
- Tests à faire : `liquidity_score = 1` (quotes = reference ± half_spread exactement), séquence mixte BUY/SELL, `decay = 1`.
- Différence avec le Case 8 : pas de `+ 1e-6` ici. Chaque cas a son propre contrat, on le suit à la lettre.
