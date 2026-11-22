FUNCTION = "is_foo"

TESTS = [
    {"name": 'is_foo("foo")', "origin": "source",
     "args": lambda: {"param": "foo"}, "expected": True},
    {"name": 'Case sensitive: "Foo"', "origin": "source", "note": "Cas cité dans le corrigé.",
     "args": lambda: {"param": "Foo"}, "expected": False},
    {"name": "Not a string: None", "origin": "source", "note": "Cas cité dans le corrigé.",
     "args": lambda: {"param": None}, "expected": False},
    {"name": "Not a string: an integer", "origin": "source", "note": "Cas cité dans le corrigé.",
     "args": lambda: {"param": 42}, "expected": False},
    {"name": 'Another string: "bar"', "origin": "extra",
     "args": lambda: {"param": "bar"}, "expected": False},
    {"name": "Empty string", "origin": "extra",
     "args": lambda: {"param": ""}, "expected": False},
    {"name": 'Trailing space: "foo "', "origin": "extra",
     "args": lambda: {"param": "foo "}, "expected": False},
]
