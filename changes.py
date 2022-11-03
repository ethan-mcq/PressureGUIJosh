import pandas as pd

def apply_changes(data, changes):
    bool_selection = data['datetime'].isin(changes['datetime'])
    # data_series = data.loc[bool_selection]["pressure_hobo"]
    changed_data = data.loc[bool_selection]["pressure_hobo"].add(changes["pressure_hobo"].values)

    data.update(changed_data)

    return data

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
