import datetime

FUNCTION = "next_week"

TESTS = [
    {"name": "Today", "origin": "source", "note": "Même appel que le test code du book.",
     "args": lambda: {"d": datetime.date.today()}},
    {"name": "Across a year end: 28/12/2026", "origin": "source", "note": "Exemple du corrigé.",
     "args": lambda: {"d": datetime.date(2026, 12, 28)}, "expected": datetime.date(2027, 1, 4)},
    {"name": "Across a month end", "origin": "extra",
     "args": lambda: {"d": datetime.date(2025, 4, 27)}, "expected": datetime.date(2025, 5, 4)},
    {"name": "Leap year: 23/02/2024", "origin": "extra",
     "args": lambda: {"d": datetime.date(2024, 2, 23)}, "expected": datetime.date(2024, 3, 1)},
    {"name": "Non-leap year: 23/02/2025", "origin": "extra",
     "args": lambda: {"d": datetime.date(2025, 2, 23)}, "expected": datetime.date(2025, 3, 2)},
    {"name": "Middle of a month", "origin": "extra",
     "args": lambda: {"d": datetime.date(2026, 6, 10)}, "expected": datetime.date(2026, 6, 17)},
]
