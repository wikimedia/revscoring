

class Scorer:
    """
    Interface for implementing a wide variety of scoring strategies.
    """
    
    def __init__(self, source):
        self.source = source
    
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
    
    def __init__(self, source, model):
        """
        Constructs a new scorer with a given model.  Note this scorer expects
        the model to already be trained.
        """
        super().__init__(source)
        
        assert isinstance(model, self.MODEL)
        self.model = model
    
    def score(self, rev_ids):
        values = self.extract(rev_ids)
        
        scores = self.model.score(values)
        
        return scores
    
    def extract(self, rev_ids):
        """
        Extracts the model's features for a set of rev_ids.
        """
        return (self.source.extract(rev_id, self.model.features)
                for rev_id in rev_ids)
        
    

class MLScorerModel:
    """
    A machine learned model to be used by a MLScorer
    """
    
    def __init__(self, features):
        """
        Constructs a new Machine Learned scoring model.
        
        :Parameters:
            extractors : `list`(`feature extractor`)
                A list of extractors that will be used to train
        """
        self.features = tuple(features)
    
    
    def train(self, values_scores):
        """
        Trains the model on an iterable of labeled data (<features>, <score>).
        """
        raise NotImplementedError()
        
    
    def test(self, values_scores):
        """
        Returns a dictionary of test results based on an iterable of labeled data (<features>, <score>)
        """
        raise NotImplementedError()
    
    
    def score(self, values):
        """
        Returns a prediction based on a set of features.
        """
        raise NotImplementedError()
    
    
    def _validate_features(self, values):
        """
        Checks the features against provided values to confirm types, ordinality, etc.
        """
        return [feature.return_type(value)
                for feature, value in zip(self.feature, values)]
            
    def dump(self, f):
        """
        Writes serialized model information to a file.
        """
        raise NotImplementedError()

    @classmethod
    def load(cls, f):
        """
        Reads serialized model information from a file.
        """
        raise NotImplementedError()
