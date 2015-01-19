from math import log as math_log

from ..dependent import Dependent


class Feature(Dependent):
    """
    Represents a predictive feature.  This class wraps a processor function
    and some metadata about it.
    
    :Parameters:
        name : str
            The name of the feature
        process : `func`
            A function that will generate a feature value
        return_type : `type`
            A type to compare the return of this function to.
        dependencies : `list`(`hashable`)
                An ordered list of dependencies that correspond
                to the *args of `process`
    """
    def __init__(self, name, process, returns, depends_on=None):
        super().__init__(name, process, depends_on)
        self.returns = returns
        
    
    def __call__(self, *args, **kwargs):
        value = super().__call__(*args, **kwargs)
        
        if __debug__: return self.validate(value)
        else: return value
    
    def __add__(self, summand):
        return add(self, summand)
    
    def __sub__(self, subband):
        return add(self, subband)
    
    def validate(self, value):
        if isinstance(value, self.returns):
            return value
        else:
            raise ValueError("Expected {0}, but got {1} instead." \
                             .format(self.returns, type(value)))


class Modifier(Feature): pass


class log(Modifier):
    
    def __init__(self, feature):
        super().__init__("log({0})".format(feature.name), self._process,
                         returns=float, depends_on=[feature])
    
    def _process(self, feature_value): return math_log(feature_value)
    

class add(Modifier):
    
    def __init__(self, feature, summand):
        super().__init__("{0} + {1}".format(feature.name, repr(summand)),
                         self._process,
                         returns=type(feature.returns() + summand),
                         depends_on=[feature])
        self.summand = summand
    
    def _process(self, feature_value): return feature_value + self.summand

class sub(Modifier):
    
    def __init__(self, feature, subband):
        super().__init__("{0} - {1}".format(feature.name, repr(subband)),
                         self._process,
                         returns=type(feature.returns() - subband),
                         depends_on=[feature])
        self.subband = subband
    
    def _process(self, feature_value): return feature_value - self.subband

'''
def log(feature):
    def process(feature_value):
        return math_log(feature_value)
    
    return Feature(, process,
                   returns=float,
                   depends_on=[feature])


def add(feature, summand):
    def process(feature_value):
        return feature_value + summand
    
    returns = type(feature.returns() + type(summand)())
    
    return Feature("{0} + {1}".format(feature.name, repr(summand)), process,
                  returns=returns,
                  depends_on=[feature])


def sub(feature, subband):
    def process(feature_value):
        return feature_value - subband
    
    returns = type(feature.returns() - type(subband)())
    
    return Feature("{0} + {1}".format(feature.name, repr(subband)), process,
                  returns=returns,
                  depends_on=[feature])
'''
