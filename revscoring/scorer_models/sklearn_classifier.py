import io
import logging
import time
from collections import defaultdict
from datetime import datetime
from multiprocessing import Pool, cpu_count

from sklearn.cross_validation import KFold
from sklearn.preprocessing import RobustScaler

from . import util
from ..features import vectorize_values
from .scorer_model import MLScorerModel
from .test_statistics import (accuracy, precision, precision_recall, recall,
                              roc, table)

logger = logging.getLogger(__name__)


class ScikitLearnClassifier(MLScorerModel):
    Estimator = NotImplemented
    Base_Params = {}

    def __init__(self, features, version=None,
                 balanced_sample=False, balanced_sample_weight=False,
                 scale=False, center=False,
                 test_statistics=None, estimator=None, **estimator_params):
        super().__init__(features, version=version)
        if estimator is None:
            _params = dict(self.Base_Params)
            _params.update(estimator_params)
            self.estimator_params = _params
            self.estimator = self.Estimator(**_params)
        else:
            self.estimator = estimator
            self.estimator_params = estimator.get_params()

        self.balanced_sample = balanced_sample
        self.balanced_sample_weight = balanced_sample_weight
        if scale or center:
            self.scaler = RobustScaler(with_centering=center,
                                       with_scaling=scale)
        else:
            self.scaler = None

        self.test_statistics = test_statistics

        self.test_stats = None
        self.params = {
            'balanced_sample': balanced_sample,
            'balanced_sample_weight': balanced_sample_weight,
            'scale': scale,
            'center': center
        }

    def _clean_copy(self):
        cls = self.__class__
        kwargs = dict(self.estimator_params)
        kwargs.update(self.params)
        return cls(self.features, version=self.version,
                   test_statistics=self.test_statistics, **kwargs)

    def __getattr__(self, attr):
        if attr is "stats":
            return None
        elif attr is "params":
            return None
        else:
            raise AttributeError(attr)

    def train(self, values_labels, **kwargs):
        """

        :Returns:
            A dictionary with the fields:

            * seconds_elapsed -- Time in seconds spent fitting the model
        """
        start = time.time()
        values, labels = zip(*values_labels)
        # Flaten feature vector
        values = [vectorize_values(feature_values)
                  for feature_values in values]

        if self.scaler is not None:
            values = self.scaler.fit_transform(values)
            values_labels = zip(values, labels)

        if self.balanced_sample:
            values_labels = zip(values, labels)
            values_labels = util.balance_sample(values_labels)
            values, labels = zip(*values_labels)

        if self.balanced_sample_weight:
            sample_weight = util.balance_sample_weights(labels)
        else:
            sample_weight = None

        # Fit SVC model
        self.estimator.fit(values, labels, sample_weight=sample_weight,
                           **kwargs)
        self.trained = time.time()

        return {
            'seconds_elapsed': time.time() - start
        }

    def score(self, feature_values):
        """
        Generates a score for a single revision based on a set of extracted
        feature_values.

        :Parameters:
            feature_values : collection(`mixed`)
                an ordered collection of values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dict with the fields:

            * predicion -- The most likely class
            * probability -- A mapping of probabilities for input classes
                             corresponding to the classes the classifier was
                             trained on.  Generating this probability is
                             slower than a simple prediction.
        """
        feature_values = vectorize_values(feature_values)
        if self.scaler is not None:
            feature_values = self.scaler.transform([feature_values])[0]

        prediction = self.estimator.predict([feature_values])[0]
        labels = self.estimator.classes_
        probas = self.estimator.predict_proba([feature_values])[0]
        probability = {label: proba for label, proba in zip(labels, probas)}

        doc = {
            'prediction': prediction,
            'probability': probability
        }
        return util.normalize_json(doc)

    def test(self, values_labels, test_statistics=None, store_stats=True):
        """
        :Returns:
            A dictionary of test statistics with the fields:

            * n -- The number of observations tested against
            * accuracy -- The accuracy of classification
            * table -- A truth table for classification
            * test_statistics -- A map of test statistic values
        """
        values, labels = zip(*values_labels)

        test_statistics = test_statistics or self.test_statistics or \
                          [table(), accuracy(), precision(), recall(),
                           roc(), precision_recall()]

        scores = [self.score(feature_values) for feature_values in values]

        test_stats = {}
        for statistic in test_statistics:
            test_stats[statistic] = \
                statistic.score(scores, labels)

        if store_stats:
            self.test_statistics = test_statistics
            self.test_stats = test_stats

        return test_stats

    def cross_validate(self, values_labels, test_statistics=None, folds=10,
                       store_stats=True, processes=None):

        test_statistics = test_statistics or self.test_statistics or \
                          [table(), accuracy(), precision(), recall(),
                           roc(), precision_recall()]

        pool = Pool(processes=processes or cpu_count())

        folds_i = KFold(len(values_labels), n_folds=folds, shuffle=True,
                        random_state=0)
        results = pool.map(self._generate_test_stats,
                           ((i, [values_labels[i] for i in train_i],
                                [values_labels[i] for i in test_i],
                             test_statistics)
                            for i, (train_i, test_i) in enumerate(folds_i)))
        cross_validations = defaultdict(list)
        for test_stats in results:
            for test_statistic in test_statistics:
                stat = test_stats[str(test_statistic)]
                cross_validations[test_statistic].append(stat)

        merged_stats = {}
        for test_statistic, stats in cross_validations.items():
            merged_stats[test_statistic] = test_statistic.merge(stats)

        merged_stats['cross-validation'] = {
            'folds': folds,
            'observations': len(values_labels)
        }

        if store_stats:
            self.test_statistics = test_statistics
            self.test_stats = merged_stats

        return merged_stats

    def _generate_test_stats(self, i_train_test_vls_stats):
        i, train_vls, test_vls, test_statistics = i_train_test_vls_stats
        logger.info("Performing cross-validation {0}...".format(i + 1))
        sm = self._clean_copy()
        logger.debug("Training cross-validation for {0}...".format(i + 1))
        sm.train(train_vls)
        logger.debug("Testing cross-validation for {0}...".format(i + 1))
        test_stats = sm.test(test_vls, test_statistics=test_statistics)
        return {str(t): v for t, v in test_stats.items()}

    def info(self):
        params = {}
        params.update(self.params or {})
        params.update(self.estimator.get_params())

        return util.normalize_json({
            'type': self.__class__.__name__,
            'params': params,
            'version': self.version,
            'trained': self.trained,
            'test_stats': self.test_stats
        })

    def format_info(self, format="str"):
        if format == "str":
            return self.format_info_str()
        elif format == "json":
            return self.format_info_json()
        else:
            raise ValueError("Format '{0}' not available for {1}."
                             .format(format, self.__class__.__name__))

    def format_info_str(self, format="str"):
        info = self.info()
        formatted = io.StringIO()
        formatted.write("ScikitLearnClassifier\n")
        formatted.write(" - type: {0}\n".format(info.get('type')))
        formatted.write(" - params: {0}\n"
                        .format(util.format_params(info.get('params'))))
        formatted.write(" - version: {0}\n".format(info.get('version')))
        if isinstance(info['trained'], float):
            date_string = datetime.fromtimestamp(info['trained']).isoformat()
            formatted.write(" - trained: {0}\n".format(date_string))
        else:
            formatted.write(" - trained: {0}\n".format(info.get('trained')))

        formatted.write("\n")
        formatted.write(self.format_stats_str())
        return formatted.getvalue()

    def format_stats_str(self):
        if self.test_stats is None:
            return "No stats available"
        else:
            return "\n".join(statistic.format(self.test_stats[statistic])
                             for statistic in self.test_statistics)

    def format_info_json(self):
        params = {}
        params.update(self.params or {})
        params.update(self.estimator.get_params())

        test_stats = {}
        if self.test_stats is not None:
            for test_stat in self.test_statistics:
                stats = self.test_stats[test_stat]
                test_stats[str(test_stat)] = \
                    test_stat.format(stats, format="json")

        return util.normalize_json({
            'type': self.__class__.__name__,
            'params': params,
            'version': self.version,
            'trained': self.trained,
            'test_stats': test_stats
        })
