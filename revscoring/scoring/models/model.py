"""
All scoring models are an implementation of :class:`revscoring.Model`.

.. autoclass:: revscoring.scoring.models.Learned
    :members:

.. autoclass:: revscoring.scoring.models.Classifier
    :members:
"""
import bz2
import logging
import pickle
from multiprocessing import Pool, cpu_count

import yamlconf
from sklearn.model_selection import KFold
from sklearn.preprocessing import RobustScaler

from ..environment import Environment
from ..model_info import ModelInfo

logger = logging.getLogger(__name__)


class Model:
    SCORE_SCHEMA = NotImplemented

    def __init__(self, features, version=None, environment=None,
                 statistics=None, additional_info=None):
        """
        A model used to score things

        :Parameters:
            features : `list`(`Feature`)
                A list of `Feature`s that the model expects to be provided.
            version : `str`
                A string describing the version of the model.
        """
        logger.debug("Initializing Model with {0}".format(features))
        self.features = tuple(features)
        self.params = {}
        self.version = version

        self.info = ModelInfo()
        """
        A :class:`revscoring.scoring.ModelInfo` instance that implements
        :func:`~revscoring.scoring.ModelInfo.lookup` and
        :func:`~revscoring.scoring.ModelInfo.format` -- both of which
        act as an index into information about a model.
        """
        self.info['type'] = self.__class__.__name__
        self.info['version'] = version
        self.info['params'] = self.params
        for key, value in (additional_info or {}):
            self.info[key] = value
        self.info['environment'] = environment or Environment()
        if statistics is not None:
            self.info['statistics'] = statistics

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
        self.info['statistics'].fit(score_labels)

        return self.info['statistics']

    @classmethod
    def load(cls, f, error_on_env_check=False):
        """
        Reads serialized model information from a file.
        """
        if hasattr(f, 'buffer'):
            model = pickle.load(f.buffer)
        else:
            model = pickle.load(f)

        model.info['environment'].check(raise_exception=error_on_env_check)
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
                # TODO: Cache the model file for reuse across workers?
                with open_file(section['model_file']) as stream:
                    return Class.load(stream)
            else:
                return Class(**{k: v for k, v in section.items()
                                if k != "class"})


def open_file(path):
    if path[-4:] == ".bz2" or path[-6:] == ".bzip2":
        return bz2.open(path, 'rb')
    else:
        return open(path, 'rb')


class Learned(Model):

    def __init__(self, *args, scale=False, center=False, **kwargs):
        """
        A machine learned model.  Beyond :class:`revscoring.Model`, this
        "Learned" models implement
        :func:`~revscoring.scoring.models.Learned.fit` and
        :func:`~revscoring.scoring.models.Learned.cross_validate`.
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

    def train(self, values_labels):
        """
        Fits the model using labeled data by learning its shape.

        :Parameters:
            values_labels : [( `<feature_values>`, `<label>` )]
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                :class:`revscoring.Feature` s provided to the constructor
        """
        raise NotImplementedError()

    def fit_scaler_and_transform(self, fv_vectors):
        """
        Fits the internal scale to labeled data.

        :Parameters:
            fv_vectors : `iterable` (( `<feature_values>`, `<label>` ))
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dictionary of model statistics.
        """
        if self.scaler is not None:
            return self.scaler.fit_transform(fv_vectors)
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

    def cross_validate(self, values_labels, folds=10, processes=1):
        """
        Trains and tests the model agaists folds of labeled data.

        :Parameters:
            values_labels : [( `<feature_values>`, `<label>` )]
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor
            folds : `int`
                When set to 1, cross-validation will run in the parent thread.
                When set to 2 or greater, a :class:`multiprocessing.pool.Pool`
                will be created.
        """
        folds_i = KFold(n_splits=folds, shuffle=True,
                        random_state=0)
        if processes == 1:
            mapper = map
        else:
            pool = Pool(processes=processes or cpu_count())
            mapper = pool.map
        results = mapper(self._cross_score,
                         ((i, [values_labels[i] for i in train_i],
                           [values_labels[i] for i in test_i])
                          for i, (train_i, test_i) in enumerate(
                              folds_i.split(values_labels))))
        agg_score_labels = []
        for score_labels in results:
            agg_score_labels.extend(score_labels)

        self.info['statistics'].fit(agg_score_labels)

        return self.info['statistics']

    def _cross_score(self, i_train_test):
        i, train_set, test_set = i_train_test
        logger.info("Performing cross-validation {0}...".format(i + 1))
        model = self._clean_copy()
        logger.debug("Training cross-validation for {0}...".format(i + 1))
        model.train(train_set)
        logger.debug("Scoring cross-validation for {0}...".format(i + 1))
        feature_values, labels = map(list, zip(*test_set))
        docs = model.score_many(feature_values)
        return list(zip(docs, labels))


class Classifier(Learned):

    def __init__(self, features, labels, multilabel=False,
                 population_rates=None, **kwargs):
        self.labels = labels
        self.multilabel = multilabel
        self.population_rates = population_rates
        super().__init__(features, **kwargs)

        self.params.update({
            'labels': labels,
            'multilabel': multilabel,
            'population_rates': population_rates
        })
