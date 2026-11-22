FUNCTION = "compute_size_on_disk"

TESTS = [
    {"name": "Example: 512, 1500", "origin": "source",
     "args": lambda: {"cluster_size": 512, "file_size": 1500}, "expected": 1536},
    {"name": "File exactly aligned: 1536", "origin": "source", "note": "Cas limite du corrigé.",
     "args": lambda: {"cluster_size": 512, "file_size": 1536}, "expected": 1536},
    {"name": "One byte more: 1537", "origin": "source", "note": "Cas limite du corrigé.",
     "args": lambda: {"cluster_size": 512, "file_size": 1537}, "expected": 2048},
    {"name": "Empty file", "origin": "source", "note": "Cas limite du corrigé (formule standard : 0).",
     "args": lambda: {"cluster_size": 512, "file_size": 0}, "expected": 0},
    {"name": "Smallest cluster, largest file", "origin": "extra",
     "args": lambda: {"cluster_size": 1, "file_size": 1000000}, "expected": 1000000},
    {"name": "Largest cluster, one byte", "origin": "extra",
     "args": lambda: {"cluster_size": 65536, "file_size": 1}, "expected": 65536},
    {"name": "Largest cluster, largest file", "origin": "extra",
     "args": lambda: {"cluster_size": 65536, "file_size": 1000000}, "expected": 1048576},
    {"name": "File smaller than one cluster", "origin": "extra",
     "args": lambda: {"cluster_size": 4096, "file_size": 10}, "expected": 4096},
]
