"""
.. autoclass:: revscoring.scorer_models.scorer_model.ScorerModel
    :members:

.. autoclass:: revscoring.scorer_models.scorer_model.MLScorerModel
    :members:

.. autoclass:: revscoring.scorer_models.scorer_model.ScikitLearnClassifier
    :members:
"""
import pickle
import time
import traceback
from statistics import mean, stdev

from sklearn.metrics import auc, roc_curve

import yamlconf

from ..extractors import Extractor
from .util import normalize_json


class ScorerModel:
    """
    A model used to score a revision based on a set of features.
    """

    def __init__(self, features, language=None, version=None):
        """
        :Parameters:
            features : `list`(`Feature`)
                A list of `Feature` s that will be used to train the model and
                score new observations.
            language : `Language`
                A language to use when applying a feature set.
        """
        self.features = tuple(features)
        self.language = language
        self.version  = version

    def __getattr__(self, attr):
        if attr is "version":
            return None
        else:
            raise AttributeError(attr)

    def score(self, feature_values):
        """
        Make a prediction or otherwise use the model to generate a score.

        :Parameters:
            feature_values : collection(`mixed`)
                an ordered collection of values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A `dict` of statistics
        """
        raise NotImplementedError()


    def _validate_features(self, feature_values):
        """
        Checks the features against provided values to confirm types,
        ordinality, etc.
        """
        return [feature.validate(feature_values)
                for feature, value in zip(self.feature, feature_values)]

    def _generate_stats(self, values):
        columns = zip(*values)

        stats = tuple((mean(c), stdev(c)) for c in columns)

        return stats

    def _scale_and_center(self, values, stats):

        for feature_values in values:
            yield (tuple((val-mean)/max(sd, 0.01)
                   for (mean, sd), val in zip(stats, feature_values)))

    @classmethod
    def from_config(cls, config, name, section_key='scorer_models'):
        section = config[section_key][name]

        if 'module' in section:
            return yamlconf.import_module(section['module'])
        elif 'class' in section:
            class_path = section['class']
            Class = yamlconf.import_module(class_path)
            assert cls != Class

            return Class.from_config(config, name, section_key=section_key)


class MLScorerModel(ScorerModel):
    """
    A machine learned model used to score a revision based on a set of features.

    Machine learned models are trained and tested against labeled data.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trained = None

    def train(self, values_labels):
        """
        Trains the model on labeled data.

        :Parameters:
            values_scores : `iterable`((`<values_labels>`, `<label>`))
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dictionary of model statistics.
        """
        raise NotImplementedError()


    def test(self, values_labels):
        """
        Tests the model against a labeled data.  Note that test data should be
        withheld from from train data.

        :Parameters:
            values_labels : `iterable`((`<feature_values>`, `<label>`))
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dictionary of test results.
        """
        raise NotImplementedError()



    @classmethod
    def load(cls, f):
        """
        Reads serialized model information from a file.  Make sure to open
        the file as a binary stream.
        """
        return pickle.load(f)

    def dump(self, f):
        """
        Writes serialized model information to a file.  Make sure to open the
        file as a binary stream.
        """
        pickle.dump(self, f)

    @classmethod
    def from_config(cls, config, name, section_key="scorer_models"):
        """
        Constructs a model from configuration.
        """
        section = config[section_key][name]
        if 'model_file' in section:
            return cls.load(open(section['model_file'], 'rb'))
        else:
            return cls(**{k:v for k,v in section.items() if k != "class"})



class ScikitLearnClassifier(MLScorerModel):

    def __init__(self, features, classifier_model, language=None, version=None):
        super().__init__(features, language=language, version=version)
        self.classifier_model = classifier_model

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
        probability = {label:proba for label, proba in zip(labels, probas)}

        doc = {
            'prediction': prediction,
            'probability': probability
        }
        return normalize_json(doc)


    def test(self, values_labels, comparison_class=None):
        """
        :Returns:
            A dictionary of test statistics with the fields:

            * mean.accuracy -- The mean accuracy of classification
            * auc -- The area under the ROC curve
            * table -- A truth table for classification
            * roc
                * fpr -- A list of false-positive rate values
                * tpr -- A list of true-positive rate values

        """
        values, labels = zip(*values_labels)

        scores = [self.score(feature_values) for feature_values in values]

        if comparison_class == None:
            comparison_class = self.classifier_model.classes_[1]
        elif comparison_class not in self.classifier_model.classes_:
            raise TypeError("comparison_class {0} is not in {1}" \
                            .format(comparison_class,
                                    self.classifier_model.classes_))


        probabilities = [s['probability'][comparison_class]
                         for s in scores]
        predicteds = [s['prediction'] for s in scores]

        true_positives = [l == comparison_class for l in labels]

        fpr, tpr, thresholds = roc_curve(true_positives, probabilities)

        table = {}
        for pair in zip(labels, predicteds):
            table[pair] = table.get(pair, 0) + 1

        return {
            'table': table,
            'mean.accuracy': self.classifier_model.score(values, labels),
            'roc': {
                'fpr': list(fpr),
                'tpr': list(tpr),
                'thresholds': list(thresholds)
            },
            'auc': auc(fpr, tpr)
        }
