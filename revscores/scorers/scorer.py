

class Scorer:
    
    FEATURES = []
    
    def __init__(self, feature_extractor):
        self.feature_extractor = feature_extractor
    
    def score(self, rev_ids):
        feature_sets = self.feature_extractor.extract(rev_id, self.FEATURES)\
                       for rev_id in rev_ids
        
        return self._score(feature_sets)
    
    def _score(self, feature_set): pass
    
    def _validate_features(self, feature_set):
        [extractor.return_type(feature) \
         for extractor, feature in zip(self.FEATURES, feature_set)]
    
class ModelScorer(Scorer)
    
    def train(self, rev_ids, scores):
        feature_sets = self.feature_extractor.extract(rev_id, self.FEATURES)\
                       for rev_id in rev_ids
        
        return self._train(feature_sets, scores)
        
    def _train(self, feature_sets, scores): pass
    
    def test(self, rev_ids, scores):
        feature_sets = self.feature_extractor.extract(rev_id, self.FEATURES)\
                       for rev_id in rev_ids
        
        return self._test(feature_sets, scores)
    
    def _test(self, feature_sets, scores): pass
