### Réponse modèle (à adapter à l'écrit, en anglais)

> *I used AND because the goal asks for employees who meet both conditions at the same time: at least 5 years at the company and a satisfaction of at least 0.8. With AND, a row is returned only if both conditions are true.*
>
> *If I used OR, a row would be returned as soon as one condition is true. The result would include every employee with 5 years or more regardless of satisfaction (e.g. 9 years with 0.79), and every employee with satisfaction of 0.8 or more regardless of seniority (e.g. 4 years with 0.99), in addition to those meeting both. So the OR result is a superset of the AND result, and it would not match the requirement.*

### Points clés à placer

- `AND` = intersection des deux ensembles ; `OR` = union.
- Le résultat avec `OR` contient toujours celui avec `AND`, plus des lignes en trop.
- Donner un exemple concret de ligne qui passerait avec `OR` mais pas avec `AND` : c'est ce qui montre que tu as compris.

### What makes a strong interview answer

- **Set language first**: AND = intersection, OR = union — one sentence, no hedging.
- **The superset argument**: the OR result always contains the AND result plus extra rows, so it cannot meet a requirement that asks for both conditions.
- **One concrete row from the table** that passes with OR but not with AND (Alice Adams: 9 years, 0.79; Bob Baker: 4 years, 0.99). A concrete counter-example is what convinces an interviewer you actually reasoned about the data.
- **Tie it back to the wording** of the requirement ("at least 5 years *and* at least 0.8") — and mention the inclusive bounds (`>=`) if asked to go further.

A weak answer just says "because both conditions must be true" without describing what OR would return.
