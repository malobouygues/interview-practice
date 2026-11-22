### Idée

Lookup as-of backward : on filtre les prix valides, on trie une fois, et on localise par recherche binaire la dernière barre <= ts. Pas de scan ligne à ligne.

{{code}}

### Points à défendre à l'oral

- **Aucun lookahead :** `side="right"` puis `-1` donne le dernier index dont le timestamp est <= ts. On n'atteint jamais une barre postérieure à la requête.
- Filtrer les invalides avant le `searchsorted` fait que la barre trouvée est par construction exploitable — inutile de remonter la série ensuite.
- `searchsorted` est en O(log n) sur une série triée, contre O(n) pour un scan : c'est l'« efficient as-of lookup » demandé.
- La staleness se mesure par rapport à la dernière barre valide, pas à la dernière barre tout court : un actif illiquide plein de trous devient naturellement non cotable.
- Test de staleness en `>` strict : exactement `max_staleness_minutes` reste acceptable.
- Sur un DataFrame déjà trié, `pd.merge_asof(..., direction="backward")` ferait le même travail pour un lot de requêtes ; ici une seule requête, `searchsorted` suffit.
