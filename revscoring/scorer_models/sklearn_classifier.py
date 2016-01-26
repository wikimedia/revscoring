import io
import time
from datetime import datetime

from sklearn.preprocessing import RobustScaler
from tabulate import tabulate

from .scorer_model import MLScorerModel
from .statistics import pr, roc
from .util import balanced_sample_weights, format_params, normalize_json


class ScikitLearnClassifier(MLScorerModel):

    def __init__(self, features, classifier_model, version=None,
                 balanced_sample_weight=False, scale=False, center=False,
                 test_statistics=None):
        super().__init__(features, version=version)
        self.classifier_model = classifier_model
        self.balanced_sample_weight = balanced_sample_weight
        if scale or center:
            self.scaler = RobustScaler(with_centering=center,
                                       with_scaling=scale)
        else:
            self.scaler = None

        test_statistics = test_statistics or [pr(), roc()]
        self.test_statistics = {ts: None for ts in test_statistics}

        self.stats = None
        self.params = {
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

        values, labels = zip(*values_labels)

        if self.balanced_sample_weight:
            sample_weight = balanced_sample_weights(labels)
        else:
            sample_weight = None

        if self.scaler is not None:
            values = self.scaler.fit_transform(values)

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
        return normalize_json(doc)

    def test(self, values_labels):
        """
        :Returns:
            A dictionary of test statistics with the fields:

            * accuracy -- The mean accuracy of classification
            * table -- A truth table for classification
            * roc
                * auc -- The area under the ROC curve
        """
        values, labels = zip(*values_labels)

        scores = [self.score(feature_values) for feature_values in values]

        self.stats = {
            'table': self._label_table(scores, labels),
            'accuracy': self.classifier_model.score(values, labels)
        }

        for statistic in self.test_statistics:
            self.test_statistics[statistic] = statistic.score(scores, labels)

        return self.stats

    def info(self):
        params = {}
        params.update(self.params or {})
        params.update(self.classifier_model.get_params())

        stats = dict((self.stats or {}).items())
        for statistic in self.test_statistics:
            stats[str(statistic)] = self.test_statistics[statistic]

        return normalize_json({
            'type': self.__class__.__name__,
            'params': params,
            'version': self.version,
            'trained': self.trained,
            'stats': stats
        })

    def format_info(self):
        info = self.info()
        formatted = io.StringIO()
        formatted.write("ScikitLearnClassifier\n")
        formatted.write(" - type: {0}\n".format(info.get('type')))
        formatted.write(" - params: {0}\n"
                        .format(format_params(info.get('params'))))
        formatted.write(" - version: {0}\n".format(info.get('version')))
        if isinstance(info['trained'], float):
            date_string = datetime.fromtimestamp(info['trained']).isoformat()
            formatted.write(" - trained: {0}\n".format(date_string))
        else:
            formatted.write(" - trained: {0}\n".format(info.get('trained')))

        formatted.write("\n")
        formatted.write(self.format_stats())
        return formatted.getvalue()

    def format_stats(self):
        if self.stats is None:
            return "No stats available"
        else:
            formatted = io.StringIO()
            predicted_actuals = self.stats['table'].keys()
            possible = list(set(actual for actual, _ in predicted_actuals))
            possible.sort()

            table_data = []
            for actual in possible:
                table_data.append(
                    [(str(actual))] +
                    [self.stats['table'].get((actual, predicted), 0)
                     for predicted in possible]
                )
            formatted.write(tabulate(
                table_data, headers=["~{0}".format(p) for p in possible]))

            formatted.write("\n\n")

            formatted.write("Accuracy: {0}\n\n".format(self.stats['accuracy']))

            for statistic, stat_doc in self.test_statistics.items():
                formatted.write(statistic.format(stat_doc))
                formatted.write("\n")

            return formatted.getvalue()

    @staticmethod
    def _label_table(scores, labels):

        predicteds = [s['prediction'] for s in scores]

        table = {}
        for pair in zip(labels, predicteds):
            table[pair] = table.get(pair, 0) + 1

        return table
