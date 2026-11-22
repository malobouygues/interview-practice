FUNCTION = "select_best_person_left"

SUPERHUMANS = {"Quicksnail": 140, "Grey Widow": 246, "Magnetoast": 228, "Pyro Girl": 157,
               "Captain Confetti": 87}

TESTS = [
    {"name": "Example", "origin": "source",
     "args": lambda: {"test_result": dict(SUPERHUMANS), "threshold": 200},
     "expected": "Pyro Girl"},
    {"name": "No need to filter", "origin": "rebuilt",
     "note": "Test nommé dans le book, sans données : valeurs reconstituées.",
     "args": lambda: {"test_result": dict(SUPERHUMANS), "threshold": 1000},
     "expected": "Grey Widow"},
    {"name": "Same scores, except the filtered best", "origin": "rebuilt",
     "note": "Test nommé dans le book, sans données : valeurs reconstituées.",
     "args": lambda: {"test_result": dict(SUPERHUMANS), "threshold": 230},
     "expected": "Magnetoast"},
    {"name": "Score equal to the threshold stays eligible", "origin": "extra",
     "note": "Seuls les scores strictement au-dessus du seuil sont écartés.",
     "args": lambda: {"test_result": {"Alpha": 150, "Beta": 200, "Gamma": 201}, "threshold": 200},
     "expected": "Beta"},
    {"name": "Threshold of zero", "origin": "extra",
     "args": lambda: {"test_result": {"Zero Hero": 0, "Tiny Titan": 5, "Mega Mind": 900},
                      "threshold": 0},
     "expected": "Zero Hero"},
    {"name": "Only one candidate left", "origin": "extra",
     "args": lambda: {"test_result": {"Solo": 12, "Too Good": 9999}, "threshold": 50},
     "expected": "Solo"},
]
