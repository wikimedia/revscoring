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
import pickle
from datetime import datetime
from multiprocessing import Pool, cpu_count

import yamlconf
from sklearn.cross_validation import KFold
from sklearn.preprocessing import RobustScaler

from . import util
from .. import statistics
from ...features import vectorize_values
from ..environment import Environment

logger = logging.getLogger(__name__)


class Model:
    Statistics = NotImplemented
    SCORE_SCHEMA = NotImplemented

    def __init__(self, features, version=None):
        """
        A model used to score things

        :Parameters:
            features : `list`(`Feature`)
                A list of `Feature`s that the model expects to be provided.
            version : `str`
                A string describing the version of the model.
        """
        logger.debug("Initializing Model with {0}")
        self.features = tuple(features)
        self.version = version
        self.environment = Environment()
        self.statistics = self.__init_stats__()

        self.params = {}

    def __init_stats__(self):
        if self.Statistics is NotImplemented:
            return NotImplemented
        else:
            return self.Statistics()

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

    def test(self, values_labels):
        """
        Tests the model against a labeled data.

        :Parameters:
            values_labels : `iterable` (( `<feature_values>`, `<label>` ))
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dictionary of test results.
        """
        # Score all of the observations
        score_labels = [(self.score(values), label)
                        for values, label in values_labels]

        # Fit builtin statistics engine
        self.statistics.fit(score_labels)

        return self.statistics

    def format(self, *args, formatting="str", **kwargs):
        """
        Returns formatted information about the model.
        """
        if formatting == "str":
            return self.format_str(*args, **kwargs)
        elif formatting == "json":
            return self.format_json(*args, **kwargs)
        else:
            raise ValueError("Unknown formatting {0!r}".format(formatting))

    def format_str(self, ndigits=3):
        formatted = self.format_basic_info_str()
        formatted += '\n'
        formatted += self.format_environment_str()
        formatted += '\n'
        formatted += self.format_stats_str(ndigits=ndigits)
        return formatted

    def format_basic_info_str(self):
        formatted = "{0}({1}):\n".format(
            self.__class__.__name__, util.format_params(self.params))
        formatted += " - version: {0}\n".format(self.version)
        return formatted

    def format_environment_str(self):
        formatted = "Enviornment:\n"
        formatted += util.tab_it_in(self.environment.format_str())
        return formatted

    def format_stats_str(self, ndigits=3):
        if self.statistics is NotImplemented:
            return ""
        elif not self.statistics.fitted:
            return "No stats available\n"
        else:
            formatted = "Statistics:\n"
            formatted += util.tab_it_in(
                self.statistics.format_str(ndigits=ndigits))
            return formatted

    def format_json(self, ndigits=3):
        return util.json_normalize({
            'type': self.__class__.__name__,
            'version': self.version,
            'params': self.params,
            'environment': self.environment.format_json(),
            'statistics': self.format_stats_json(ndigits)
        })

    def format_stats_json(self, ndigits=3):
        if not self.statistics.fitted:
            return None
        else:
            return self.statistics.format_json(ndigits=ndigits)

    @classmethod
    def load(cls, f, error_on_env_check=False):
        """
        Reads serialized model information from a file.
        """
        if hasattr(f, 'buffer'):
            model = pickle.load(f.buffer)
        else:
            model = pickle.load(f)

        model.environment.check(raise_exception=error_on_env_check)
        return model

    def dump(self, f):
        """
        Writes serialized model information to a file.
        """

        if hasattr(f, 'buffer'):
            return pickle.dump(self, f.buffer)
        else:
            return pickle.dump(self, f)

    @classmethod
    def from_config(cls, config, name, section_key='scorer_models'):
        section = config[section_key][name]

        if 'module' in section:
            return yamlconf.import_module(section['module'])
        elif 'class' in section:
            class_path = section['class']
            Class = yamlconf.import_module(class_path)
            if 'model_file' in section:
                return Class.load(open(section['model_file'], 'rb'))
            else:
                return Class(**{k: v for k, v in section.items()
                                if k != "class"})


