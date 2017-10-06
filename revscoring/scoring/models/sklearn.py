"""
Implements the basics of all sklearn based models.

.. autoclass:: revscoring.scoring.models.sklearn.Classifier
    :members:

.. autoclass:: revscoring.scoring.models.sklearn.ProbabilityClassifier
    :members:
"""
import json
import logging
import time

from . import model, util
from ...features import vectorize_values
from ..statistics import Classification
from ..util import check_label_consistency

logger = logging.getLogger(__name__)


class Classifier(model.Classifier):
    Estimator = NotImplemented
    BASE_PARAMS = {}

    def __init__(self, features, labels, version=None,
                 label_weights=None, population_rates=None,
                 scale=False, center=False, statistics=None,
                 estimator=None, **estimator_params):
        statistics = statistics if statistics is not None else Classification(
            labels, prediction_key="prediction",
            population_rates=population_rates)
        super().__init__(
            features, labels, version=version,
            population_rates=population_rates, scale=scale, center=center,
            statistics=statistics)
        self.info['score_schema'] = self.build_schema()
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
        Fits the internal model to the provided `values_labels`.

        :Returns:
            A dictionary with the fields:

            * seconds_elapsed -- Time in seconds spent fitting the model
        """
        logger.info("Training {0} with {1} observations"
                    .format(self.__class__.__name__, len(values_labels)))
        start = time.time()
        values, labels = zip(*values_labels)

        # Check that all labels exist in our expected label set and that all
        # expected labels are represented.
        check_label_consistency(labels, self.labels)

        # Re-vectorize features -- this expands/flattens sub-FeatureVectors
        fv_vectors = [vectorize_values(fv) for fv in values]

        # Scale and transform (if applicable)
        scaled_fv_vectors = self.fit_scaler_and_transform(fv_vectors)

        fit_kwargs = {}
        if self.label_weights:
            fit_kwargs['sample_weight'] = [
                self.label_weights.get(l, 1) for l in labels]

        # fit the esitimator
        self.estimator.fit(scaled_fv_vectors, labels, **fit_kwargs)
        self.trained = time.time()

        return {'seconds_elapsed': time.time() - start}

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

    def build_schema(self):
        return {
            'title': "Scikit learn-based classifier score with " +
                     "probability",
            'type': "object",
            'properties': {
                'prediction': {
                    'description': "The most likely label predicted by " +
                                   "the estimator",
                    'type': labels2json_type(self.labels)
                }
            }
        }


class ProbabilityClassifier(Classifier):

    def __init__(self, features, labels, statistics=None,
                 population_rates=None, threshold_ndigits=None, **kwargs):
        statistics = statistics if statistics is not None else Classification(
            labels, prediction_key="prediction", decision_key="probability",
            threshold_ndigits=threshold_ndigits or 3,
            population_rates=population_rates)
        super().__init__(features, labels, statistics=statistics, **kwargs)

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

    def build_schema(self):
        schema_doc = super().build_schema()
        schema_doc['properties']['probability'] = {
            'description': "A mapping of probabilities onto " +
                           "each of the potential output labels",
            'type': "object",
            'properties': json.loads(json.dumps(
                {l: "number" for l in self.labels}))
        }
        return schema_doc


def labels2json_type(labels):
    unique_json_types = set(label2json_type(l) for l in labels)

    if len(unique_json_types) == 1:
        return unique_json_types.pop()
    else:
        return list(sorted(unique_json_types))


def label2json_type(val):

    if type(val) in (int, float):
        return 'number'
    elif isinstance(val, str):
        return 'string'
    elif isinstance(val, bool):
        return 'bool'
    else:
        raise ValueError(
            "{0} of type {1} can't be interpereted as a JSON type.".format(
                val, type(val)))
