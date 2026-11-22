You have the ingredient list of a one-person recipe. You want to cook it for many persons (defined by `nb_persons`). So, you must multiply all the quantities.

The ingredient list consists of strings, each defining a specific product. They all have the following format:

- An integer (written with digits), defining the quantity.
- A space character.
- Some words, defining the product.

Modify the string by multiplying the initial integer by `nb_persons`.

You do not have to take care of the singular/plural of the words defining the product. These words may contain some numbers, you must not modify them.

The order of the lines must be preserved.

### Example

You want to cook a cake for 3 persons. Here is the initial ingredient list for one person:

```text
2 eggs
200 grams of flour
150 grams of sugar
1 liter(s) of milk
```

You must output this list:

```text
6 eggs
600 grams of flour
450 grams of sugar
3 liter(s) of milk
```

### Implementation

**Function** — Implement the function `adjust_quantities`.

**Parameters**

| Name | Type | Description |
|---|---|---|
| `nb_persons` | int | Number of persons for which to prepare the recipe. Strictly positive integer. |
| `ingredients` | List[str] | List of ingredients. All of them start with an integer, strictly positive. |

**Return value**

| Name | Type | Description |
|---|---|---|
| `output` | List[str] | List of ingredients, with quantities multiplied by the number of persons. |

**Constraints**

- Available RAM: 512MB
- Timeout: 6 seconds

### Tests

- **Cake recipe, normal case** — parameters `3, ["2 eggs", "200 grams of flour", "150 grams of sugar", "1 liter(s) of milk"]` → `["6 eggs", "600 grams of flour", "450 grams of sugar", "3 liter(s) of milk"]`
- **Big quantities, for many persons**
- **One for one**
