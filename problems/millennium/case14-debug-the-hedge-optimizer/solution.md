### Diagnostic

Les deux indices de l'énoncé (« what is being regressed and on what scale » et « whether the leftover-risk number is really a variance ») pointent vers ces défauts :

| # | Bug | Conséquence |
|---|---|---|
| 1 | Régression sur les niveaux de prix | prix non stationnaires et fortement colinéaires → régression fallacieuse, ratios instables et surdimensionnés |
| 2 | Aucun dé-moyennage, et pas d'intercept | droite forcée par l'origine → coefficients biaisés |
| 3 | `np.mean(resid ** 2)` sans centrage, en prix² | ce n'est pas une variance de rendement autour de la moyenne |
| 4 | `df = prices` alors que `prices` est un dict sérialisé | `df["Asset_3"]` échoue sur le format annoncé |

### Correction

{{code}}

### Points à défendre à l'oral

- `.iloc[1:]` plutôt que `dropna()` : le spec dit « drop the first row », rien d'autre.
- Sur des données centrées, les résidus OLS ont déjà une moyenne nulle. Recentrer `hedged` est donc mathématiquement redondant, mais c'est ce que demande le spec et cela reste juste si l'estimateur change.
- Variance de population : on divise par n avec `np.mean`, pas `np.var(ddof=1)`.
- À anticiper : sur des rendements, la variance résiduelle est de l'ordre de 1e-5, donc arrondie à 4 dp elle vaut souvent 0.0. C'est le comportement attendu du spec, pas un bug.
- **Lien avec le Case 13 :** pour un book qui ne contient que de l'Asset_3, l'OLS centré et la formule de covariance donnent exactement le même hedge (vérifié sur les mêmes données : −620.1732 et −317.5777 dans les deux cas). Les deux cas calculent le même objet par deux chemins.
