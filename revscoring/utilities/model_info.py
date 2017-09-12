"""
``revscoring model_info -h``
::

    Prints formatted information about a model file.


    Usage:
        module_info -h | --help
        module_info <model-file> [<path>...] [--formatting=<type>]

    Options:
        -h --help            Prints this documentation
        <model-file>         Path to a model file
        <path>               A model information path.  If no path is provided,
                             all default fields will be in the output.
        --formatting=<type>  What format to output the information?  "str" or
                             "json" [default: str]
"""
import json

import docopt

from ..scoring import Model, models


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    scoring_model = Model.load(models.open_file(args['<model-file>']))
    paths = args['<path>']
    formatting = args['--formatting']

    run(scoring_model, paths, formatting)


def run(scoring_model, paths, formatting):
    formatted = scoring_model.info.format(paths, formatting=formatting)
    if formatting == "json":
        formatted = json.dumps(formatted, indent=2)

    print(formatted)
