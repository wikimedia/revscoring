from numpy import array
from sklearn import svm

from .scorer import MLScorer, MLScorerModel


class LinearSVCModel(MLScorerModel):
    
    def __init__(self, features, **kwargs):
        super().__init__(features)
        
        self.svc = svm.SVC(**kwargs)
    
    def train(self, values_scores):
        
        x_values, y_values = self.convert_to_arrays(values_scores)
        
        return self.svc.fit(x_values, y_values)
    
    def test(self, values_scores):
        
        x_values, y_values = self.convert_to_arrays(values_scores)
        
        return self.svc.score(x_values, y_values)
        
    
    @classmethod
    def convert_to_arrays(cls, values_scores):
        """
        Converts an iterable of <values> and <score> into a column-major
        array.
        
        1  2  3
        4  5  6
        7  8  9
        
        Column major = [[1,4,7], [2,5,8], [3,6,9]]
        Row major = [[1,2,3], [4,5,6], [7,8,9]]
        """
        
        # Convert input values into simple rows of data
        rows = [values for values, _ in values_scores]
        
        # Convert to column major format
        #columns = list(zip(*rows))
        
        x_values = array(rows)
        y_values = array([score for _, score in values_scores])
        
        return x_values, y_values

class LinearSVC(MLScorer):
    
    MODEL = LinearSVCModel
