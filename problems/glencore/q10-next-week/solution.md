### Points à défendre à l'oral

- `date + timedelta` renvoie un `datetime.date` : c'est le type exigé par l'énoncé.
- `timedelta` gère seul les changements de mois et d'année (28/12/2026 + 7 jours = 04/01/2027) et les années bissextiles.
- Ne pas bricoler `d.day + 7` : ça casse en fin de mois (`ValueError: day is out of range`).
- Penser à l'`import datetime` dans le fichier réponse, sinon `NameError` (le code de test l'utilise, mais ta fonction aussi).
