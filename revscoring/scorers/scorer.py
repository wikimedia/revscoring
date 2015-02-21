import pickle
import time

from sklearn.metrics import auc, roc_curve

from .util import normalize_json


class Scorer:
    
    def __init__(self, models, extractor):
        for model in models:
            if extractor.language != models.language:
                raise ValueError


class ScorerModel:
    """
    A model used to score a revision based on a set of features.
    """
    
    def __init__(self, name, features, language=None):
        """
        :Parameters:
            features : `list`(`Feature`)
                A list of `Feature` s that will be used to train the model and
                score new observations.
            language : `Language`
                A language to use when applying a feature set.
        """
        self.name     = str(name)
        self.features = tuple(features)
        self.language = language
    
    
    def score(self, feature_values):
        """
        Make a prediction or otherwise use the model to generate a score.
        
        :Parameters:
            feature_values : `iterable`(list(`feature_values`))
                an iterable of labeled data Where <feature_values> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor
                
        :Returns:
            A `dict` of statistics
        """
        raise NotImplementedError()
    
    
    def _validate_features(self, values):
        """
        Checks the features against provided values to confirm types,
        ordinality, etc.
        """
        return [feature.validate(value)
                for feature, value in zip(self.feature, values)]
                    
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


class ScikitLearnClassifier(MLScorerModel):
    
    def __init__(self, name, features, classifier_model, language=None):
        super().__init__(name, features, language=language)
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
    
    def score(self, values):
        """
        :Returns:
            An iterable of dictionaries with the fields:
            
            * predicion -- The most likely class
            * probability -- A mapping of probabilities for input classes
                             corresponding to the classes the classifier was
                             trained on.  Generating this probability is
                             slower than a simple prediction.
        """
        predictions = self.classifier_model.predict(values)
        probabilities = (
            {label:proba for label, proba in zip(self.classifier_model.classes_, probas)}
            for probas in self.classifier_model.predict_proba(values)
        )
        
        for prediction, probability in zip(predictions, probabilities):
            doc = {
                'prediction': prediction,
                'probability': probability
            }
            yield normalize_json(doc)
                
        
    
    def test(self, values_labels, comparison_class=None):
        """
        :Returns:
            A dictionary of test statistics with the fields:
            
            * mean.accuracy -- The mean accuracy of classification
            * auc --
            * table --
            * roc
                * fpr --
                * tpr --
                
        """
        values, labels = zip(*values_labels)
        
        scores = list(self.score(values))
        
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
