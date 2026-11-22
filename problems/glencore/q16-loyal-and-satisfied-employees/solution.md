### Points à défendre à l'oral

- Colonnes dans l'ordre exact demandé : `first_name`, `last_name`, `satisfaction`. Remplacer le `SELECT *` fourni, sinon le résultat a 5 colonnes et échoue.
- `>=` sur les deux conditions : « at least » inclut la borne (5 ans pile et 0,8 pile sont gardés).
- `AND` parce que les deux critères doivent être vrais en même temps.
- `ASC` est la valeur par défaut, mais l'écrire rend l'intention explicite.
- `satisfaction` est un `DECIMAL(25,5)` : la comparaison avec 0.8 est exacte, d'où l'affichage `0.86000` dans l'exemple.
