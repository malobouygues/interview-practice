### Idée

On minimise la variance du book total w'Cw en ne jouant que sur les composantes liquides. En écrivant w = v + [h ; 0], la condition du premier ordre donne C_LL h + C_L,all v = 0, d'où h = −C_LL⁻¹ C_L,all v : c'est exactement la formule de l'énoncé.

{{code}}

### Points à défendre à l'oral

- `np.linalg.solve` plutôt que `inv` : même résultat, numériquement plus stable. La formule avec l'inverse est l'écriture mathématique, pas l'implémentation.
- Ridge `1e-12 · I` : garantit que C_LL reste inversible si Asset_1 et Asset_2 sont parfaitement colinéaires, sans changer le résultat sinon.
- `C_LL = C_LL + ...` et non `C_LL += ...` : avec le Copy-on-Write de pandas 3, `.to_numpy()` peut renvoyer un tableau en lecture seule, et l'addition en place lève une `ValueError` (vérifié sur pandas 3.0.2).
- `C_L_all @ v` inclut les positions déjà détenues en Asset_1 et Asset_2 : le hedge couvre tout le book, pas seulement Asset_3.
- Le `-0.0` vient de `-solve(C, 0)` quand l'inventaire est nul : c'est précisément le sample I/O, d'où la normalisation explicite.
- Vérifié numériquement : décaler le hedge de ±5 unités dans chaque direction augmente toujours w'Cw, on est bien au minimum.
- `returns.cov()` est la covariance d'échantillon (ddof=1, convention pandas). Le choix de ddof ne change pas le hedge, seulement l'échelle de la variance résiduelle.
