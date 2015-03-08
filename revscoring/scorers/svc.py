import random
import time
from collections import defaultdict

from sklearn import svm

from .scorer import ScikitLearnClassifier


class SVCModel(ScikitLearnClassifier):
    
    def __init__(self, features, language=None, svc=None, **kwargs):
        if svc is None:
            classifier_model = svm.SVC(probability=True, **kwargs)
        else:
            classifier_model = svc
        
        super().__init__(features, classifier_model, language=language)
        
        self.feature_stats = None
        self.weights = None
        
    def train(self, values_labels, balance_labels=True):
        """
        
        :Returns:
            A dictionary with the fields:
            
            * seconds_elapsed -- Time in seconds spent fitting the model
        """
        start = time.time()
        
        # Balance labels
        if balance_labels: values_labels = self._balance_labels(values_labels)
        
        # Split out feature_values
        feature_values, labels = zip(*values_labels)
        
        # Scale and center feature_values
        self.feature_stats = self._generate_stats(feature_values)
        scaled_values = self._scale_and_center(feature_values,
                                               self.feature_stats)
            
        # Train the classifier
        stats = super().train(zip(scaled_values, labels))
        
        # Overwrite seconds elapsed to account for time spent
        # balancing and scaling
        stats['seconds_elapsed'] = time.time() - start
        
        return stats
    
    def score(self, feature_values):
        scaled_values = next(self._scale_and_center([feature_values],
                                                    self.feature_stats))
        
        return super().score(scaled_values)
    
    
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
        numbers of observations[2].
        
        1. See https://www.ma.utexas.edu/users/parker/sampling/repl.htm for a
           discussion of "sampling with replacement".
        2. http://nbviewer.ipython.org/github/halfak/Objective-Revision-Evaluation-Service/blob/ipython/ipython/Wat%20predict_proba.ipynb
                
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


class LinearSVCModel(SVCModel):
    
    def __init__(self, *args, **kwargs):
        if 'kernel' in kwargs:
            raise TypeError("'kernel' is hard-coded to 'linear'. If you'd " +
                            "like to use a different kernel, use SVCModel.")
        super().__init__(*args, kernel="linear", **kwargs)


class RBFSVCModel(SVCModel):
    
    def __init__(self, *args, **kwargs):
        if 'kernel' in kwargs:
            raise TypeError("'kernel' is hard-coded to 'rbf'. If you'd " +
                            "like to use a different kernel, try SVCModel.")
        super().__init__(*args, kernel="rbf", **kwargs)
