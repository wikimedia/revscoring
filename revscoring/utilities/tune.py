"""
``revscoring tune -h``
::

    Tunes a set of models against a training set to identify the best
    model/configuration.

    Usage:
        tune <params-config> <features> <label>
             [--observations=<path>]
             [--scoring=<type>]
             [--test-prop=<prop>]
             [--folds=<num>]
             [--report=<path>]
             [--label-type=<type>]
             [--processes=<num>]
             [--cv-timeout=<mins>]
             [--scale-features]
             [--verbose] [--debug]

    Options:
        <params-config>        The path to a YAML configuration file containing
                               the models and parameter values to search when
                               tuning
        <features>             The classpath to a feature_list to use when
                               interpreting the feature values of the
                               observations
        <label>                The name of the field to be predicted
        --observations=<path>  The path to a file containing observations to
                               train and test against. [default: <stdin>]
        --scoring=<type>       The type of scoring strategy to optimize for
                               when choosing parameter sets [default: roc_auc]
        --folds=<num>          The number of cross-validation folds to try
                               [default: 5]
        --report=<path>        Path to a file to write the tuning report to
                               [default: <stdout>]
        --processes=<num>      The number of parallel processes to start for
                               model building [default: <cpu-count>]
        --cv-timeout=<mins>    The number of minutes to wait for a model to
                               cross-validate before timing out
                               [default: <forever>]
        --scale-features       Scales the feature values before tuning
        --verbose              Print progress information to stderr
        --debug                Print debug information to stderr

"""
import datetime
import json
import logging
import multiprocessing
import sys
import time
import traceback
from collections import defaultdict

import docopt
import numpy
import yamlconf
from sklearn import cross_validation, grid_search, preprocessing
from tabulate import tabulate

from . import metrics
from .. import __version__
from ..dependencies import solve
from .util import Timeout, read_observations

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    params_config = yamlconf.load(open(args['<params-config>']))

    features_path = args['<features>']
    features = yamlconf.import_path(features_path)

    if args['--observations'] == "<stdin>":
        observations = read_observations(sys.stdin)
    else:
        observations = read_observations(open(args['--observations']))

    logger.info("Reading feature values & labels...")
    label_name = args['<label>']
    value_labels = \
        [(list(solve(features, cache=ob['cache'])), ob[label_name])
         for ob in observations]

    # Get a sepecialized scorer if we have one
    scoring = metrics.SCORERS.get(args['--scoring'], args['--scoring'])

    folds = int(args['--folds'])

    if args['--report'] == "<stdout>":
        report = sys.stdout
    else:
        report = open(args['--report'], "w")

    if args['--processes'] == "<cpu-count>":
        processes = multiprocessing.cpu_count()
    else:
        processes = int(args['--processes'])

    if args['--cv-timeout'] == "<forever>":
        cv_timeout = None
    else:
        cv_timeout = float(args['--cv-timeout']) * 60  # Convert to seconds

    scale_features = args['--scale-features']
    verbose = args['--verbose']

    run(params_config, features_path, value_labels, scoring, folds,
        report, processes, cv_timeout, scale_features, verbose)


