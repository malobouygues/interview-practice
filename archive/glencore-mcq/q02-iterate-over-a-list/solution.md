**Réponse : C — `for n in arr:`**

### Pourquoi

La boucle `for` de Python parcourt directement n'importe quel itérable avec le mot-clé `in`.

### Pièges

- `foreach ... of` est une syntaxe JavaScript/PHP, et `for (n : arr)` est du Java/C++. Aucune des deux n'existe en Python.
- Pour avoir l'indice en plus de la valeur, utiliser `enumerate(arr)` plutôt que `range(len(arr))`.
