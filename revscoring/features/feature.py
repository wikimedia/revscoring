from math import log as math_log

from ..dependent import Dependent

# Sets up refences to overloaded function names
math_max = max
math_min = min

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

    def __hash__(self):
        return super().__hash__()

    # Binary math
    def __add__(self, summand):
        return add(self, summand)

    def __sub__(self, subband):
        return sub(self, subband)

    def __truediv__(self, divisor):
        return div(self, divisor)

    def __mul__(self, multiplier):
        return mul(self, multiplier)

    # Comparison
    def __lt__(self, other):
        return lt(self, other)

    def __le__(self, other):
        return le(self, other)

    def __eq__(self, other):
        return eq(self, other)

    def __ne__(self, other):
        return ne(self, other)

    def __gt__(self, other):
        return gt(self, other)

    def __ge__(self, other):
        return ge(self, other)

    def validate(self, value):
        if isinstance(value, self.returns):
            return value
        else:
            raise ValueError("Expected {0}, but got {1} instead." \
                             .format(self.returns, type(value)))
    @classmethod
    def or_constant(self, val):
        if isinstance(val, Feature):
            return val
        else:
            return Constant(val)

class Constant(Feature):

    def __init__(self, value):
        self.value = value
        super().__init__(str(value), self._process, type(value), depends_on=[])

    def _process(self):
        return self.value

class Modifier(Feature): pass

class BinaryOperator(Modifier):

    CHAR = "?"

    def __init__(self, left, right, returns=None):
        left = Feature.or_constant(left)
        right = Feature.or_constant(right)

        name = "({0} {1} {2})".format(left.name, self.CHAR, right.name)
        if returns is None:
            returns = type(self.operate(left.returns(), right.returns()))

        super().__init__(name, self.operate, returns=returns,
                         depends_on=[left, right])

    def operate(self, left, right): raise NotImplementedError()


class add(BinaryOperator):

    CHAR = "+"

    def operate(self, left, right): return left + right

class sub(BinaryOperator):

    CHAR = "-"

    def operate(self, left, right): return left - right

class mul(BinaryOperator):

    CHAR = "*"

    def operate(self, left, right):
        return left * right

class div(BinaryOperator):

    CHAR = "/"
    def __init__(self, left, right):
        # Explicitly setting return type to float.
        super().__init__(left, right, returns=float)

    def operate(self, left, right): return left / right


class Comparison(BinaryOperator):

    def __init__(self, left, right):
        # Explicitly setting return type to boolean.
        super().__init__(left, right, returns=bool)

class gt(Comparison):

    CHAR = ">"

    def operate(self, left, right): return left > right

class lt(Comparison):

    CHAR = "<"

    def operate(self, left, right): return left < right

class ge(Comparison):

    CHAR = ">="

    def operate(self, left, right): return left >= right

class le(Comparison):

    CHAR = "<="

    def operate(self, left, right): return left <= right

class eq(Comparison):

    CHAR = "=="

    def operate(self, left, right): return left == right

class ne(Comparison):

    CHAR = "!="

    def operate(self, left, right): return left != right

class max(Modifier):

    def __init__(self, *args):
        dependencies = [Feature.or_constant(arg) for arg in args]
        returns = float # Hardcoded even though max can return strings, it
                        # shouldn't ever do that

        name = "max({0})".format(", ".join(f.name for f in dependencies))
        super().__init__(name, self._process, returns=returns,
                         depends_on=dependencies)

    def _process(self, *feature_values): return float(math_max(*feature_values))

class min(Modifier):

    def __init__(self, *args):
        dependencies = [Feature.or_constant(arg) for arg in args]
        returns = float # Hardcoded even though max can return strings, it
                        # shouldn't ever do that

        name = "min({0})".format(", ".join(f.name for f in dependencies))
        super().__init__(name, self._process, returns=returns,
                         depends_on=dependencies)

    def _process(self, *feature_values): return float(math_min(*feature_values))


class log(Modifier):

    def __init__(self, feature):
        feature = Feature.or_constant(feature)
        super().__init__("log({0})".format(feature.name), self._process,
                         returns=float, depends_on=[feature])

    def _process(self, feature_value): return math_log(feature_value)
