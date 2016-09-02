"""
``revscoring test_model -h``
::

    Tests a scorer model.  This utility expects to get a file of
    tab-separated feature values and labels from which to test a model.

    Usage:
        test_model -h | --help
        test_model <scorer_model> <label>
                   [-s=<kv>]...
                   [--observations=<path>]
                   [--model-file=<path>]
                   [--debug]

    Options:
        -h --help               Prints this documentation
        <scorer_model>          Path to model file that already trained.
        <label>                 The name of the field to be predicted
        -s --statistic=<kv>     A test statistic argument to use to evaluate
                                the scorer model against the test set.
        --observations=<path>   Path to a file containing observations
                                containing a 'cache' with <features> and a
                                <label> field [default: <stdin>]
        --model-file=<math>     Path to write a model file to
                                [default: <stdout>]
        --debug                 Print debug logging.
"""
import logging
import sys

import docopt
from nose.tools import nottest

from ..dependencies import solve
from ..scorer_models import ScorerModel
from ..scorer_models.test_statistics import TestStatistic
from .util import read_observations

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

    if args['--observations'] == "<stdin>":
        observations = read_observations(sys.stdin)
    else:
        observations = read_observations(open(args['--observations']))

    label_name = args['<label>']
    value_labels = \
        [(solve(scorer_model.features, cache=ob['cache']), ob[label_name])
         for ob in observations]

    if args['--model-file'] == "<stdout>":
        model_file = sys.stdout.buffer
    else:
        model_file = open(args['--model-file'], 'wb')

    run(value_labels, model_file, scorer_model, test_statistics)


def run(value_labels, model_file, scorer_model, test_statistics):

    scorer_model = test_model(scorer_model, value_labels, test_statistics)

    sys.stderr.write(scorer_model.format_info())

    sys.stderr.write("\n\n")

    scorer_model.dump(model_file)


@nottest
def test_model(scorer_model, value_labels, test_statistics):

    logger.debug("Test set: {0}".format(len(value_labels)))

    logger.info("Testing model...")
    scorer_model.test(value_labels, test_statistics=test_statistics)

    return scorer_model
