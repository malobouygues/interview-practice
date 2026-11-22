### Idée

Traduire le côté client en côté market maker, puis appliquer spread et pénalité de taille contre le client. Client BUY → le MM vend → on cote l'ask, arrondi au tick supérieur. Client SELL → le MM achète → on cote le bid, arrondi au tick inférieur. L'arrondi se fait toujours « vers l'extérieur » : le client n'obtient jamais mieux que le prix calculé.

{{code}}

### Points à défendre à l'oral

- Le piège annoncé est le côté : `side` est la direction du client. Client BUY = on vend = ask au-dessus de la référence.
- `ceil` sur l'ask, `floor` sur le bid : les deux arrondis élargissent la cotation, jamais l'inverse. C'est une protection de l'edge.
- `raw_ticks = round(raw / tick_size, 9)` est une étape à part, avant le ceil/floor, car ce sont deux décisions différentes. En flottant, `0.1 + 0.05 = 0.15000000000000002`, donc un ceil naïf cote 0.16 au lieu de 0.15 — un tick de trop sur un prix déjà sur la grille. Testé : cela arrive dans environ 12 % des prix sur une grille à 0.01. Arrondir le nombre de ticks à 9 décimales supprime ce bruit sans changer aucun cas légitime.
- `round(..., 10)` final : `10006 * 0.01` vaut `100.06000000000002` ; on nettoie la représentation.
- Sample : 100 + 0.05 + 1e-5 × 100 = 100.051 → ceil au centime → 100.06 ✓ ; symétriquement 99.949 → floor → 99.94 ✓.
