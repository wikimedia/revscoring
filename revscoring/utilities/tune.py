"""
Tunes a set of models against a training set to identify the best
model/configuration.

Usage:
    tune <params-config> <features> [--observations=<path>]
                                    [--scoring=<type>]
                                    [--test-prop=<prop>]
                                    [--folds=<num>]
                                    [--report=<path>]
                                    [--label-type=<type>]
                                    [--processes=<num>]
                                    [--verbose]
                                    [--debug]

Options:
    <params-config>        The path to a YAML configuration file containing the
                           models and parameter values to search when tuning
    <features>             The classpath to a feature_list to use when
                           interpreting the feature values of the observations
    --observations=<path>  The path to a file containing observations to train
                           and test against. [default: <stdin>]
    --scoring=<type>       The type of scoring strategy to optimize for when
                           choosing parameter sets [default: roc_auc]
    --test-prop=<prop>     The proportion of observations that should be held
                           asside for testing. [default: 0.25]
    --folds=<num>          The number of cross-validation folds to try
                           [default: 5]
    --report=<path>        Path to a file to write the tuning report to
                           [default: <stdout>]
    --label-type=<type>    A type describing the value to expect as a label
                           [default: str]
    --processes=<num>      The number of parallel processes to start for
                           model building [default: <cpu-count>]
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

import docopt
import yamlconf
from sklearn import grid_search
from sklearn.metrics import f1_score, roc_auc_score
from tabulate import tabulate

from . import util

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    params_config = yamlconf.load(open(args['<params-config>']))

    features = yamlconf.import_module(args['<features>'])

    label_decoder = util.DECODERS[args['--label-type']]
    if args['--observations'] == "<stdin>":
        observations_f = sys.stdin
    else:
        observations_f = open(args['--observations'])

    observations = util.read_observations(observations_f, features,
                                          label_decoder)

    scoring = args['--scoring']
    test_prop = float(args['--test-prop'])
    folds = int(args['--folds'])

    if args['--report'] == "<stdout>":
        report = sys.stdout
    else:
        report = open(args['--report'], "w")

    if args['--processes'] == "<cpu-count>":
        processes = multiprocessing.cpu_count()
    else:
        processes = int(args['--processes'])

    verbose = args['--verbose']

    run(params_config, features, observations, scoring, test_prop, folds,
        report, processes, verbose)


def run(params_config, features, observations, scoring, test_prop, folds,
        report, processes, verbose):

    # Split train and test
    train_set, test_set = util.train_test_split(observations,
                                                test_prop=test_prop)

    best_fits = []

    # For each estimator, run gridsearch.
    for name, config in params_config.items():
        try:
            EstimatorClass = yamlconf.import_module(config['class'])
            estimator = EstimatorClass()
            if not hasattr(estimator, "fit"):
                raise RuntimeError("Estimator {0} does not have a fit() method."
                                   .format(config['class']))

            parameter_grid = grid_search.ParameterGrid(config['params'])
            logger.info("Running gridsearch for {0}...".format(name))
            logger.debug("{0} parameter sets:".format(len(parameter_grid)))
            for params in parameter_grid:
                logger.debug(" - {0}".format(format_params(params)))
            logger.debug("{0} folds per parameter set".format(folds))

            start = time.time()
            grid_model = gridsearch(train_set, estimator, config['params'],
                                    scoring=scoring, folds=folds,
                                    processes=processes, verbose=verbose)

            logger.info("Completed gridsearch for {0} in {1} hours."
                        .format(name, round((time.time() - start) / (60 * 60), 3)))
            best_params, best_score, _ = max(grid_model.grid_scores_,
                                             key=lambda x: x[1])
            logger.info("\tBest fit: {0}={1} with {2}"
                        .format(scoring, round(best_score, 3),
                                format_params(best_params)))

            test_f1, test_auc = test_model(test_set, grid_model)
            logger.info("\tTest fit: f1={0}, roc_auc={1}\n"
                        .format(test_f1, test_auc))

            best_fits.append((name, best_params, best_score, test_f1, test_auc))

            logger.info("\tGrid scores:")
            table = tabulate(
                ((round(mean_score, 3), round(scores.std(), 3),
                  format_params(params))
                 for params, mean_score, scores in
                 grid_model.grid_scores_),
                headers=["mean(score)", "std(score)", "params"]
            )
            for line in table.split("\n"):
                logger.info("\t\t" + line)
        except Exception:
            logger.warn("An error occurred while trying to fit {0}"
                        .format(name))
            logger.warn("Exception:\n" + traceback.format_exc())

    # Sort the results by the best fit
    best_fits.sort(key=lambda r: r[2], reverse=True)
    possible_labels = set(label for _, label in train_set)

    # Write out the report
    report.write("# Model tuning report\n")
    report.write("- Date: {0}\n".format(datetime.datetime.now().isoformat()))
    report.write("- Train set: {0}\n".format(len(train_set)))
    report.write("- Test set: {0}\n".format(len(test_set)))
    report.write("- Labels: {0}\n".format(json.dumps(list(possible_labels))))
    report.write("- Scoring: {0}\n".format(scoring))
    report.write("\n")
    report.write("# Best fits\n")
    report.write(tabulate(
        ((name, format_params(par), round(score, 3), round(test_f1, 3),
          round(test_auc, 3))
         for name, par, score, test_f1, test_auc in best_fits),
        headers=["model", "parameters", "score", "test_f1", "test_auc"]
    ))
    report.write("\n")

    report.close()


def format_params(doc):
    return ", ".join("{0}={1}".format(k, json.dumps(v))
                     for k, v in doc.items())


def gridsearch(observations, estimator, param_grid=None,
               scoring='roc_auc', folds=5, processes=None, verbose=False):
    """
    Determine the best model via cross validation. This should be run on
    training data with test data withheld.
    """
    feature_values, labels = (list(vals) for vals in zip(*observations))
    param_grid = param_grid or {}

    processes = processes or multiprocessing.cpu_count()

    grid_model = grid_search.GridSearchCV(
        cv=folds,
        estimator=estimator,
        param_grid=param_grid,
        scoring=scoring,
        n_jobs=processes
    )

    # To perform the gridsearch, we run fit()
    feature_values, labels = (list(vals) for vals in zip(*observations))
    grid_model.fit(feature_values, labels)

    return grid_model


def test_model(observations, grid_model):
    feature_values, labels = (list(vals) for vals in zip(*observations))
    predictions = grid_model.predict(feature_values)
    scores = get_scores(grid_model, feature_values)

    return f1_score(labels, predictions), roc_auc_score(labels, scores)


# To compute an ROC score, you need scores for each example, either a class
# probability or a distance from the decision boundary
def get_scores(model, X):
    try:
        scores = model.decision_function(X)
    except:
        scores = model.predict_proba(X)[:, 1]
    return scores
