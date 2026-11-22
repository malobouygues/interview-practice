**Réponse : C**

```python
for index, color in enumerate(["red", "green", "blue"]):
    print(index, color)
```

### Pourquoi

`enumerate` produit des tuples (indice, élément) : `(0, "red")`, `(1, "green")`, `(2, "blue")`. Le déballage `index, color` les reçoit dans le bon ordre.

### Pourquoi pas les autres

- **A** : la liste est plate, chaque élément est un scalaire. `0` ne peut pas être déballé en deux variables → `TypeError`, et `"red"` serait déballé lettre par lettre → `ValueError`.
- **B** : deux tours de boucle seulement ; le premier déballe un tuple de 3 éléments dans 2 variables → `ValueError`.
- **D** : les noms sont inversés (`color` reçoit l'indice), et le `print(index, color)` affiche `red 0`, `green 1`, `blue 2`.
