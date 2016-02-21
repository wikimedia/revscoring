"""
``revscoring test -h``
::

    Tests a scorer model.  This utility expects to get a file of
    tab-separated feature values and labels from which to test a model.

    Usage:
        test -h | --help
        test <scorer_model> [-s=<kv>]...
             [--values-labels=<path>]
             [--model-file=<path>]
             [--label-type=<type>]
             [--scale]
             [--debug]

    Options:
        -h --help               Prints this documentation
        <scorer_model>          Path to model file that already trained.
        -s --statistic=<kv>     A test statistic argument to use to evaluate
                                the scorer model against the test set.
        --values-labels=<path>  Path to a file containing feature values and
                                labels [default: <stdin>]
        --model-file=<math>     Path to write a model file to
                                [default: <stdout>]
        --label-type=<type>     Interprets the labels as the appropriate type
                                (int, float, str, bool) [default: str]
        --debug                 Print debug logging.
"""
import logging
import sys

import docopt
from nose.tools import nottest

from . import util
from ..scorer_models import ScorerModel
from ..scorer_models.test_statistics import TestStatistic

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    scorer_model = ScorerModel.load(open(args['<scorer_model>'], 'rb'))

    test_statistics = []
    for stat_str in args['--statistic']:
        test_statistics.append(TestStatistic.from_stat_str(stat_str))

    if args['--values-labels'] == "<stdin>":
        observations_f = sys.stdin
    else:
        observations_f = open(args['--values-labels'], 'r')

    if args['--model-file'] == "<stdout>":
        model_file = sys.stdout.buffer
    else:
        model_file = open(args['--model-file'], 'wb')

    decode_label = util.DECODERS[args['--label-type']]

    observations = util.read_observations(observations_f,
                                          scorer_model.features,
                                          decode_label)
    observations = list(observations)

    run(observations, model_file, scorer_model, test_statistics)


def run(observations, model_file, scorer_model, test_statistics):

    scorer_model = test_model(scorer_model, observations, test_statistics)

    sys.stderr.write(scorer_model.format_info())

    sys.stderr.write("\n\n")

    scorer_model.dump(model_file)


@nottest
def test_model(scorer_model, observations, test_statistics):

    logger.debug("Test set: {0}".format(len(observations)))

    logger.info("Testing model...")
    scorer_model.test(observations, test_statistics=test_statistics)

    return scorer_model
