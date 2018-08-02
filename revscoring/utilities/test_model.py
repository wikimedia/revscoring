"""
``revscoring test_model -h``
::

    Tests a scorer model.  This utility expects to get a file of
    tab-separated feature values and labels from which to test a model.

    Usage:
        test_model -h | --help
        test_model <scorer_model> <label>
                   [--observations=<path>]
                   [--model-file=<path>]
                   [--debug]

    Options:
        -h --help               Prints this documentation
        <scoring-model>         Path to model file that already trained.
        <label>                 The name of the field to be predicted
        --observations=<path>   Path to a file containing observations
                                containing a 'cache' [default: <stdin>]
        --model-file=<path>     Path to write a model file to
        --debug                 Print debug logging.
"""
import logging
import sys

import docopt

from ..dependencies import solve
from ..scoring import Model, models
from .util import read_observations

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    scoring_model = Model.load(models.open_file(args['<scorer_model>']))

    if args['--observations'] == "<stdin>":
        observations = read_observations(sys.stdin)
    else:
        observations = read_observations(open(args['--observations']))

    label_name = args['<label>']
    value_labels = \
        [(solve(scoring_model.features, cache=ob['cache']), ob[label_name])
         for ob in observations]

    if args['--model-file'] is None:
        model_file = None
    else:
        model_file = open(args['--model-file'], 'wb')

    run(scoring_model, value_labels, model_file)


def run(scoring_model, value_labels, model_file):

    scoring_model = test_model(scoring_model, value_labels)
    sys.stderr.write(scoring_model.info.format())
    sys.stderr.write("\n\n")

    if model_file is not None:
        scoring_model.dump(model_file)


def test_model(scoring_model, value_labels):

    logger.debug("Test set: {0}".format(len(value_labels)))

    logger.info("Testing model...")
    scoring_model.test(value_labels)

    return scoring_model
