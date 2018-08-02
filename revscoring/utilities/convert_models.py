import os
import os.path
import pickle

from ..scoring import Model, models


def main(argv=None):
    for path in argv:
        new_path = path.replace("models", "models_new")
        new_parent = os.path.dirname(new_path)
        if not os.path.exists(new_parent):
            os.mkdir(new_parent)

        model = Model.load_pickle(models.open_file(path))
        model.dump(open(new_path, "w"))
