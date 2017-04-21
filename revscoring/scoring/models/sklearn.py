"""
.. autoclass:: revscoring.scoring.models.sklearn.Classifier
    :members:

.. autoclass:: revscoring.scoring.models.sklearn.ThresholdClassifier
    :members:
"""
import logging
import time

from . import model, util
from .. import statistics
from ...features import vectorize_values

logger = logging.getLogger(__name__)


class Classifier(model.Classifier, model.Model):
    Estimator = NotImplemented
    BASE_PARAMS = {}
    SCORE_SCHEMA = {
        'title': "Scikit learn-based classifier score",
        'type': "object",
        'properties': {
            'prediction': {
                'description': "The most likely label predicted by the " +
                               "estimator",
                'type': ['string', 'boolean']
            }
        }
    }
    PREDICTION_KEY = "prediction"

    def __init__(self, features, version=None,
                 labels=None, label_weights=None, population_rates=None,
                 scale=False, center=False,
                 estimator=None, **estimator_params):
        super().__init__(
            features, version=version, labels=labels,
            population_rates=population_rates, scale=scale, center=center)
        self.label_weights = label_weights

        if estimator is None:
            params = dict(self.BASE_PARAMS)
            params.update(estimator_params)
            self.estimator_params = params
            self.estimator = self.Estimator(**params)
        else:
            self.estimator = estimator
            self.estimator_params = estimator.get_params()

        self.params.update(self.estimator.get_params())
        self.params.update({'label_weights': label_weights})

    def _clean_copy(self):
        cls = self.__class__
        kwargs = dict(self.estimator_params)
        kwargs.update(self.params)
        return cls(self.features, version=self.version,
                   **kwargs)

    def train(self, values_labels, **kwargs):
        """
        :Returns:
            A dictionary with the fields:

            * seconds_elapsed -- Time in seconds spent fitting the model
        """
        logger.info("Training {0} with {1} observations"
                    .format(self.__class__.__name__, len(values_labels)))
        start = time.time()
        values, labels = zip(*values_labels)
        fv_vectors = [vectorize_values(fv) for fv in values]
        scaled_fv_vectors = self.fit_scaler_and_transform(fv_vectors)

        unique_labels = set(labels)
        if len(unique_labels) < 2:
            raise ValueError("Only one label present in the training set {0}"
                             .format(unique_labels))

        fit_kwargs = {}
        if self.label_weights:
            fit_kwargs['sample_weight'] = [
                self.label_weights.get(l, 1) for l in labels]

        # fit the esitimator
        self.estimator.fit(scaled_fv_vectors, labels, **fit_kwargs)
        self.trained = time.time()

        return {'seconds_elapsed': time.time() - start}

    def format_basic_info_str(self):
        formatted = super().format_basic_info_str()
        if self.label_weights is not None:
            formatted += " - label_weights: {0}\n".format(self.label_weights)
        return formatted

    def format_json(self, ndigits=3):
        doc = super().format_json()
        doc['params']['label_weights'] = self.label_weights
        return util.normalize_json(doc)

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
        """
        fv_vector = vectorize_values(feature_values)
        scaled_fv_vector = self.apply_scaling(fv_vector)

        prediction = self.estimator.predict([scaled_fv_vector])[0]

        doc = {'prediction': prediction}
        return util.normalize_json(doc)


class ProbabilityClassifier(model.ThresholdClassifier, Classifier):
    SCORE_SCHEMA = {
        'title': "Scikit learn-based classifier score with probability",
        'type': "object",
        'properties': {
            'prediction': {
                'description': "The most likely label predicted by the " +
                               "estimator",
                'type': ['string', 'boolean']
            },
            'probability': {
                'description': "A mapping of probabilities onto each of the " +
                               "potential output labels",
                'type': "object",
                'additionalProperties': {
                    'type': "number"
                }
            }
        }
    }
    DECISION_KEY = "probability"
    PREDICTION_KEY = "prediction"
    Statistics = statistics.ThresholdClassification

    def __init_stats__(self):
        return self.Statistics(
            prediction_key=self.PREDICTION_KEY, labels=self.labels,
            decision_key=self.DECISION_KEY, max_thresholds=self.max_thresholds,
            threshold_optimizations=self.threshold_optimizations,
            population_rates=self.population_rates)

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
        fv_vector = vectorize_values(feature_values)
        scaled_fv_vector = self.apply_scaling(fv_vector)

        prediction = self.estimator.predict([scaled_fv_vector])[0]
        labels = self.estimator.classes_
        probas = self.estimator.predict_proba([scaled_fv_vector])[0]
        probability = {label: proba for label, proba in zip(labels, probas)}

        doc = {'prediction': prediction, 'probability': probability}
        return util.normalize_json(doc)
