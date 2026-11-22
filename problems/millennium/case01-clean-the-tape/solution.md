### Idée

Quatre étapes dans l'ordre imposé par l'énoncé : trier, dédupliquer, invalider les prix non positifs, puis forward-fill. Le forward-fill doit venir après le tri, sinon on propage une information issue d'une ligne qui n'est pas la précédente chronologiquement (lookahead).

{{code}}

### Points à défendre à l'oral

- `kind="mergesort"` = tri stable : à timestamp égal, l'ordre d'arrivée est préservé, donc le résultat est déterministe.
- `mask(df[assets] <= 0)` : `NaN <= 0` vaut `False`, donc les NaN déjà présents restent NaN — pas besoin de les traiter séparément.
- `ffill()` s'applique colonne par colonne : chaque actif porte son propre dernier prix valide.
- Le NaN de tête reste NaN : il n'existe aucun prix antérieur, et le remplir impliquerait d'utiliser un prix futur.
- `prices.copy()` : on ne modifie jamais l'input.
