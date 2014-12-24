import pickle
import time

from numpy import array
from sklearn import svm
from sklearn.metrics import auc, roc_curve

from .scorer import MLScorer, MLScorerModel


class LinearSVCModel(MLScorerModel):
    
    def __init__(self, features, **kwargs):
        super().__init__(features)
        
        self.svc = svm.SVC(kernel="linear", probability=True, **kwargs)
    
    def train(self, values_scores):
        """
        :Returns:
            An empty dictionary
        """
        values, scores = zip(*values_scores)
        start = time.time()
        self.svc.fit(values, scores)
        
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
        values = list(values)
        if not probabilities:
            for prediction in self.svc.predict(values):
                yield {'prediction': prediction}
        else:
            for pred, proba in zip(self.svc.predict(values),
                                   self.svc.predict_proba(values)):
                yield {'prediction': pred,
                       'probabilities': list(proba)}
                
        
    
    def test(self, values_scores):
        """
        :Returns:
            A dictionary of test statistics with the fields:
            
            * mean.accuracy -- The mean accuracy of classification
        """
        values, scores = zip(*values_scores)
        
        true_probas = [p[1] for p in self.svc.predict_proba(list(values))]
        fpr, tpr, thresholds = roc_curve(scores, true_probas)
        
        return {
            'mean.accuracy': self.svc.score(list(values), list(scores)),
            'roc': {
                'fpr': list(fpr),
                'tpr': list(tpr),
                'thresholds': list(thresholds)
            },
            'auc': auc(fpr, tpr)
        }
        
    def dump(self, f):
        
        pickle.dump(self, f)
    
    @classmethod
    def load(cls, f):
        
        return pickle.load(f)

class LinearSVC(MLScorer):
    
    MODEL = LinearSVCModel
