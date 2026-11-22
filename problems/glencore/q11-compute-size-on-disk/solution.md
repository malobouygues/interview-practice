### Idée

Un fichier occupe un nombre **entier** de clusters : on arrondit `file_size / cluster_size` **au supérieur**, puis on multiplie par la taille d'un cluster.

Exemple : 1500 / 512 = 2,93 → 3 clusters → 3 × 512 = **1536** octets.

### Points à défendre à l'oral

- `(a + b - 1) // b` est la division entière arrondie au supérieur, sans passer par les flottants. Équivalent : `-(-a // b)` ou `math.ceil(a / b)`.
- Cas limites testés : fichier exactement aligné (1536 → 1536), un octet de plus (1537 → 2048), fichier vide (0 → 0 cluster → 0 octet).
- Complexité O(1), aucun souci avec la contrainte de 6 s.

> *Le début de l'énoncé manque sur la photo. Si l'énoncé complet précise qu'un fichier vide occupe quand même un cluster, remplacer par `max(1, clusters)`. La formule standard donne 0.*
