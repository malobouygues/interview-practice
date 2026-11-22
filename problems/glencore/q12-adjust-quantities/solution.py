from typing import List

def adjust_quantities(nb_persons: int, ingredients: List[str]) -> List[str]:
    result = []
    for line in ingredients:
        quantity, product = line.split(" ", 1)
        result.append(f"{int(quantity) * nb_persons} {product}")
    return result
