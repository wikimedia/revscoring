import pickle
import time

from sklearn import svm
from sklearn.metrics import auc, roc_curve
from statistics import mean, stdev

from .scorer import MLScorer, MLScorerModel
from .util import normalize_json


# Rescales based on prior weights of classes
#def true_proba(p, prior): return (p/prior)/((p/prior)+1)

class SVCModel(MLScorerModel):
    
    def __init__(self, features, language=None, svc=None, **kwargs):
        super().__init__(features, language=language)
        
        if svc is None:
            self.svc = svm.SVC(probability=True, **kwargs)
        else:
            self.svc = svc
        
        self.feature_stats = None
        self.weights = None
        
    def train(self, values_scores, balanced_weight=True):
        """
        :Returns:
            A dictionary with the fields:
            
            * seconds_elapsed -- Time in seconds spent fitting the model
        """
        start = time.time()
        
        values, scores = zip(*values_scores)
        values, scores = list(values), list(scores)
        
        self.feature_stats = self._generate_stats(values)
        scaled_values = list(self._scale_and_center(values, self.feature_stats))
        
        if balanced_weight:
            counts = {}
            for score in scores:
                counts[score] = counts.get(score, 0) + 1
            
            self.weights = {s:1-(counts[s]/len(scores)) for s in counts}
            
            score_weights = [self.weights[s] for s in scores]
            self.svc.fit(scaled_values, scores, score_weights)
        else:
            self.svc.fit(scaled_values, scores)
        
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
        scaled_values = list(self._scale_and_center(values, self.feature_stats))
        predictions = self.svc.predict(scaled_values)
        probabilities = (
            {c:proba for c, proba in zip(self.svc.classes_, probas)}
            for probas in self.svc.predict_proba(scaled_values)
        )
        
        for prediction, probability in zip(predictions, probabilities):
            doc = {
                'prediction': prediction,
                'probability': probability
            }
            yield normalize_json(doc)
                
        
    
    def test(self, values_labels, comparison_class="auto"):
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
        values, labels = list(values), list(labels)
        
        scores = list(self.score(values))
        
        if comparison_class == "auto":
            comparison_class = self.svc.classes_[1]
        elif comparison_class not in self.svc.classes_:
            raise TypeError("comparison_class {0} is not in {1}" \
                            .format(comparison_class, self.svc.classes_))
        
        
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
            'mean.accuracy': self.svc.score(values, labels),
            'roc': {
                'fpr': list(fpr),
                'tpr': list(tpr),
                'thresholds': list(thresholds)
            },
            'auc': auc(fpr, tpr)
        }
    
    def _generate_stats(self, values):
        columns = zip(*values)
        
        stats = tuple((mean(c), stdev(c)) for c in columns)
        
        return stats
    
    def _scale_and_center(self, values, stats):
        
        for feature_values in values:
            yield tuple((val-mean)/max(sd, 0.01)
                        for (mean, sd), val in zip(stats, feature_values))


class LinearSVCModel(SVCModel):
    
    def __init__(self, *args, **kwargs):
        if 'kernel' in kwargs:
            raise TypeError("'kernel' is hard-coded to 'linear'. If you'd " +
                            "like to use a different kernel, use SVCModel.")
        super().__init__(*args, kernel="linear", **kwargs)


class RBFSVCModel(SVCModel):
    
    DEFAULTS = {}
    
    def __init__(self, *args, **kwargs):
        if 'kernel' in kwargs:
            raise TypeError("'kernel' is hard-coded to 'rbf'. If you'd " +
                            "like to use a different kernel, try SVCModel.")
        super().__init__(*args, kernel="rbf", **kwargs)
