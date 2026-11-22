### Idée

Deux étapes : **filtrer** (garder les scores ≤ seuil, car « strictement au-dessus » = déjà recruté), puis **prendre le max** en comparant sur le score et en renvoyant le nom.

### Points à défendre à l'oral

- `<=` et pas `<` : seuls les scores **strictement** supérieurs au seuil sont éliminés, un score égal au seuil reste candidat.
- `max(eligible, key=eligible.get)` : on itère sur les clés (les noms), on compare sur la valeur (le score), on renvoie le nom. C'est exactement le rôle du paramètre `key` (c'était la QCM Q6 du book, désormais archivée dans `archive/glencore-mcq`).
- Le test *Same scores, except the filtered best* piège ceux qui prennent le max **avant** de filtrer : il faut filtrer d'abord.
- L'énoncé garantit un gagnant unique après filtrage, donc pas d'égalité ni de dict vide à gérer.
- Complexité O(n), un seul passage pour le filtre et un pour le max.
