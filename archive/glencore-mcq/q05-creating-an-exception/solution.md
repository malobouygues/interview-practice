**Réponses : B et D**

- `raise Exception("Exception occurred!")`
- `raise Exception()`

### Pourquoi

En Python, on lève une exception avec `raise`. Le message est optionnel. `throw` est le mot-clé de Java, JavaScript et C++, et n'existe pas en Python (`SyntaxError`).

### Bonus oral

- On peut aussi écrire `raise Exception` sans parenthèses : Python instancie la classe.
- Bonne pratique : lever une exception spécifique (`ValueError`, `TypeError`) ou une sous-classe maison, plutôt que `Exception` générique.
