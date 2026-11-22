### Idée

Application directe de la formule, avec le plancher.

{{code}}

### Points à défendre à l'oral

- Deux lignes seulement, mais deux étapes logiques distinctes : le spread brut, puis le clamp. Les écrire séparément rend la formule lisible d'un coup d'œil.
- `(1 - liquidity_score)` est un terme d'illiquidité : score = 1 (parfaitement liquide) annule la pénalité, score = 0 la rend maximale.
- Monotone croissant en volatilité et décroissant en liquidité — c'est le comportement attendu d'un market maker : on élargit quand le prix bouge ou quand on ne trouvera pas de contrepartie.
- `min_half_spread` protège contre un spread nul ou négatif si les paramètres sont mal calibrés : on ne cote jamais sans marge.
- `float(...)` garantit le type de retour même si les params sont des entiers.
