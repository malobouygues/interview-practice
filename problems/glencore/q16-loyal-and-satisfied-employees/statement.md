### Data model

**employees**

| Column | Type |
|---|---|
| <u>id</u> | INTEGER |
| first_name | VARCHAR(50) |
| last_name | VARCHAR(50) |
| num_years | INTEGER |
| satisfaction | DECIMAL(25,5) |

### Goal

Write a query that returns the employees who have been at the company for at least 5 years (`num_years` superior or equal to 5) **and** have a satisfaction level of at least 0.8 (`satisfaction` superior or equal to 0.8).

### Requirements

- Expected columns: `first_name`, `last_name`, `satisfaction`, in that order.
- Sort the rows by `last_name` ascending.
- Example:

| FIRST_NAME | LAST_NAME | SATISFACTION |
|---|---|---|
| Kent | Bennett | 0.86000 |
| Tony | Beyer | 0.90000 |
| James | Bradford | 0.95000 |

> *Ici, la requête tourne en local sur SQLite. Le book ne montre que les trois lignes d'exemple : la table `employees` locale (24 lignes) les contient et a été complétée avec des lignes de test (bornes 5 ans et 0.8 pile, employés ne remplissant qu'une seule des deux conditions).*
