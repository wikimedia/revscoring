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
        return sub(self, subband)
    
    def __truediv__(self, divisor):
        return div(self, divisor)
    
    def __mul__(self, multiplier):
        return mul(self, multiplier)
    
    def validate(self, value):
        if isinstance(value, self.returns):
            return value
        else:
            raise ValueError("Expected {0}, but got {1} instead." \
                             .format(self.returns, type(value)))


class Modifier(Feature): pass


class BinaryOperator(Modifier):
    
    CHAR = "?"
    
    def __init__(self, feature, operand, returns=None):
        if isinstance(operand, Feature):
            self.operand_value = None
            operand_name = operand.name
            operand_type = operand.returns
            depends_on = [feature, operand]
        else:
            self.operand_value = operand
            operand_name = str(operand)
            operand_type = type(operand)
            depends_on = [feature]
        
        name = "{0} {1} {2}".format(feature.name, self.CHAR, operand_name)
        if returns is None:
            returns = type(self.operate(feature.returns(), operand_type()))
        super().__init__(name, self._process, returns=returns,
                         depends_on=depends_on)
        
    def _process(self, feature_value, operand_value=None):
        
        operand_value = operand_value if operand_value is not None \
                        else self.operand_value
        
        return self.operate(feature_value, operand_value)
        
    def operate(self, left, right): raise NotImplementedError()

class add(BinaryOperator):
    
    CHAR = "+"
    
    def operate(self, left, right): return left + right

class sub(BinaryOperator):
    
    CHAR = "-"
    
    def operate(self, left, right): return left - right

class mul(BinaryOperator):
    
    CHAR = "*"
    
    def operate(self, left, right): return left * right

class div(BinaryOperator):
    
    CHAR = "/"
    def __init__(self, feature, divisor):
        # All division returns a float, so we are hardcoding it. 
        super().__init__(feature, divisor, returns=float)
    
    def operate(self, left, right): return left / right
        

class log(Modifier):
    
    def __init__(self, feature):
        super().__init__("log({0})".format(feature.name), self._process,
                         returns=float, depends_on=[feature])
    
    def _process(self, feature_value): return math_log(feature_value)

'''
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
