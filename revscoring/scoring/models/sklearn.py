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

import numpy as np

from ...features import vectorize_values
from ..labels import Binarizer, ClassVerifier
from ..statistics import Classification
from . import model, util

logger = logging.getLogger(__name__)


class Classifier(model.Classifier):
    Estimator = NotImplemented
    SUPPORTS_CLASSWEIGHT = False
    BASE_PARAMS = {}

    def __init__(self, features, labels, multilabel=False, version=None,
                 label_weights=None, population_rates=None,
                 scale=False, center=False, statistics=None,
                 estimator=None, **estimator_params):
        statistics = statistics if statistics is not None else Classification(
            labels, multilabel=multilabel, prediction_key="prediction",
            population_rates=population_rates)
        super().__init__(
            features, labels, multilabel=multilabel, version=version,
            population_rates=population_rates, scale=scale, center=center,
            statistics=statistics)
        self.info['score_schema'] = self.build_schema()

        # Initialize the label preprocessor
        if self.multilabel:
            self.label_normalizer = Binarizer(self.labels)
        else:
            self.label_normalizer = ClassVerifier(self.labels)

        self.estimator_params = {}
        # Set label weights as class weights if given
        self.label_weights = label_weights
        if self.label_weights is not None and self.SUPPORTS_CLASSWEIGHT:
            # normalize label weights and apply it as an estimator parameter
            self.estimator_params['class_weight'] = \
                self.label_normalizer.normalize_weights(label_weights)

        if estimator is None:
            params = dict(self.BASE_PARAMS)
            params.update(estimator_params)
            self.estimator_params.update(params)
            self.estimator = self.Estimator(**params)
        else:
            self.estimator = estimator
            self.estimator_params = estimator.get_params()
        self.params.update(self.estimator.get_params())

        if self.multilabel:
            # The collection of estimators per label. Each entry in this
            # collection is a tuple of (label, estimator)
            self.estimators = []
            for idx, label in enumerate(labels):
                params = self.estimator_params.copy()
                # class_weight will be set above if supported
                if 'class_weight' in params:
                    params['class_weight'] = params['class_weight'][idx]
                self.estimators.append((label, self.Estimator(**params)))

        self.params.update({'label_weights': label_weights})

    def _clean_copy(self):
        cls = self.__class__
        kwargs = dict(self.estimator_params)
        kwargs.update(self.params)
        return cls(self.features, version=self.version,
                   **kwargs)

    def preprocess(self, values_labels):
        values, labels = zip(*values_labels)

        # Check that all labels exist in our expected label set and that all
        # expected labels are represented.
        normalized_labels = \
            self.label_normalizer.check_consistency_and_normalize(labels)

        # Re-vectorize features -- this expands/flattens sub-FeatureVectors
        fv_vectors = [vectorize_values(fv) for fv in values]

        # Scale and transform (if applicable)
        scaled_fv_vectors = self.fit_scaler_and_transform(fv_vectors)

        fit_kwargs = {}
        if self.label_weights and not self.SUPPORTS_CLASSWEIGHT:
            # Note that, when class weight is supported, that's handle as a
            # hyper parameter on the estimator.
            fit_kwargs['sample_weight'] = [
                self.label_weights.get(l, 1) for l in labels]
        return scaled_fv_vectors, normalized_labels, fit_kwargs

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
        scaled_fv_vectors, normalized_labels, fit_kwargs = \
            self.preprocess(values_labels)

        # fit the esitimator
        if self.multilabel:
            normalized_labels = np.array(normalized_labels)
            # fit the esitimators
            for idx, estimator in enumerate(self.estimators):
                estimator[1].fit(scaled_fv_vectors, normalized_labels[:, idx],
                                 **fit_kwargs)
        else:
            self.estimator.fit(scaled_fv_vectors, normalized_labels,
                               **fit_kwargs)
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

            * prediction -- The most likely class
        """
        fv_vector = vectorize_values(feature_values)
        scaled_fv_vector = self.apply_scaling(fv_vector)

        prediction = []
        if self.multilabel:
            for _, estimator in self.estimators:
                prediction.append(estimator.predict([scaled_fv_vector])[0])
            prediction = self.label_normalizer.denormalize(prediction)
        else:
            prediction = self.label_normalizer.denormalize(
                self.estimator.predict([scaled_fv_vector])[0])

        doc = {'prediction': prediction}
        return util.normalize_json(doc)

    def score_many(self, feature_values):
        """
        Generates a score for a bunch of revisions based on a set of extracted
        feature_values.

        :Parameters:
            feature_values : collection(`mixed`)
                an ordered collection of values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dict with the fields:

            * prediction -- The most likely class
        """
        # Re-vectorize features -- this expands/flattens sub-FeatureVectors
        fv_vectors = [vectorize_values(fv) for fv in feature_values]

        # Scale and transform (if applicable)
        scaled_fv_vectors = self.fit_scaler_and_transform(fv_vectors)
        predictions = []
        docs = []
        if self.multilabel:
            for _, estimator in self.estimators:
                predictions.append(estimator.predict(scaled_fv_vectors))
            predictions = np.transpose(np.array(predictions))
        else:
            predictions = self.estimator.predict(scaled_fv_vectors)
        for pred in predictions:
            doc = {'prediction': self.label_normalizer.denormalize(pred)}
            docs.append(util.normalize_json(doc))
        return docs

    def build_schema(self):
        if not self.multilabel:
            prediction_type = {
                'description': "The most likely label predicted by " +
                               "the estimator",
                'type': labels2json_type(self.labels)
            }
        else:
            prediction_type = {
                'description': "The most likely labels predicted by " +
                               "the estimator",
                'type': "array",
                'items': {
                    'type': labels2json_type(self.labels)
                }
            }
        return {
            'title': "Scikit learn-based classifier score with " +
                     "probability",
            'type': "object",
            'properties': {
                'prediction': prediction_type
            }
        }


class ProbabilityClassifier(Classifier):

    def __init__(self, features, labels, multilabel=False, statistics=None,
                 population_rates=None, threshold_ndigits=None, **kwargs):
        statistics = statistics if statistics is not None else Classification(
            labels, multilabel=multilabel, prediction_key="prediction",
            decision_key="probability",
            threshold_ndigits=threshold_ndigits or 3,
            population_rates=population_rates)
        super().__init__(features, labels, multilabel=multilabel,
                         statistics=statistics, **kwargs)

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

            * prediction -- The most likely class
            * probability -- A mapping of probabilities for input classes
                             corresponding to the classes the classifier was
                             trained on.  Generating this probability is
                             slower than a simple prediction.
        """
        fv_vector = vectorize_values(feature_values)
        scaled_fv_vector = self.apply_scaling(fv_vector)
        prediction, probas, probability = [], [], []
        if self.multilabel:
            for _, estimator in self.estimators:
                prediction.append(estimator.predict([scaled_fv_vector])[0])
                probas.append(
                    estimator.predict_proba([scaled_fv_vector])[0][1])
            prediction = self.label_normalizer.denormalize(prediction)
            labels = self.labels
            probability = {label: proba
                           for label, proba in zip(labels, probas)}
        else:
            prediction = self.label_normalizer.denormalize(
                self.estimator.predict([scaled_fv_vector])[0])
            labels = self.estimator.classes_
            probas = self.estimator.predict_proba([scaled_fv_vector])[0]
            probability = {label: proba
                           for label, proba in zip(labels, probas)}

        doc = {'prediction': prediction, 'probability': probability}
        return util.normalize_json(doc)

    def score_many(self, feature_values):
        """
        Generates a score for a bunch of revisions based on a set of extracted
        feature_values.

        :Parameters:
            feature_values : array(collection(`mixed`))
                an ordered collection of values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dict with the fields:

            * prediction -- The most likely class
            * probability -- A mapping of probabilities for input classes
                             corresponding to the classes the classifier was
                             trained on.  Generating this probability is
                             slower than a simple prediction.
        """
        # Re-vectorize features -- this expands/flattens sub-FeatureVectors
        fv_vectors = [vectorize_values(fv) for fv in feature_values]

        # Scale and transform (if applicable)
        scaled_fv_vectors = self.fit_scaler_and_transform(fv_vectors)
        predictions, probabilities = [], []
        docs = []
        if self.multilabel:
            for _, estimator in self.estimators:
                predictions.append(estimator.predict(scaled_fv_vectors))
                all_probabilities = estimator.predict_proba(scaled_fv_vectors)
                positive_probabilities = [prob[1]
                                          for prob in all_probabilities]
                probabilities.append(positive_probabilities)

            # This converts probability matrix to [n_samples, n_labels] for
            # ease of iteration
            predictions = np.transpose(np.array(predictions))
            prob_matrix = np.transpose(np.array(probabilities))
            probabilities = []
            labels = self.labels
            for prob in prob_matrix:
                probabilities.append({label: prob
                                      for label, prob in zip(labels, prob)})
        else:
            predictions = self.estimator.predict(scaled_fv_vectors)
            labels = self.estimator.classes_
            probas = self.estimator.predict_proba(scaled_fv_vectors)
            for prob in probas:
                probabilities.append({label: prob
                                      for label, prob in zip(labels, prob)})
        for pred, prob in zip(predictions, probabilities):
            preds = self.label_normalizer.denormalize(pred)
            doc = {'prediction': preds, 'probability': prob}
            docs.append(util.normalize_json(doc))
        return docs

    def build_schema(self):
        schema_doc = super().build_schema()
        schema_doc['properties']['probability'] = {
            'description': "A mapping of probabilities onto " +
                           "each of the potential output labels",
            'type': "object",
            'properties': json.loads(json.dumps(
                {l: {"type": "number"} for l in self.labels}))
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
        return 'boolean'
    else:
        raise ValueError(
            "{0} of type {1} can't be interpereted as a JSON type.".format(
                val, type(val)))
