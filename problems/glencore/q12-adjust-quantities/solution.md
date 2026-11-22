### Idée

Chaque ligne a la forme `<entier> <espace> <produit>`. On coupe **au premier espace seulement**, on multiplie la partie gauche, et on recolle le reste tel quel. Couper au premier espace garantit qu'on ne touche jamais aux nombres qui apparaissent dans le nom du produit.

### Points à défendre à l'oral

- `split(" ", 1)` : `maxsplit=1` découpe une seule fois. `"3 eggs size 42"` donne `["3", "eggs size 42"]` : le 42 n'est pas modifié.
- L'ordre est conservé parce qu'on parcourt la liste dans l'ordre et qu'on fait `append`.
- `int(...)` gère les grands nombres sans perte (les entiers Python sont en précision arbitraire), ce qui couvre le test *Big quantities*.
- Test *One for one* : `nb_persons = 1` renvoie la liste à l'identique.
- Version compacte possible : `return [f"{int(q) * nb_persons} {p}" for q, p in (l.split(" ", 1) for l in ingredients)]`. La version en boucle est plus lisible pour l'oral.
