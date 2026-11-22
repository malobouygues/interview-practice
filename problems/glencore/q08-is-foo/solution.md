### Points à défendre à l'oral

- `==` renvoie déjà un booléen : pas besoin de `if ... return True else return False`.
- Utiliser `==` et pas `is` : `is` teste l'identité de l'objet, et deux chaînes égales ne sont pas garanties d'être le même objet.
- Si `param` n'est pas une chaîne (`None`, un entier), `==` renvoie simplement `False`, sans erreur.
- Comparaison sensible à la casse : `"Foo"` renvoie `False`, conformément à l'énoncé.
