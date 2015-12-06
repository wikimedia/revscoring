import io
import time
from datetime import datetime

from sklearn.metrics import auc, roc_curve
from tabulate import tabulate

from .scorer_model import MLScorerModel
from .util import normalize_json


class ScikitLearnClassifier(MLScorerModel):

    def __init__(self, features, classifier_model, version=None):
        super().__init__(features, version=version)
        self.classifier_model = classifier_model
        self.stats = None

    def __getattr__(self, attr):
        if attr is "stats":
            return None
        else:
            raise AttributeError(attr)

    def train(self, values_labels):
        """

        :Returns:
            A dictionary with the fields:

            * seconds_elapsed -- Time in seconds spent fitting the model
        """
        start = time.time()

        values, labels = zip(*values_labels)

        # Fit SVC model
        self.classifier_model.fit(values, labels)
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
            'accuracy': self.classifier_model.score(values, labels),
            'roc': self._roc_stats(scores, labels,
                                   self.classifier_model.classes_)
        }
        return self.stats

    def info(self):
        return normalize_json({
            'type': self.__class__.__name__,
            'version': self.version,
            'trained': self.trained,
            'stats': self.stats
        })

    def format_info(self):
        info = self.info()
        formatted = io.StringIO()
        formatted.write("ScikitLearnClassifier\n")
        formatted.write(" - type: {0}\n".format(info.get('type')))
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
            possible = list(set(actual for _, actual in predicted_actuals))
            possible.sort()

            formatted.write("Accuracy: {0}\n\n".format(self.stats['accuracy']))
            if 'auc' in self.stats['roc']:
                formatted.write("ROC-AUC: {0}\n\n"
                                .format(self.stats['roc']['auc']))
            else:
                formatted.write("ROC-AUC:\n")

                table_data = [[comparison_label,
                               self.stats['roc'][comparison_label]['auc']]
                              for comparison_label in possible]
                formatted.write(tabulate(table_data))
                formatted.write("\n\n")

            table_data = []

            for actual in possible:
                table_data.append(
                    [(str(actual))] +
                    [self.stats['table'].get((predicted, actual), 0)
                     for predicted in possible]
                )
            formatted.write(tabulate(
                table_data,
                headers=["~{0}".format(p) for p in possible]))

            return formatted.getvalue()

    @classmethod
    def _roc_stats(cls, scores, labels, possible_labels):

        if len(possible_labels) <= 2:
            # Binary classification, class choice doesn't matter.
            comparison_label = possible_labels[0]
            return cls._roc_single_class(scores, labels, comparison_label)
        else:
            roc_stats = {}
            for comparison_label in possible_labels:
                roc_stats[comparison_label] = \
                    cls._roc_single_class(scores, labels, comparison_label)

            return roc_stats

    @classmethod
    def _roc_single_class(cls, scores, labels, comparison_label):
        probabilities = [s['probability'][comparison_label]
                         for s in scores]

        true_positives = [l == comparison_label for l in labels]
        fpr, tpr, thresholds = roc_curve(true_positives, probabilities)

        return {
            'auc': auc(fpr, tpr)
        }

    @staticmethod
    def _label_table(scores, labels):

        predicteds = [s['prediction'] for s in scores]

        table = {}
        for pair in zip(labels, predicteds):
            table[pair] = table.get(pair, 0) + 1

        return table
