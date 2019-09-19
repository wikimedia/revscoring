"""
``revscoring tune -h``
::

    Tunes a set of models against a training set to identify the best
    model/configuration.  Note that either --labels or --pop-rates must be
    specified for classifiers.

    Usage:
        tune <params-config> <features> <label> <statistic>
             [-w=<lw>]... [-r=<lp>]...
             [--labels=<labels>]
             [--labels-config=<lc>]
             [--center]
             [--scale]
             [--minimize]
             [--multilabel]
             [--observations=<path>]
             [--folds=<num>]
             [--report=<path>]
             [--processes=<num>]
             [--cv-timeout=<mins>]
             [--verbose] [--debug]

    Options:
        <params-config>        The path to a YAML configuration file containing
                               the models and parameter values to search when
                               tuning
        <features>             The classpath to a feature_list to use when
                               interpreting the feature values of the
                               observations
        <label>                The name of the field to be predicted
        <statistic>            The statistic to tune for.  Stated as a path
                               within the statistics tree of the model --
                               e.g. "roc_auc.micro" or "recall.labels.true"
       --labels=<labels>       A comma-separated sequence of labels that will
                               be used for ordering labels statistics and
                               other presentations of the model.
       --labels-config=<lc>    Path to a config file containing labels and
                               associated configurations like population rates
                               and weights
       -w --label-weight=<lw>  A label-weight pair that rescales adjusts the
                               cost of getting a specific label prediction
                               wrong.
       -r --pop-rate=<lp>      A label-proportion pair that rescales metrics
                               based on the rate that the label appears in the
                               population.  If not provided, sample rates will
                               be assumed to reflect population rates.
        --minimize             If set, assume the best score is the smallest
                               value.
        --multilabel           Whether to perform multilabel classification
        --observations=<path>  The path to a file containing observations to
                               train and test against. [default: <stdin>]
        --folds=<num>          The number of cross-validation folds to try
                               [default: 5]
        --report=<path>        Path to a file to write the tuning report to
                               [default: <stdout>]
        --processes=<num>      The number of parallel processes to start for
                               model building [default: <cpu-count>]
        --cv-timeout=<mins>    The number of minutes to wait for a model to
                               cross-validate before timing out
                               [default: <forever>]
        --center               Features should be centered on a common axis
        --scale                Features should be scaled to a common range
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
import yamlconf
from sklearn.model_selection import ParameterGrid
from tabulate import tabulate

from . import util
from ..about import __version__
from ..dependencies import solve
from ..scoring.models import util as model_util
from .util import Timeout, read_observations

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    logging.getLogger("revscoring.scoring.models").setLevel(logging.WARNING)

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

    statistic_path = args['<statistic>']
    additional_params = {}

    labels, label_weights, population_rates = \
        util.read_labels_and_population_rates(
            args['--labels'], args['--label-weight'], args['--pop-rate'],
            args['--labels-config'])
    if label_weights is not None:
        additional_params['label_weights'] = label_weights
    if population_rates is not None:
        additional_params['population_rates'] = population_rates

    if args['--center']:
        additional_params['center'] = args['--center']
    if args['--scale']:
        additional_params['scale'] = args['--scale'],

    if args['--multilabel']:
        additional_params['multilabel'] = True

    maximize = not args['--minimize']

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

    verbose = args['--verbose']

    run(params_config, features, labels, features_path, value_labels,
        statistic_path, additional_params, maximize, folds, report,
        processes, cv_timeout, verbose)


def run(params_config, features, possible_labels, features_path, value_labels,
        statistic_path, additional_params, maximize, folds, report,
        processes, cv_timeout, verbose):

    feature_values, _ = (list(vect) for vect in zip(*value_labels))

    # Prepare the worker pool
    logger.debug("Starting up multiprocessing pool (processes={0})"
                 .format(processes))
    pool = multiprocessing.Pool(processes=processes)

    # Start writing the model tuning report
    report.write("# Model tuning report\n")
    report.write("- Revscoring version: {0}\n".format(__version__))
    report.write("- Features: {0}\n".format(features_path))
    report.write("- Date: {0}\n".format(datetime.datetime.now().isoformat()))
    report.write("- Observations: {0}\n".format(len(value_labels)))
    report.write("- Labels: {0}\n".format(json.dumps(list(possible_labels))))
    report.write("- Statistic: {0} ({1})\n"
                 .format(statistic_path,
                         "maximize" if maximize else "minimize"))
    report.write("- Folds: {0}\n".format(folds))
    report.write("\n")

    # For each estimator and paramset, submit the cross_validate method
    # with only 1 process.  We'll do our own parallelization.
    cv_result_sets = defaultdict(lambda: [])
    for name, Model, param_grid in _model_param_grid(params_config):
        logger.debug("Submitting jobs for {0}:".format(name))
        for params in param_grid:
            logger.debug("\tsubmitting {0}..."
                         .format(model_util.format_params(params)))

            result = pool.apply_async(
                _cross_validate,
                [features, possible_labels, value_labels, Model, params,
                 additional_params],
                {'cv_timeout': cv_timeout,
                 'statistic_path': statistic_path,
                 'folds': folds})
            cv_result_sets[name].append((params, result))

    # Barrier synchronization
    logger.info("Running gridsearch for {0} model/params pairs ..."
                .format(sum(len(p_r) for p_r in cv_result_sets)))
    grid_scores = []
    for name, param_results in cv_result_sets.items():
        for params, result in param_results:
            statistic = result.get()  # This is a line that blocks
            if statistic is not None:
                grid_scores.append((name, params, statistic))

    # Write the rest of the report!  First, print the top 10 combinations
    report.write("# Top scoring configurations\n")
    logger.info("# Top scoring configurations")
    grid_scores.sort(key=lambda gs: gs[2], reverse=maximize)
    table = tabulate(
        ((name, round(statistic, 4),
          model_util.format_params(params))
         for name, params, statistic in grid_scores[:10]
         if statistic is not None),
        headers=["model", statistic_path, "params"],
        tablefmt="pipe"
    )
    report.write(table + "\n\n")
    logger.info("\n" + table)

    # Now print out scores for each model.
    report.write("# Models\n")
    for name, param_results in cv_result_sets.items():
        report.write("## {0}\n".format(name))

        param_statistics = [(p, r.get()) for p, r in param_results
                            if r.get() is not None]
        param_statistics.sort(key=lambda v: v[1], reverse=maximize)

        table = tabulate(
            ((round(statistic, 4), model_util.format_params(params))
             for params, statistic in param_statistics
             if statistic is not None),
            headers=[statistic_path, "params"],
            tablefmt="pipe"
        )
        report.write(table + "\n")
        report.write("\n")

    report.close()


def _model_param_grid(params_config):
    for name, config in params_config.items():
        try:
            Model = yamlconf.import_module(config['class'])
        except Exception:
            logger.warn("Could not load model {0}"
                        .format(config['class']))
            logger.warn("Exception:\n" + traceback.format_exc())
            continue

        if not hasattr(Model, "train"):
            logger.warn("Model {0} does not have a train() method."
                        .format(config['class']))
            continue

        param_grid = ParameterGrid(config['params'])

        yield name, Model, param_grid


def _cross_validate(features, possible_labels,
                    value_labels, Model, params, additional_params,
                    statistic_path, folds=5, cv_timeout=None,
                    verbose=False):

    start = time.time()

    try:
        logger.debug("Running cross-validation for {0}"
                     .format(Model.__name__) +
                     " with timeout of {0} seconds".format(cv_timeout)
                     if cv_timeout is not None else "")
        model_params = dict(additional_params)
        model_params.update(params)
        model = Model(features, possible_labels, version=None, **model_params)
        if cv_timeout is not None:
            with Timeout(cv_timeout):
                stats = model.cross_validate(
                    value_labels, processes=1, folds=folds)
        else:
            stats = model.cross_validate(
                value_labels, processes=1, folds=folds)

        statistic = stats.lookup(statistic_path)

        duration = time.time() - start
        logger.debug("Cross-validated {0} with {1} in {2} minutes: {3}={4}"
                     .format(Model.__name__,
                             model_util.format_params(params),
                             round(duration / 60, 3),
                             statistic_path,
                             round(statistic, 4)))
        return statistic

    except Exception:
        logger.warn("Could not cross-validate estimator {0}"
                    .format(Model.__name__))
        logger.warn("Exception:\n" + traceback.format_exc())
        return None
