"""
Tunes a set of models against a training set to identify the best
model/configuration.

Usage:
    tune <params-config> [--observations=<path>]
                         [--scoring=<type>]
                         [--test-prop=<prop>]
                         [--folds=<num>]
                         [--report=<path>]
                         [--label-type=<type>]
                         [--verbose]
                         [--debug]

"""
import logging
import multiprocessing
import random

import numpy as np
import yamlconf
from sklearn import cross_validation, grid_search
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import (accuracy_score, auc, f1_score,
                             precision_recall_curve,
                             precision_recall_fscore_support, precision_score,
                             recall_score, roc_auc_score, roc_curve)

logger = logging.getLogger(__name__)


def run(params_config, observations, scoring, test_prop, folds, report,
        processes, verbose):

    # Split train and test
    train_set, test_set = train_test_split(observations, test_prop=test_prop)

    best_fits = []

    # For each estimator, run gridsearch.
    for name, config in params_config:
        logger.info("Running gridsearch for {0}".format(name))
        EstimatorClass = yamlconf.import_module(config['class'])
        estimator = EstimatorClass()
        if not hasattr(estimator, "fit"):
            raise RuntimeError("Estimator {0} does not have a fit() method."
                               .format(config['class']))

        logger.info("Running gridsearch for {0}...".format(name))
        grid_model = gridsearch(train_set, estimator, config['params'],
                                scoring=scoring, folds=folds,
                                processes=processes)

        logger.info("Completed gridsearch for {0}.".format(name))
        best_params, best_score, _ = max(grid_model.grid_scores_,
                                         key=lambda x: x[1])
        logger.info("\tBest fit: {0}={1} with {2}"
                    .format(scoring, best_score, best_params))

        f1, roc_auc = test_model(test_set, grid_model)
        logger.info("\tTest set fit: f1={0}, roc_auc={1}\n"
                    .format(f1, roc_auc))

        best_fits.append((name, best_params, best_score, f1, roc_auc))

        # TODO: should be tabular
        logger.info("\tGrid scores:")
        for params, mean_score, scores in grid_model.grid_scores_:
            logger.info("\t - %0.3f (+/-%0.03f) for %r"
                        % (mean_score, scores.std(), params))


def train_test_split(observations, test_prop=0.25):
    # Split train and test set from obs.
    observations = list(observations)
    random.shuffle(observations)

    test_set_size = int(len(observations) * test_prop)
    test_set = observations[:test_set_size]
    logger.debug("Test set: {0}".format(len(test_set)))

    train_set = observations[test_set_size:]
    logger.debug("Train set: {0}".format(len(train_set)))

    return train_set, test_set


def gridsearch(observations, estimator, param_grid=None,
               scoring='roc_auc', folds=5, processes=None):
    """
    Determine the best model via cross validation. This should be run on
    training data with test data withheld.
    """
    param_grid = param_grid or {}

    processes = processes or multiprocessing.cpu_count()

    stratified_cv = cross_validation.StratifiedKFold(labels, n_folds=folds)

    grid_model = grid_search.GridSearchCV(
        cv=stratified_cv,
        estimator=estimator,
        param_grid=param_grid,
        scoring=scoring,
        n_jobs=processes
    )

    # This line actually performs the gridsearch
    feature_values, labels = (list(vals) for vals in zip(*observations))
    grid_model.fit(feature_values, labels)

    return grid_model

def test_model(observations, grid_model):

    feature_values, labels = (list(vals) for vals in zip(*observations))
    predictions = model_grid.predict(feature_values)
    scores = get_scores(model_grid, feature_values)

    return f1_score(labels, predictions), roc_auc_score(labels, scores)

# To compute an ROC score, you need scores for each example, either a class probability
# of a distance from the decision boundary
def get_scores(model, X):
    try:
        scores = model.decision_function(X)
    except:
        scores = model.predict_proba(X)[:, 1]
    return scores
