**Réponse : D — A then B then C**

### Pourquoi

Python exécute le fichier de haut en bas :

1. Bloc **A** : code de module, exécuté immédiatement.
2. `def main()` : définit seulement la fonction ; le bloc B **n'est pas** exécuté à ce moment.
3. `if __name__ == '__main__':` est vrai quand on lance `python3 file.py` → `main()` est appelée → bloc **B**.
4. Bloc **C** : code de module, exécuté en dernier car il est placé **après** le `if`.

### Pièges

- Si le fichier était **importé** (`import file`), `__name__` vaudrait `"file"` : on aurait A puis C, sans B.
- Placer du code après le `if __name__ == '__main__'` est une mauvaise pratique : c'est justement pour tester cette subtilité que la question le fait.
