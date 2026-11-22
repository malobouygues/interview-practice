### Idée

Deux signaux par actif — volatilité des rendements (inversée) et part de flux client — chacun min-max normalisé entre actifs, moyennés à parts égales, puis remis sur [0.1, 1.0].

{{code}}

### Points à défendre à l'oral

- `pct_change().std()` : `std()` de pandas ignore le premier NaN, pas besoin de `dropna()`.
- `share.get(a, 0.0)` : un actif coté mais jamais demandé a une fréquence de 0, il ne doit pas disparaître du dictionnaire.
- `value_counts(normalize=True)` divise par le total des requêtes, ce qui est bien la définition de « share of all requests ».
- Le cas « range nul » (tous les actifs ont la même vol, ou le même flux) renvoie 0.5 : le signal ne discrimine pas, il reste neutre au lieu de produire une division par zéro.
- Le plancher `0.1 + 0.9 * (...)` garantit un score strictement positif : l'actif le moins liquide reste cotable, simplement plus large.
