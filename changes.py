import pandas as pd
import json

def apply_changes(data, changes):
    bool_selection = data['datetime'].isin(changes['datetime'])
    # data_series = data.loc[bool_selection]["pressure_hobo"]
    changed_data = data.loc[bool_selection]["pressure_hobo"].add(changes["pressure_hobo"].values)

    data.update(changed_data)

    return data

def log_changes(history, type, changes_df, description):
    newChange = Change(des=description,type=type,changes_df=changes_df)
    if (isinstance(history,str)):
        try:
            history = json.loads(history)
        except:
            print("ERROR: couldn't parse json history string, save your work and run while you still can")
    history.append(newChange.to_json())
    return history

def undo_delete(data, changes):
    pass


def undo_shift(data, changes):
    data = pd.read_json(data)
    changes.pressure_hobo *= -1
    return apply_changes(data, changes)

def undo_add(data, changes):
    pass

class Change:
    # Text description of the change
    description = "description uninitialized"

    # Type of change corresponds to how the change was made: eg. Delete, Shift, Expcomp, etc.
    type = ""

    # A function that we can call to undo this change
    undoFunc = None

    # A data frame with the affected changes
    changes_df = pd.DataFrame

    def __init__(self, jsonIn='', des='', type='', changes_df=''):
        if jsonIn != '':
            data = json.loads(jsonIn)
            self.changes_df = pd.read_json(data['changes_df'])
            self.description = data['description']
            self.type = data['type']
            pass
        else:
            self.description = des
            self.type = type
            self.changes_df = changes_df

        match self.type:
            case "delete":
                self.undoFunc = undo_delete

            case "shift":
                self.undoFunc = undo_shift
            case "compression":
                self.undoFunc = undo_shift

            case "add":
                self.undoFunc = undo_add

        pass

    def to_json(self):
        export = {
            "changes_df": self.changes_df.to_json(),
            "description": self.description,
            "type": self.type
        }

        return json.dumps(export)
