"""
``revscoring score -h``
::

    Prints formatted information about a model file.


    Usage:
        module_info -h | --help
        module_info <model-file> [--as-json]

    Options:
        -h --help     Prints this documentation
        <model-file>  Path to a model file
        --as-json     Output model info as a JSON blob
"""
import json

import docopt

from ..scorer_models import ScorerModel


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    scorer_model = ScorerModel.load(open(args['<model-file>'], 'rb'))
    as_json = args['--as-json']

    run(scorer_model, as_json)


def run(scorer_model, as_json):
    if not as_json:
        print(scorer_model.format_info())
    else:
        print(json.dumps(scorer_model.info()))
