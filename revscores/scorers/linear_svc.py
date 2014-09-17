from sklearn import svm

from ..feature_extractors import (bytes_changed, is_anon, is_custom_comment,
                                  is_mainspace, is_previous_user_same,
                                  is_section_comment, num_words_added,
                                  num_words_removed)
from .scorer import Scorer


def LinearSVCDiff(ModelScorer):
    
    VERSION = "0.0.1"
    
    EXTRACTORS = [
        bytes_changed,
        is_anon,
        is_custom_comment,
        is_mainspace,
        is_previous_user_same,
        is_section_comment,
        num_words_added,
        num_words_removed
    ]
    
    def __init__(self, *, feature_extractor, classifier=None, **kwargs):
        super().__init__(self, feature_extractor)
        
        if classifier is not None:
            self.classifier = svm.SVC(**kwargs)
        else:
            self.classifier = classifier
        
        
    def _train(self, feature_sets, scores):
        feature_sets = self._validate(feature_set) \
                       for feature_set in feature_sets
        
        self.classifier.fit(feature_sets, scores)
    
    def _test(self, feature_sets, scores):
        feature_sets = self._validate(feature_set) \
                       for feature_set in feature_sets
        
        return self.classifier.score(feature_sets, scores)
    
    
    def _predict(self, feature_sets, proba=False):
        feature_sets = self._validate(feature_set) \
                       for feature_set in feature_sets
        
        if not proba:
            return self.classifier.predict_proba(feature_sets)
        else:
            return self.classifier.predict(feature_sets)
