import pickle
import time
import traceback
from statistics import mean, stdev

from sklearn.metrics import auc, roc_curve

import yamlconf

from ..dependent import expand_many
from ..extractors import Extractor
from .util import normalize_json


class Scorer:

    def __init__(self, model_map, extractor):
        """
        :Parameters:
            model_map : dict
                A mapping between model names and `ScorerModel` s.
            extractor : `revscoring.extractors.Extractor`
                An extractor to use for gathering feature values
        """
        self._check_compatibility(model_map, extractor)
        self.model_map = model_map
        self.extractor = extractor

    def dependencies(self, models=None):
        return expand_many(self.features(models))

    def features(self, models=None):
        """
        Gathers a single tuple of unique features needed by the models
        """
        # If no particular model is requested, generate for all available models
        models = models or self.model_map.keys()

        return tuple({feature for name in models
                      for feature in self.model_map[name].features})

    def score(self, rev_id, models=None, context=None, cache=None):
        return next(self.score_many([rev_id], models=models, context=context,
                                    caches={rev_id: cache}))

    def score_many(self, rev_ids, models=None, context=None,
                         caches=None):
        # If no particular model is requested, generate for all available models
        models = models or self.model_map.keys()

        features = self.features(models)

        error_feature_values = \
                self.extractor.extract_many(rev_ids, features,
                                            caches=caches, context=context)
        for rev_id, (err, feature_values) in zip(rev_ids, error_feature_values):

            if err is not None:
                yield {"error": {'type': str(type(err)), 'message': str(err)}}
            else:
                feature_map = {f:v for f,v in zip(features, feature_values)}

                score_map = {}
                for name in models:
                    model = self.model_map[name]
                    feature_values = [feature_map[f] for f in model.features]
                    try:
                        score_map[name] = model.score(feature_values)
                    except Exception as e:
                        score_map[name] = {
                            "error": {'type': str(type(e)), 'message': str(e),
                                      'traceback': traceback.format_exc()}
                        }

                yield score_map

    def _check_compatibility(self, model_map, extractor):
        for _, model in model_map.items():
            if model.language is not None and \
               extractor.language != model.language:
                raise ValueError(("Model language {0} does not match " +
                                  "extractor language {1}")\
                                 .format(model.language.name,
                                         extractor.language.name))

    @classmethod
    def from_config(cls, config, name, section_key="scorers"):
        """
        Expects:

            scorers:
                enwiki:
                    models:
                        damaging: enwiki_damaging_2014
                        good-faith: enwiki_good-faith_2014
                    extractor: enwiki
                ptwiki:
                    models:
                        damaging: ptwiki_damaging_2014
                        good-faith: ptwiki_good-faith_2014
                    extractor: ptwiki

            extractors:
                enwiki_api: ...
                ptwiki_api: ...

            scorer_models:
                enwiki_damaging_2014: ...
                enwiki_good-faith_2014: ...
        """
        section = config[section_key][name]

        model_map = {}
        for name, key in section['models'].items():
            model = ScorerModel.from_config(config, key)
            model_map[name] = model

        extractor = Extractor.from_config(config, section['extractor'])

        return cls(model_map, extractor)


class ScorerModel:
    """
    A model used to score a revision based on a set of features.
    """

    def __init__(self, features, language=None):
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
            return Class.from_config(config, name)


class MLScorerModel(ScorerModel):
    """
    A machine learned model used to score a revision based on a set of features.

    Machine learned models are trained and tested against labeled data.
    """

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

    def __init__(self, features, classifier_model, language=None):
        super().__init__(features, language=language)
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