class Learned:

    def __init__(self, *args, scale=False, center=False, **kwargs):
        """
        A machine learned model used to score a revision based on a set of
        features.

        Machine learned models are trained and tested against labeled data.
        """
        super().__init__(*args, **kwargs)
        self.trained = None
        if scale or center:
            self.scaler = RobustScaler(with_centering=center,
                                       with_scaling=scale)
        else:
            self.scaler = None

        self.params.update({
            'scale': scale,
            'center': center
        })

    def fit_scaler_and_transform(self, fv_vectors):
        """
        Fits the internal scale to labeled data.

        :Parameters:
            values_scores : `iterable` (( `<feature_values>`, `<label>` ))
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dictionary of model statistics.
        """
        if self.scaler is not None:
            return self.scaler.fit_and_transform(fv_vectors)
        else:
            return fv_vectors

    def apply_scaling(self, fv_vector):
        if self.scaler is not None:
            if not hasattr(self.scaler, "center_") and \
               not hasattr(self.scaler, "scale_"):
                raise RuntimeError("Cannot scale a vector before " +
                                   "training the scaler")
            fv_vector = self.scaler.transform([fv_vector])[0]

        return fv_vector

    def _clean_copy(self):
        raise NotImplementedError()

    def format_basic_info_str(self):
        formatted = super().format_basic_info_str()
        if self.trained is not None:
            date_string = datetime.fromtimestamp(self.trained).isoformat()
        else:
            date_string = "n/a"
        formatted += " - trained: {0}\n".format(date_string)
        return formatted

    def format_json(self, ndigits=3):
        doc = super().format_json()
        doc['params']['trained'] = self.trained
        return doc

    def cross_validate(self, values_labels, folds=10, processes=None):
        pool = Pool(processes=processes or cpu_count())

        folds_i = KFold(len(values_labels), n_folds=folds, shuffle=True,
                        random_state=0)
        results = pool.map(self._cross_score,
                           ((i, [values_labels[i] for i in train_i],
                                [values_labels[i] for i in test_i])
                            for i, (train_i, test_i) in enumerate(folds_i)))
        agg_score_labels = []
        for score_labels in results:
            agg_score_labels.extend(score_labels)

        self.statistics.fit(agg_score_labels)

        return self.statistics

    def _cross_score(self, i_train_test):
        i, train_set, test_set = i_train_test
        logger.info("Performing cross-validation {0}...".format(i + 1))
        model = self._clean_copy()
        logger.debug("Training cross-validation for {0}...".format(i + 1))
        model.train(train_set)
        logger.debug("Scoring cross-validation for {0}...".format(i + 1))
        return [(model.score(feature_values), label)
                for feature_values, label in test_set]


class Classifier(Learned):
    Statistics = statistics.Classification
    PREDICTION_KEY = NotImplemented

    def __init__(self, *args, labels=None, population_rates=None, **kwargs):
        self.labels = labels
        self.population_rates = population_rates
        super().__init__(*args, **kwargs)

        self.params.update({
            'labels': labels,
            'population_rates': population_rates
        })

    def format_basic_info_str(self):
        formatted = super().format_basic_info_str()
        if self.labels is not None:
            formatted += " - labels: {0}\n".format(self.labels)
        if self.population_rates is not None:
            pop_rates = ", ".join("{0}={1}".format(l, r)
                                  for l, r in self.population_rates.items())
            formatted += " - population_rates: ({0})\n".format(pop_rates)
        return formatted

    def format_json(self, ndigits=3):
        doc = super().format_json()
        doc['params']['labels'] = self.labels
        doc['params']['population_rates'] = self.population_rates
        return doc

    def __init_stats__(self):
        return self.Statistics(
            prediction_key=self.PREDICTION_KEY, labels=self.labels,
            population_rates=self.population_rates)


class ThresholdClassifier(Classifier):
    Statistics = statistics.ThresholdClassification
    PREDICTION_KEY = NotImplemented
    DECISION_KEY = NotImplemented

    def __init__(self, *args, max_thresholds=200,
                 threshold_optimizations=None, **kwargs):
        self.max_thresholds = max_thresholds
        self.threshold_optimizations = threshold_optimizations
        super().__init__(*args, **kwargs)

        self.params.update({
            'max_thresholds': max_thresholds,
            'threshold_optimizations': threshold_optimizations
        })

    def __init_stats__(self):
        return self.Statistics(
            prediction_key=self.PREDICTION_KEY, decision_key=self.DECISION_KEY,
            labels=self.labels, population_rates=self.population_rates,
            max_thresholds=self.max_thresholds)
