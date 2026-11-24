import pandas as pd


def treat_gaps(hours):
    """Solar blanks -> 0 at night / flagged in daylight; wind flagged; capacity carried 48 h with its age."""
    hours = hours.copy()
    raise NotImplementedError("decide variable by variable")
