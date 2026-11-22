### Idée

Pour chaque fill, lire le prix de l'actif as-of (fill + horizon) avec un `merge_asof` backward par actif, calculer le PnL du market maker à cet horizon, puis moyenner par client. Un client dont la moyenne est négative nous fait perdre de l'argent : il est toxique.

{{code}}

### Points à défendre à l'oral

- C'est le seul cas où l'on regarde après le fill, et c'est légitime : le markout est une analyse post-trade à horizon fixe. Mais la lookup reste backward par rapport au `mark_time` : jamais de prix postérieur à fill + horizon.
- `melt` : passer le tape en format long permet un seul `merge_asof` avec `by="asset"`, chaque fill est marqué sur son propre actif.
- Horizon au-delà de la fin du tape : `direction="backward"` renvoie naturellement le dernier prix disponible, la règle est satisfaite sans code supplémentaire.
- `merge_asof` exige que les deux côtés soient triés sur la clé `on`, d'où les deux `sort_values`.
- `dropna` sur le tape : un prix manquant n'est pas un prix, l'as-of remonte au dernier prix valide.
- Sample : Asset_1 monte de 100 à 100.5 en 5 minutes. CLIENT_A achète, le MM se retrouve short et perd 0.5 × 100 = −50 → toxique. CLIENT_B vend, le MM est long et gagne +50 ✓.
- `toxic` est calculé sur la moyenne arrondie : un bruit flottant de 1e-13 autour de 0 ne marque pas un client comme toxique.

---

### Fil conducteur des 15 cas

Les cas s'enchaînent comme la journée d'un desk de market making :

1. **Cases 1–2** — nettoyer la tape (tri, dédup, invalidation, ffill, jamais de bfill).
2. **Case 3** — mesurer la liquidité depuis les données, pas depuis un label.
3. **Cases 4–5** — lire un prix de référence as-of, avec clamp de staleness.
4. **Cases 6–9** — construire la cotation : spread, taille, grille de tick, impact cumulé.
5. **Cases 10–12** — tenir le book et le risque : inventaire, cash, PnL, limites, skew.
6. **Cases 13–14** — hedger le risque résiduel avec les actifs réellement tradables.
7. **Case 15** — mesurer après coup quels clients nous coûtent de l'argent.

Deux réflexes transverses sont notés partout. Le premier : **ne jamais utiliser une information postérieure au moment de la décision.** C'est ce qui motive le ffill sans bfill, le tri avant toute propagation, le `<=` et pas `<`, la quote n calculée avec l'état d'avant l'ordre n, et le `direction="backward"` de tout lookup as-of.

Le second : **side est la direction du client, et le market maker prend le côté opposé.** Client BUY → on vend, on cote l'ask, notre inventaire baisse et notre cash monte (Cases 7, 10, 11, 15). Seule exception : quand un contrat définit explicitement une autre convention (Case 12), on applique le contrat.
