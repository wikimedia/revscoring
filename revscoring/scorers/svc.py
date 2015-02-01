import pickle
import time

from sklearn import svm
from sklearn.metrics import auc, roc_curve
from statistics import mean, stdev

from .scorer import MLScorer, MLScorerModel


class SVCModel(MLScorerModel):
    
    def __init__(self, features, svc=None, **kwargs):
        super().__init__(features)
        
        if 'probabily' not in kwargs:
            kwargs['probability'] = True
        
        if svc is None:
            self.svc = svm.SVC(**kwargs)
        else:
            self.svc = svc
        
        self.feature_stats = None
        
    def train(self, values_scores, balanced_weight=True):
        """
        :Returns:
            A dictionary with the fields:
            
            * seconds_elapsed -- Time in seconds that fitting the model took
        """
        start = time.time()
        
        values, scores = zip(*values_scores)
        self.feature_stats = self._generate_stats(values)
        scaled_values = list(self._scale_and_center(values, self.feature_stats))
        
        if balanced_weight:
            scores = list(scores)
            counts = {}
            for score in scores:
                counts[score] = counts.get(score, 0) + 1

            weights = [1/(counts[s]/len(scores)) for s in scores]
            self.svc.fit(scaled_values, scores, weights)
        else:
            self.svc.fit(scaled_values, scores)
        
        return {
            'seconds_elapsed': time.time() - start
        }
    
    def score(self, values, probabilities=False):
        """
        :Returns:
            An iterable of dictionaries with the fields:
            
            * predicion -- The most likely class
            * probabilities -- (optional) A vector of probabilities
                               corresponding to the classes the classifier was
                               trained on.  Generating this probability is
                               slower than a simple prediction.
        """
        scaled_values = list(self._scale_and_center(values, self.feature_stats))
        if not probabilities:
            for prediction in self.svc.predict(scaled_values):
                yield {'prediction': prediction}
        else:
            for pred, probas in zip(self.svc.predict(scaled_values),
                                   self.svc.predict_proba(scaled_values)):
                yield {'prediction': pred,
                       'probabilities': list(probas)
                }
                
        
    
    def test(self, values_scores):
        """
        :Returns:
            A dictionary of test statistics with the fields:
            
            * mean.accuracy -- The mean accuracy of classification
        """
        values, scores = zip(*values_scores)
        
        scaled_values = list(self._scale_and_center(values, self.feature_stats))
        
        true_probas = [p[1] for p in self.svc.predict_proba(scaled_values)]
        fpr, tpr, thresholds = roc_curve(scores, true_probas)
        
        table = {}
        predicteds = self.svc.predict(scaled_values)
        for score, predicted in zip(scores, predicteds):
            table[(score, predicted)] = table.get((score, predicted), 0) + 1
        
        return {
            'table': table,
            'mean.accuracy': self.svc.score(list(values), list(scores)),
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

class SVC(MLScorer):
    
    MODEL = SVCModel


class LinearSVCModel(SVCModel):
    
    def __init__(self, features, **kwargs):
        
        if 'kernel' not in kwargs:
            kwargs['kernel'] = "linear"
        
        super().__init__(features, **kwargs)

class LinearSVC(SVC):
    
    MODEL = LinearSVCModel

class RBFSVCModel(SVCModel):
    
    def __init__(self, features, **kwargs):
        
        if 'kernel' not in kwargs:
            kwargs['kernel'] = "rbf"
        
        super().__init__(features, **kwargs)

class RBFSVC(SVC):
    
    MODEL = RBFSVCModel
