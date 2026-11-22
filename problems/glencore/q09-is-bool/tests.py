FUNCTION = "is_bool"

TESTS = [
    {"name": "is_bool(1, 5)", "origin": "source",
     "args": lambda: {"i": 1, "j": 5}, "expected": True},
    {"name": "is_bool(2, 3)", "origin": "source",
     "args": lambda: {"i": 2, "j": 3}, "expected": False},
    {"name": "is_bool(-3, 4)", "origin": "source",
     "args": lambda: {"i": -3, "j": 4}, "expected": True},
    {"name": "Second argument equals 1", "origin": "extra",
     "args": lambda: {"i": 5, "j": 1}, "expected": True},
    {"name": "Both zero", "origin": "extra",
     "args": lambda: {"i": 0, "j": 0}, "expected": False},
    {"name": "Sum equals 1 with a negative", "origin": "extra",
     "args": lambda: {"i": 2, "j": -1}, "expected": True},
    {"name": "Both equal 1 (sum is 2)", "origin": "extra",
     "args": lambda: {"i": 1, "j": 1}, "expected": True},
    {"name": "Both negative", "origin": "extra",
     "args": lambda: {"i": -1, "j": -1}, "expected": False},
]
