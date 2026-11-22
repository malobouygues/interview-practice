### Idée

La limite dure est proportionnelle à la liquidité. La décision accept / widen / reject se prend sur la position projetée après le trade ; le skew se calcule sur la position actuelle et fait pencher les deux côtés de la cotation vers le retour à plat.

{{code}}

### Points à défendre à l'oral

- `hard = base_limit * liquidity_score` : un actif à 0.1 a une capacité dix fois plus faible, il se remplit et commence à rejeter bien plus tôt.
- Décision sur la position projetée : on refuse le trade qui nous ferait franchir la limite, pas seulement celui qui arrive quand on y est déjà.
- Skew = −coeff × inventaire actuel : long → skew négatif → ask et bid plus bas → on attire les acheteurs et on décourage les vendeurs → retour vers flat.
- « Add an extra half_spread » est écrit `half = 2 * half_spread` : une seule formule de quote au lieu de deux branches de correction.
- Reject en `>` strict : c'est ce que dit ce contrat. Le Case 12 utilise `>=` — on suit chaque énoncé tel qu'il est écrit.
