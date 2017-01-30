"""
``revscoring cv_train -h``
::

    Performs a cross-validation of a scorer model strategy across folds of
    a dataset and then trains a final model on the entire set of data.

    Usage:
        cv_train -h | --help
        cv_train <scorer-model> <features> <label>
                 [-p=<kv>]... [-s=<kv>]...
                 [--version=<vers>]
                 [--observations=<path>]
                 [--model-file=<path>]
                 [--label-type=<type>]
                 [--folds=<num>]
                 [--workers=<num>]
                 [--balance-sample]
                 [--balance-sample-weight]
                 [--center]
                 [--scale]
                 [--debug]

    Options:
        -h --help               Prints this documentation
        <scorer-model>          Classpath to a ScorerModel to construct
                                and train
        <features>              Classpath to an list of features to use when
                                constructing the model
        <label>                 The name of the field to be predicted
        -p --parameter=<kv>     A key-value argument pair to use when
                                constructing the <scorer-model>.
        -s --statistic=<kv>     A test statistic argument to use to evaluate
                                the <scorer-model> against a test set.
        --version=<vers>        A version to associate with the model
        --observations=<path>   Path to a file containing observations
                                containing a 'cache' [default: <stdin>]
        --model-file=<path>     Path to write a model file to
                                [default: <stdout>]
        --folds=<num>           The number of folds that should be used when
                                cross-validating [default: 10]
        --workers=<num>         The number of workers that should be used when
                                cross-validating
        --balance-sample         Balance the samples by sampling with
                                 replacement until all classes are equally
                                 represented
        --balance-sample-weight  Balance the weight of samples (increase
                                 importance of under-represented classes)
        --center                 Features should be centered on a common axis
        --scale                  Features should be scaled to a common range
        --debug                  Print debug logging.
"""
import json
import logging
import sys

import docopt
import yamlconf
from nose.tools import nottest

from ..dependencies import solve
from ..scorer_models.test_statistics import TestStatistic
from .util import read_observations

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    sys.path.insert(0, ".")  # Search local directory first
    ScorerModel = yamlconf.import_module(args['<scorer-model>'])
    features = yamlconf.import_module(args['<features>'])

    version = args['--version']

    estimator_params = {}
    for parameter in args['--parameter']:
        key, value = parameter.split("=")
        estimator_params[key] = json.loads(value)

    test_statistics = []
    for stat_str in args['--statistic']:
        test_statistics.append(TestStatistic.from_stat_str(stat_str))

    scorer_model = ScorerModel(
        features, version=version,
        balanced_sample=args['--balance-sample'],
        balanced_sample_weight=args['--balance-sample-weight'],
        center=args['--center'],
        scale=args['--scale'],
        **estimator_params)

    if args['--observations'] == "<stdin>":
        observations = read_observations(sys.stdin)
    else:
        observations = read_observations(open(args['--observations']))

    label_name = args['<label>']
    value_labels = \
        [(list(solve(features, cache=ob['cache'])), ob[label_name])
         for ob in observations]

    if args['--model-file'] == "<stdout>":
        model_file = sys.stdout.buffer
    else:
        model_file = open(args['--model-file'], 'wb')

    folds = int(args['--folds'])
    workers = int(args['--workers']) if args['--workers'] is not None else None

    run(value_labels, model_file, scorer_model, test_statistics, folds,
        workers)


def run(value_labels, model_file, scorer_model, test_statistics, folds,
        workers):

    scorer_model = cv_train(scorer_model, value_labels, test_statistics, folds,
                            workers)

    sys.stderr.write(scorer_model.format_info())

    sys.stderr.write("\n\n")

    scorer_model.dump(model_file)


@nottest
def cv_train(scorer_model, value_labels, test_statistics, folds, workers):

    logger.info("Cross-validating model statistics for {0} folds..."
                .format(folds))
    scorer_model.cross_validate(
        value_labels, test_statistics=test_statistics, folds=folds,
        processes=workers)

    logger.info("Training model on all data...")
    scorer_model.train(value_labels)

    return scorer_model
