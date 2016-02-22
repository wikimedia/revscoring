"""
.. autoclass:: revscoring.ScorerModel
    :members:

.. autoclass:: revscoring.scorer_models.MLScorerModel
    :members:

.. autoclass:: revscoring.scorer_models.ScikitLearnClassifier
    :members:
"""
import pickle

import yamlconf


class ScorerModel:
    """
    A model used to score a revision based on a set of features.
    """

    def __init__(self, features, version=None, stats=None):
        """
        :Parameters:
            features : `list`(`Feature`)
                A list of `Feature` s that will be used to train the model and
                score new observations.
            version : `str`
                A string describing the version of the model.
        """
        self.features = tuple(features)
        self.version = version

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

    def info(self):
        """
        Returns a raw `dict` containing all information about the model.
        """
        raise NotImplementedError()

    def format_info(self, format="str"):
        """
        Returns formatted information about the model.
        """
        raise NotImplementedError()

    @classmethod
    def load(cls, f):
        """
        Reads serialized model information from a file.
        """
        if hasattr(f, 'buffer'):
            return pickle.load(f.buffer)
        else:
            return pickle.load(f)

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
            assert cls != Class

            return Class.from_config(config, name, section_key=section_key)


class MLScorerModel(ScorerModel):
    """
    A machine learned model used to score a revision based on a set of
    features.

    Machine learned models are trained and tested against labeled data.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trained = None
        self.stats = None

    def __getattr__(self, attr):
        if attr is "trained":
            return None
        else:
            raise AttributeError(attr)

    def train(self, values_labels):
        """
        Trains the model on labeled data.

        :Parameters:
            values_scores : `iterable` (( `<feature_values>`, `<label>` ))
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor

        :Returns:
            A dictionary of model statistics.
        """
        raise NotImplementedError()

    def test(self, values_labels, test_statistics=None, store_stats=False):
        """
        Tests the model against a labeled data.  Note that test data should be
        withheld from from train data.

        :Parameters:
            values_labels : `iterable` (( `<feature_values>`, `<label>` ))
                an iterable of labeled data Where <values_labels> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor
            test_statistics : `list` ( :class:`~revscoring.scorer_models.statistics.TestStatistic` )
                a list of test statistics to apply
            store_stats : `bool`
                should the new test statistics overwrite the old (or
                non-existent)

        :Returns:
            A dictionary of test results.
        """  # noqa
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config, name, section_key="scorer_models"):
        """
        Constructs a model from configuration.
        """
        section = config[section_key][name]
        if 'model_file' in section:
            return cls.load(open(section['model_file'], 'rb'))
        else:
            return cls(**{k: v for k, v in section.items() if k != "class"})
