**Réponse : A — dict**

### Pourquoi

Des accolades contenant des paires clé : valeur créent un dictionnaire. Ici les clés sont les chaînes `'0'`, `'1'`, `'2'` et les valeurs les entiers 0, 1, 2.

### Pièges

- Des accolades **sans** `:` (`{1, 2, 3}`) créent un set. Attention : `{}` vide est un dict, pas un set (pour un set vide : `set()`).
- `array` et `map` ne sont pas des types littéraux Python : `map` est une fonction qui renvoie un itérateur, `array` est un module de la bibliothèque standard.
