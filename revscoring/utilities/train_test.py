"""
``revscoring train_test -h``
::

    Trains and tests a scorer model.  This utility expects to get a file of
    tab-separated feature values and labels from which to construct a model.

    Usage:
        train_test -h | --help
        train_test <scorer_model> <features> [-p=<kv>]... [-s=<kv>]...
                   [--version=<vers>]
                   [--values-labels=<path>]
                   [--model-file=<path>]
                   [--label-type=<type>]
                   [--test-prop=<prop>]
                   [--balance-sample]
                   [--balance-sample-weight]
                   [--center]
                   [--scale]
                   [--debug]

    Options:
        -h --help               Prints this documentation
        <scorer_model>          Classpath to the MLScorerModel to construct
                                and train
        <features>              Classpath to an list of features to use when
                                constructing the model
        -p --parameter=<kv>     A key-value argument pair to use when
                                constructing the scorer_model.
        -s --statistic=<kv>     A test statistic argument to use to evaluate
                                the scorer model against the test set.
        --version=<vers>        A version to associate with the model
        --values-labels=<path>  Path to a file containing feature values and
                                labels [default: <stdin>]
        --model-file=<math>     Path to write a model file to
                                [default: <stdout>]
        --label-type=<type>     Interprets the labels as the appropriate type
                                (int, float, str, bool) [default: str]
        --test-prop=<prop>      The proportion of data that should be withheld
                                for testing the model. [default: 0.20]
        --balance-sample         Balance the samples by sampling with
                                 replacement until all classes are equally
                                 represented
        --balance-sample-weight  Balance the weight of samples (increase
                                 importance of under-represented classes)
        --center                 Features should be centered on a common axis
        --scale                  Features should be scaled to a common range
        --debug                 Print debug logging.
"""
import json
import logging
import sys

import docopt
import yamlconf
from nose.tools import nottest

from . import util
from ..scorer_models.test_statistics import TestStatistic

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    ScorerModel = yamlconf.import_module(args['<scorer_model>'])
    features = yamlconf.import_module(args['<features>'])

    version = args['--version']

    model_kwargs = {}
    for parameter in args['--parameter']:
        key, value = parameter.split("=")
        model_kwargs[key] = json.loads(value)

    test_statistics = []
    for stat_str in args['--statistic']:
        test_statistics.append(TestStatistic.from_stat_str(stat_str))

    scorer_model = ScorerModel(
        features, version=version,
        balanced_sample=args['--balance-sample'],
        balanced_sample_weight=args['--balance-sample-weight'],
        center=args['--center'],
        scale=args['--scale'],
        **model_kwargs)

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

    test_prop = float(args['--test-prop'])

    run(observations, model_file, scorer_model, test_statistics, test_prop)


def run(observations, model_file, scorer_model, test_statistics, test_prop):

    scorer_model = train_test(scorer_model, observations, test_statistics,
                              test_prop)

    sys.stderr.write(scorer_model.format_info())

    sys.stderr.write("\n\n")

    scorer_model.dump(model_file)


@nottest
def train_test(scorer_model, observations, test_statistics, test_prop):
    train_set, test_set = util.train_test_split(observations,
                                                test_prop=test_prop)

    logger.debug("Test set: {0}".format(len(test_set)))
    logger.debug("Train set: {0}".format(len(train_set)))

    logger.info("Training model...")
    scorer_model.train(train_set)

    logger.info("Testing model...")
    scorer_model.test(test_set, test_statistics=test_statistics)

    return scorer_model
