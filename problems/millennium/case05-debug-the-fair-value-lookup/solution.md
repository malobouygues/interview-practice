### Diagnostic

Le code fourni tourne et renvoie des nombres plausibles, mais il rate trois conditions :

| # | Bug | Règle violée |
|---|---|---|
| 1 | `df['timestamp'] < query_ts` (strict) | règle 5 : une barre dont le timestamp égale ts doit être utilisée |
| 2 | La clamp de staleness n'est jamais calculée | règle 3 : un prix trop vieux doit renvoyer `None` |
| 3 | Aucun tri alors que l'énoncé dit que la série n'est pas garantie ordonnée | règle 1 : `iloc[::-1]` remonte l'ordre d'arrivée, pas le temps |

### Correction

{{code}}

### Points à défendre à l'oral

- Le masque booléen remplace la boucle `iterrows()` : en filtrant d'abord sur `notna()`, le dernier élément restant est la barre cherchée. La règle 2 (« skip nulls and keep walking back ») ne nécessite aucune boucle explicite.
- Les règles 1, 2 et 5 tiennent dans une seule condition de filtrage ; les règles 3 et 4 sont deux sorties `None` distinctes, écrites séparément pour rester lisibles.
- Le tri est la correction la plus facile à oublier parce que les tests visibles passent souvent sans : c'est précisément le « subtly wrong » de l'énoncé.
- Cas limites à vérifier : entrée non triée, ts exactement sur une barre, barre exacte mais NaN (on remonte), ts avant tout, staleness pile à la limite.
