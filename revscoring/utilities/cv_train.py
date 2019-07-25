"""
``revscoring cv_train -h``
::

    Performs a cross-validation of a scorer model strategy across folds of
    a dataset and then trains a final model on the entire set of data.  Note
    that either --labels or --pop-rates must be specified for classifiers.

    Usage:
        cv_train -h | --help
        cv_train <scoring-model> <features> <label>
                 [--labels=<labels>]
                 [--labels-config=<lc>]
                 [-p=<kv>]... [-s=<kv>]...
                 [-w=<lw>]... [-r=<lp>]...
                 [-o=<p>]...
                 [--version=<vers>]
                 [--observations=<path>]
                 [--model-file=<path>]
                 [--folds=<num>]
                 [--workers=<num>]
                 [--center]
                 [--scale]
                 [--multilabel]
                 [--debug]

    Options:
        -h --help               Prints this documentation
        <scoring-model>         Classpath to a ScorerModel to construct
                                and train
        <features>              Classpath to an list of features to use when
                                constructing the model
        <label>                 The name of the field to be predicted
        --labels=<labels>       A comma-separated sequence of labels that will
                                be used for ordering labels statistics and
                                other presentations of the model.
        --labels-config=<lc>    Path to a file containing labels and its
                                configurations like population-rates and
                                weights
        -w --label-weight=<lw>  A label-weight pair that rescales adjusts the
                                cost of getting a specific label prediction
                                wrong.
        -r --pop-rate=<lp>      A label-proportion pair that rescales metrics
                                based on the rate that the label appears in the
                                population.  If not provided, sample rates will
                                be assumed to reflect population rates.
        -p --parameter=<kv>     A key-value argument pair to use when
                                constructing the <scoring-model>.
        --version=<vers>        A version to associate with the model
        --observations=<path>   Path to a file containing observations
                                containing a 'cache' [default: <stdin>]
        --model-file=<path>     Path to write a model file to
                                [default: <stdout>]
        --folds=<num>           The number of folds that should be used when
                                cross-validating. If set to 1, testing will be
                                skipped and a model will just be trained on
                                all observations [default: 10]
        --workers=<num>         The number of workers that should be used when
                                cross-validating
        --center                Features should be centered on a common axis
        --scale                 Features should be scaled to a common range
        --multilabel            Whether to perform multilabel classification
        --debug                 Print debug logging.
"""  # noqa
import json
import logging
import sys

import docopt
import yamlconf

from ..dependencies import solve
from .util import read_labels_and_population_rates, read_observations
from .. import errors

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    ScoringModel = yamlconf.import_module(args['<scoring-model>'])
    features = yamlconf.import_module(args['<features>'])

    version = args['--version']

    estimator_params = {}
    for parameter in args['--parameter']:
        key, value = parameter.split("=", 1)
        estimator_params[key] = json.loads(value)

    labels, label_weights, population_rates = read_labels_and_population_rates(
        args['--labels'], args['--label-weight'], args['--pop-rate'],
        args['--labels-config'])

    multilabel = False
    if args['--multilabel']:
        multilabel = True

    model = ScoringModel(
        features, version=version, multilabel=multilabel,
        labels=labels, label_weights=label_weights,
        population_rates=population_rates,
        center=args['--center'],
        scale=args['--scale'],
        **estimator_params)

    if args['--observations'] == "<stdin>":
        observations = read_observations(sys.stdin)
    else:
        observations = read_observations(open(args['--observations']))

    label_name = args['<label>']
    value_labels = list(read_value_labels(features, label_name, observations))

    if args['--model-file'] == "<stdout>":
        model_file = sys.stdout.buffer
    else:
        model_file = open(args['--model-file'], 'wb')

    folds = int(args['--folds'])
    workers = int(args['--workers']) if args['--workers'] is not None else None

    run(value_labels, model_file, model, folds, workers)


def run(value_labels, model_file, model, folds, workers):
    model = cv_train(model, value_labels, folds, workers)
    sys.stderr.write(model.info.format())
    sys.stderr.write("\n")
    model.dump(model_file)


def cv_train(model, value_labels, folds, workers):
    if folds > 1:
        logger.info("Cross-validating model statistics for {0} folds..."
                    .format(folds))
        model.cross_validate(value_labels, folds=folds, processes=workers)

    logger.info("Training model on all data...")
    model.train(value_labels)

    return model


def read_value_labels(features, label_name, observations):
    for i, ob in enumerate(observations):
        try:
            yield (list(solve(features, cache=ob['cache'])), ob[label_name])
        except errors.DependencyError as e:
            logger.warn("Failed to extract dependencies (line:{0}): {1}"
                        .format(i + 1, e))
