"""
Provides access to a set of utilities for working with revision scorer models.

Utilities:

* score             Scores a set of revisions using a trained model
* extract_features  Extracts a list of features for a set of revisions
* train_model       Trains an MLScorerModel with extracted features
* test_model        Tests an MLScorerModel with extracted features
* train_test        Trains and tests a MLScorerModel with extracted features
* model_info        Reads a model-file and reports metadata and testing
                    statistics
* tune              Tunes a set of models against a training set to identify
                    the best model/configuration

Usage:
    revscoring (-h | --help)
    revscoring <utility> [-h|--help]
"""

import sys
import traceback
from importlib import import_module


USAGE = """Usage:
    revscoring (-h | --help)
    revscoring <utility> [-h|--help]\n"""


def main():

    if len(sys.argv) < 2:
        sys.stderr.write(USAGE)
        sys.exit(1)
    elif sys.argv[1] in ("-h", "--help"):
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)
    elif sys.argv[1][:1] == "-":
        sys.stderr.write(USAGE)
        sys.exit(1)

    module_name = sys.argv[1]
    try:
        module = import_module(".utilities." + module_name,
                               package="revscoring")
    except ImportError:
        sys.stderr.write(traceback.format_exc())
        sys.stderr.write("Could not find utility {0}.\n".format(module_name))
        sys.exit(1)

    module.main(sys.argv[2:])

if __name__ == "__main__":
    main()
