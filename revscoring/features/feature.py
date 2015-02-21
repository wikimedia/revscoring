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


class FeatureFunction(Modifier):
    
    FUNC = "?"
    
    def __init__(self, *args, returns=None):
        depends_on = []
        self.names = []
        self.values = []
        for arg in args:
            if isinstance(arg, Feature):
                depends_on.append(arg)
        if isinstance(left, Feature):
            self.left_value = None
            left_name = operand.name
            left_returns = operand.returns
            depends_on.append(left)
        else:
            self.left_value = left
            left_name = str(operand)
            left_returns = type(operand)
        
        if isinstance(right, Feature):
            self.right_value = None
            right_name = operand.name
            right_returns = operand.returns
            depends_on.append(right)
        else:
            self.right_value = right
            right_name = str(operand)
            right_returns = type(operand)
        
        name = "{0} {1} {2}".format(left_name, self.CHAR, operand_name)
        if returns is None:
            returns = type(self.operate(feature.returns(), operand_type()))
        super().__init__(name, self._process, returns=returns,
                         depends_on=depends_on)
    
    def _format_name(self, left_name, right_name):
        name = "{0}({1}, {2})".format(self.FUNC, left_name, right_name)
    
    def _process(self, left_value=None, right_value=None):
        
        left_value = left_value if left_value is not None \
                     else self.left_value
        
        right_value = right_value if right_value is not None \
                      else self.right_value
        
        return self.operate(left_value, right_value)
        
    def operate(self, left, right): raise NotImplementedError()

class BinaryOperator(BinaryFunction):
    
    CHAR = "?"
    
    def _format_name(self, left_name, right_name):
        name = "{0} {1} {2}".format(left_name, self.CHAR, right_name)
    

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
        # Explicitly setting return type to float.
        super().__init__(feature, divisor, returns=float)
    
    def operate(self, left, right): return left / right

class max(Modifier):
    
    def __init__(self, left, right):
        depends_on = []
        if isinstance(left, Feature):
            depends_on.append(left)
            left_returns = left.returns
            left_name    = left.name
        else:
            left_returns = type(left)
            
        super().__init__("log({0})".format(feature.name), self._process,
                         returns=float, depends_on=[feature])
    
    def _process(self, feature_value): return math_log(feature_value)
    
class log(Modifier):
    
    def __init__(self, feature):
        super().__init__("log({0})".format(feature.name), self._process,
                         returns=float, depends_on=[feature])
    
    def _process(self, feature_value): return math_log(feature_value)
