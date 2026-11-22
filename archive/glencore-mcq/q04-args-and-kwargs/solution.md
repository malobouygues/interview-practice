**Réponses : A, C, F**

- `arg_first == 10`
- `args == (20, 30)`
- `kwargs == {}` (dictionnaire vide)

### Pourquoi

- Le premier argument positionnel remplit le paramètre nommé `arg_first`.
- `*args` récupère **tous les positionnels restants** dans un **tuple**, ici `(20, 30)`.
- `**kwargs` récupère les arguments nommés (clé=valeur) dans un **dict**. Il n'y en a aucun, donc `{}`, jamais `None`.

### Pièges

- `args` est un tuple même avec un seul élément : appeler `function(10, 20)` donne `args == (20,)`, pas `20`.
- `kwargs` est toujours un dict, jamais un tuple ni `None`.
