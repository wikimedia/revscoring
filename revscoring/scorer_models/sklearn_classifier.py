import io
import time
from datetime import datetime

from sklearn.preprocessing import RobustScaler

from . import util
from .scorer_model import MLScorerModel
from .test_statistics import (accuracy, precision, precision_recall, recall,
                              roc, table)


class ScikitLearnClassifier(MLScorerModel):

    def __init__(self, features, classifier_model, version=None,
                 balanced_sample=False, balanced_sample_weight=False,
                 scale=False, center=False,
                 test_statistics=None):
        super().__init__(features, version=version)
        self.classifier_model = classifier_model
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

        if self.scaler is not None:
            values, labels = zip(*values_labels)
            values = self.scaler.fit_transform(values)
            values_labels = zip(values, labels)

        if self.balanced_sample:
            values_labels = util.balance_sample(values_labels)

        values, labels = zip(*values_labels)

        if self.balanced_sample_weight:
            sample_weight = util.balance_sample_weights(labels)
        else:
            sample_weight = None

        # Fit SVC model
        self.classifier_model.fit(values, labels, sample_weight=sample_weight,
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
        if self.scaler is not None:
            feature_values = self.scaler.transform([feature_values])[0]

        prediction = self.classifier_model.predict([feature_values])[0]
        labels = self.classifier_model.classes_
        probas = self.classifier_model.predict_proba([feature_values])[0]
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

        if self.scaler is not None:
            values = self.scaler.transform(values)

        test_stats = {}
        for statistic in test_statistics:
            test_stats[statistic] = \
                statistic.score(scores, labels)

        if store_stats:
            self.test_statistics = test_statistics
            self.test_stats = test_stats

        return test_stats

    def info(self):
        params = {}
        params.update(self.params or {})
        params.update(self.classifier_model.get_params())

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
            raise TypeError("Format '{0}' not available for {1}."
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
            return "\n".join(stat.format(self.test_stats[stat]) for stat in
                               self.test_statistics)

    def format_info_json(self):
        params = {}
        params.update(self.params or {})
        params.update(self.classifier_model.get_params())

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
