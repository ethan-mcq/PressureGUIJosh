import pandas as pd


def undoDelete(data, changes):
    pass


def undoShift(data, changes):
    pass


def undoExpcomp(data, changes):
    pass


class change:
    # Text description of the change
    description = "a change was made"

    # Type of change corresponds to how the change was made: eg. Delete, Shift, Expcomp, etc.
    type = ""

    # A data frame with the affected changes
    changes_df = pd.DataFrame
