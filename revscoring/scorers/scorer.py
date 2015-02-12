import pickle


class Scorer:
    """
    Interface for implementing a wide variety of scoring strategies.
    """
    
    def __init__(self, extractor):
        self.extractor = extractor
    
    def score(self, rev_ids):
        """
        Returns a sequence of scores that correspond to <rev_ids>.
        """
        raise NotImplementedError()
    
 
class MLScorer(Scorer):
    """
    Machine Learning Scorer -- a type of Scorer design to support a machine
    learned model of some sort.
    """
    
    MODEL = NotImplemented
    
    def __init__(self, extractor, model):
        """
        Constructs a new scorer with a given model.  Note this scorer expects
        the model to already be trained.
        """
        super().__init__(extractor)
        
        assert isinstance(model, MLScorerModel)
        self.model = model
    
    def score(self, rev_ids, **kwargs):
        values = self.extract(rev_ids)
        
        scores = self.model.score(values, **kwargs)
        
        return scores
    
    def extract(self, rev_ids):
        """
        Extracts the model's features for a set of rev_ids.
        """
        return (self.extractor.extract(rev_id, self.model.features)
                for rev_id in rev_ids)
        
    

class MLScorerModel:
    """
    A machine learned model to be used by a MLScorer
    """
    
    def __init__(self, features, language=None):
        """
        Constructs a new Machine Learned scoring model.
        
        :Parameters:
            extractors : `list`(`Feature`)
                A list of `Feature` s that will be used to train the model and
                score new observations.
        """
        self.features = tuple(features)
        self.language = language
    
    
    def train(self, values_scores):
        """
        Trains the model on labeled data.
        
        :Parameters:
            values_scores : `iterable`((`<feature_values>`, `<score>`))
                an iterable of labeled data Where <values_scores> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor
        
        :Returns:
            A dictionary of model statistics.
        """
        raise NotImplementedError()
        
    
    def test(self, values_scores):
        """
        Tests the model against a labeled data.  Note that test data should be
        withheld from from train data.
        
        :Parameters:
            values_scores : `iterable`((`<feature_values>`, `<score>`))
                an iterable of labeled data Where <values_scores> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor
                
        :Returns:
            A dictionary of test results.
        """
        raise NotImplementedError()
    
    
    def score(self, values, **opts):
        """
        Make a prediction or otherwise use the model to generate a score.
        
        :Parameters:
            values_scores : `iterable`((`<feature_values>`, `<score>`))
                an iterable of labeled data Where <values_scores> is an ordered
                collection of predictive values that correspond to the
                `Feature` s provided to the constructor
            opts : dict
                optional arguments to affect how scores are generated/returned
                
        :Returns:
            A dictionary of score values
        """
        raise NotImplementedError()
    
    
    def _validate_features(self, values):
        """
        Checks the features against provided values to confirm types,
        ordinality, etc.
        """
        return [feature.return_type(value)
                for feature, value in zip(self.feature, values)]
            
    @classmethod
    def load(cls, f):
        """
        Reads serialized model information from a file.
        """
        return pickle.load(f)
    
    def dump(self, f):
        """
        Writes serialized model information to a file.
        """
        pickle.dump(self, f)
