### Idée

Rejouer les fills du point de vue du market maker, qui prend le côté opposé du client. Inventaire et cash bougent en sens inverse. Le PnL est le cash plus la valeur de marché de l'inventaire, marquée à la dernière ligne du tape.

{{code}}

### Points à défendre à l'oral

- Le piège est encore le côté : client BUY → le MM vend → inventaire ↓ et cash ↑.
- Sample : cash = 100 × 100.05 − 100 × 99.95 = 10.0, inventaire nul, donc pnl = 10.0. C'est exactement deux fois le half-spread de 0.05 sur 100 unités : l'edge capturé par un aller-retour.
- Inventaire initialisé à 0 pour chaque colonne de `prices` : les actifs jamais tradés apparaissent quand même, et un DataFrame de fills vide donne un book plat sans cas particulier.
- `iloc[-1]` : `prices` est un tape propre et trié, la dernière ligne est le prix le plus récent.
- `float(...)` avant `round` : on renvoie des floats Python et non des `np.float64`.
- Boucle `iterrows` choisie pour la lisibilité ; une version vectorisée (`np.where` sur le côté puis `groupby("asset").sum()`) est possible si le volume de fills le justifie.