def run(params_config, features_path, value_labels, scoring, folds,
        report, processes, cv_timeout, scale_features, verbose):

    if scale_features:
        logger.debug("Scaling features...")
        ss = preprocessing.StandardScaler()
        feature_values, labels = (list(vect) for vect in zip(*value_labels))
        scaled_feature_values = ss.fit_transform(feature_values)
        value_labels = list(zip(scaled_feature_values, labels))

    # Prepare the worker pool
    logger.debug("Starting up multiprocessing pool (processes={0})"
                 .format(processes))
    pool = multiprocessing.Pool(processes=processes)

    # Start writing the model tuning report
    possible_labels = set(label for _, label in value_labels)
    report.write("# Model tuning report\n")
    report.write("- Revscoring version: {0}\n".format(__version__))
    report.write("- Features: {0}\n".format(features_path))
    report.write("- Date: {0}\n".format(datetime.datetime.now().isoformat()))
    report.write("- Observations: {0}\n".format(len(value_labels)))
    report.write("- Labels: {0}\n".format(json.dumps(list(possible_labels))))
    report.write("- Scoring: {0}\n".format(scoring))
    report.write("- Folds: {0}\n".format(folds))
    report.write("\n")

    # For each estimator and paramset, submit the job.
    cv_result_sets = defaultdict(lambda: [])
    for name, estimator, param_grid in _estimator_param_grid(params_config):
        logger.debug("Submitting jobs for {0}:".format(name))
        for params in param_grid:
            logger.debug("\tsubmitting {0}..."
                         .format(format_params(params)))
            result = pool.apply_async(_cross_validate,
                                      [value_labels, estimator, params],
                                      {'cv_timeout': cv_timeout,
                                       'scoring': scoring, 'folds': folds})
            cv_result_sets[name].append((params, result))

    # Barrier synchronization
    logger.info("Running gridsearch for {0} model/params pairs ..."
                .format(sum(len(p_r) for p_r in cv_result_sets)))
    grid_scores = []
    for name, param_results in cv_result_sets.items():
        for params, result in param_results:
            scores = result.get()  # This is a line that blocks
            grid_scores.append((name, params, scores.mean(), scores.std()))

    # Write the rest of the report!  First, print the top 10 combinations
    report.write("# Top scoring configurations\n")
    logger.info("# Top scoring configurations\n")
    grid_scores.sort(key=lambda gs: gs[2], reverse=True)
    table = tabulate(
        ((name, round(mean_score, 3), round(std_score, 3),
          format_params(params))
         for name, params, mean_score, std_score in
         grid_scores[:10]),
        headers=["model", "mean(scores)", "std(scores)", "params"],
        tablefmt="pipe"
    )
    report.write(table + "\n")
    report.write("\n")
    logger.info(table + "\n\n")

    # Now print out scores for each model.
    report.write("# Models\n")
    for name, param_results in cv_result_sets.items():
        report.write("## {0}\n".format(name))

        param_scores = ((p, r.get()) for p, r in param_results)
        param_stats = [(p, s.mean(), s.std()) for p, s in param_scores]
        param_stats.sort(key=lambda v: v[1], reverse=True)

        table = tabulate(
            ((round(mean_score, 3), round(std_score, 3),
              format_params(params))
             for params, mean_score, std_score in
             param_stats),
            headers=["mean(scores)", "std(scores)", "params"],
            tablefmt="pipe"
        )
        report.write(table + "\n")
        report.write("\n")

    report.close()


def format_params(doc):
    return ", ".join("{0}={1}".format(k, json.dumps(v))
                     for k, v in doc.items())


def _estimator_param_grid(params_config):
    for name, config in params_config.items():
        try:
            EstimatorClass = yamlconf.import_module(config['class'])
            estimator = EstimatorClass()
        except Exception:
            logger.warn("Could not load estimator {0}"
                        .format(config['class']))
            logger.warn("Exception:\n" + traceback.format_exc())
            continue

        if not hasattr(estimator, "fit"):
            logger.warn("Estimator {0} does not have a fit() method."
                        .format(config['class']))
            continue

        param_grid = grid_search.ParameterGrid(config['params'])

        yield name, estimator, param_grid


def _cross_validate(value_labels, estimator, params, scoring="roc_auc",
                    folds=5, cv_timeout=None, verbose=False):

    start = time.time()
    feature_values, labels = (list(vect) for vect in zip(*value_labels))
    estimator.set_params(**params)

    try:
        logger.debug("Running cross-validation for " +
                     "{0} with timeout of {1} seconds"
                     .format(estimator.__class__.__name__, cv_timeout))
        with Timeout(cv_timeout):
            scores = cross_validation.cross_val_score(
                estimator, feature_values,
                labels, scoring=scoring,
                cv=folds)

        duration = time.time() - start
        logger.debug("Cross-validated {0} with {1} in {2} minutes: {3} ({4})"
                     .format(estimator.__class__.__name__,
                             format_params(params),
                             round(duration / 60, 3),
                             round(scores.mean(), 3),
                             round(scores.std(), 3)))
        return scores

    except Exception:
        logger.warn("Could not cross-validate estimator {0}"
                    .format(estimator.__class__.__name__))
        logger.warn("Exception:\n" + traceback.format_exc())
        return numpy.array([0] * folds)
