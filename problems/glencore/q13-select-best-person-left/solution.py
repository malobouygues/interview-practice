def select_best_person_left(test_result: dict, threshold: int) -> str:
    eligible = {
        name: score
        for name, score in test_result.items()
        if score <= threshold
    }
    return max(eligible, key=eligible.get)
