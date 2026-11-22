### Diagnostic

Les deux symptômes rapportés par le desk correspondent à trois écarts au contrat :

| # | Bug | Symptôme |
|---|---|---|
| 1 | `abs(current)` dans les tests de limites au lieu de `abs(projected)` | le trade qui fait franchir la limite passe, car on regarde la position d'avant le trade |
| 2 | `>` au lieu de `>=` pour le reject | un trade qui atterrit exactement sur le cap est accepté alors que c'est une breach |
| 3 | `+ skew` au lieu de `- skew` | être long pousse les quotes vers le haut : on rachète ce qu'on détient déjà, le book empire |

### Correction

Le bloc qui reconditionnait les arguments dans un dict `data` puis les en ressortait ne faisait que renommer les variables : il est supprimé, on lit directement `params`, `request` et `inventory`. L'`import math`, inutilisé, est supprimé aussi.

{{code}}

### Points à défendre à l'oral

- « Our inventory skew is making our book worse » = bug 3. « Taking trades right at the risk cap » = bugs 1 et 2.
- Deux inventaires différents, deux usages : la position projetée (post-trade) pour les limites, la position actuelle (pré-trade) pour le skew. C'est écrit explicitement dans le contrat.
- Convention de signe différente du Case 11 : ici le contrat définit BUY → +quantity. Le code fourni la respecte déjà, ce n'est donc pas un bug. À mentionner à l'oral, mais à ne pas modifier : on corrige les écarts au contrat, pas le contrat.
- `hard_limit = base_limit` : pas de scaling par la liquidité dans ce cas ; `liquidity_score` est fourni mais non requis.
- Tests à faire : position projetée exactement égale au cap (reject), position actuelle sous le soft mais projetée au-dessus (widen), inventaire long (ask et bid plus bas).
