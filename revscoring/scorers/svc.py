import random
import time
from collections import defaultdict

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
        
    def train(self, values_labels, balance_labels=True):
        """
        
        :Returns:
            A dictionary with the fields:
            
            * seconds_elapsed -- Time in seconds spent fitting the model
        """
        start = time.time()
        
        if balance_labels: values_labels = self._balance_labels(values_labels)
        values, labels = zip(*values_labels)
        
        # Scale and center
        self.feature_stats = self._generate_stats(values)
        scaled_values = list(self._scale_and_center(values, self.feature_stats))
        
        # Fit SVC model
        self.svc.fit(scaled_values, labels)
        
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
            {label:proba for label, proba in zip(self.svc.classes_, probas)}
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
    
    def _balance_labels(self, values_labels):
        """
        Rebalances a set of a labels based on the label with the most
        observations by sampling (with replacement[1]) from lesser labels.
        
        For example, the following dataset has unbalanced observations:
            
            (0.10  0.20  0.30),  True
            (0.20  0.10  0.30),  False
            (0.10  0.15  0.40),  True
            (0.09  0.40  0.30),  False
            (0.15  0.00  0.28),  True
        
        True` occurs three times while `False` only occurs twice.  This
        function would randomly choose one of the False observations to
        duplicate in order to balance the labels.  For example:
            
            (0.10  0.20  0.30),  True
            (0.20  0.10  0.30),  False
            (0.20  0.10  0.30),  False
            (0.10  0.15  0.40),  True
            (0.09  0.40  0.30),  False
            (0.15  0.00  0.28),  True
        
        Why would anyone want to do this?  If you don't, SVM's
        predict_proba() will return values that don't represent it's
        predictions.  This is a hack.  It seems to work in practice with large
        numbers of observations.
        
        1. See https://www.ma.utexas.edu/users/parker/sampling/repl.htm for a
           discussion of "sampling with replacement".
                
        """
        #Group observations by label
        groups = defaultdict(list)
        for feature_values, label in values_labels:
            groups[label].append(feature_values)
        
        # Find out which label occurs most often and how often
        max_label_n = max(len(groups[label]) for label in groups)
        
        # Resample the max observations from each group of observations.
        new_values_labels = []
        for label in groups:
            new_values_labels.extend((random.choice(groups[label]), label)
                                      for i in range(max_label_n))
        
        # Shuffle the observations again before returning.
        random.shuffle(new_values_labels)
        return new_values_labels
    
    def _generate_stats(self, values):
        columns = zip(*values)
        
        stats = tuple((mean(c), stdev(c)) for c in columns)
        
        return stats
    
    def _scale_and_center(self, values, stats):
        
        for feature_values in values:
            yield (tuple((val-mean)/max(sd, 0.01)
                   for (mean, sd), val in zip(stats, feature_values)))


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
