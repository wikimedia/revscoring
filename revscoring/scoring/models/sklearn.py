"""
.. autoclass:: revscoring.Model
    :members:

.. autoclass:: revscoring.scoring.LearnedModel
    :members:

.. autoclass:: revscoring.scoring.Classifier
    :members:

.. autoclass:: revscoring.scoring.ThresholdClassifier
    :members:
"""
import logging
import time

from . import model, util

logger = logging.getLogger(__name__)


class Model(model.LearnedModel):
    Estimator = NotImplemented
    BASE_PARAMS = {}

    def __init__(self, features, version=None,
                 scale=False, center=False,
                 estimator=None, **estimator_params):
        super().__init__(features, version=version,
                         scale=scale, center=center)
        if estimator is None:
            params = dict(self.BASE_PARAMS)
            params.update(estimator_params)
            self.estimator_params = params
            self.estimator = self.Estimator(**params)
        else:
            self.estimator = estimator
            self.estimator_params = estimator.get_params()

        self.params.update(self.estimator.get_params())

    def _clean_copy(self):
        cls = self.__class__
        kwargs = dict(self.estimator.get_params())
        kwargs.update(self.params)
        return cls(self.features, version=self.version, **kwargs)

    def train(self, values_labels, **kwargs):
        """
        :Returns:
            A dictionary with the fields:

            * seconds_elapsed -- Time in seconds spent fitting the model
        """
        start = time.time()
        super().train(values_labels)
        values, labels = zip(*values_labels)
        values = [self.pre_process_vector(fv) for fv in values]

        # fit the esitimator
        self.estimator.fit(values, labels, **kwargs)
        self.trained = time.time()

        return {'seconds_elapsed': time.time() - start}


class Classifier(Model, model.Classifier):
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
        feature_values = self.pre_process_vector(feature_values)

        prediction = self.estimator.predict([feature_values])[0]

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
        feature_values = self.pre_process_vector(feature_values)

        prediction = self.estimator.predict([feature_values])[0]
        labels = self.estimator.classes_
        probas = self.estimator.predict_proba([feature_values])[0]
        probability = {label: proba for label, proba in zip(labels, probas)}

        doc = {'prediction': prediction, 'probability': probability}
        return util.normalize_json(doc)
