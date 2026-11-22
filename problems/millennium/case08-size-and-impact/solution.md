### Idée

Un état courant, l'offset d'impact, qui démarre à 0. Pour chaque requête dans l'ordre : on cote avec l'offset tel qu'il est avant le fill, puis on ajoute l'impact du fill, puis on applique le decay. L'ordre des requêtes compte.

{{code}}

### Points à défendre à l'oral

- La quote n utilise l'offset avant l'ordre n : un fill ne peut pas influencer son propre prix. C'est la version « no lookahead » de ce cas.
- `(1 - liquidity_score + 1e-6)` : le 1e-6 laisse un impact minimal même pour un actif parfaitement liquide. C'est lui qui produit les décimales ...000045 du sample.
- `decay` multiplie tout l'offset, pas seulement l'incrément : l'impact passé se résorbe géométriquement.
- `impact_params.get("decay", 1.0)` : decay est optionnel ; absent, il n'y a pas de mean-reversion.
- Sample vérifié : 20.1, puis offset = 0.05000005 × 0.9 = 0.045000045 → 20.145000045, puis 20.185500086 ✓.
