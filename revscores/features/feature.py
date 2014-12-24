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
    
    def __repr__(self):
        return "{0}({1}, process={2}, returns={3}, depends_on={4})" \
               .format(self.__class__.__name__,
                       self.name,
                       repr(self.process),
                       repr(self.returns),
                       [str(d) for d in self.depends_on])
    
    def validate(self, value):
        if isinstance(value, self.returns):
            return value
        else:
            raise ValueError("Expected {0}, but got {1} instead." \
                             .format(self.return_type, type(value)))

''' Breaks pickling
class feature_processor:
    """
    Decorator for feature processor functions.  Functions
    decorated with this decorator will be wrapped as a `Feature` and can expect
    to be called with their dependencies solved as *args by the `solve()`
    function.
    
    :Example:
        >>> from revscores.feature_extraction.features import feature_processor
        >>> @feature_processor(returns=int)
        ... def foo():
        ...     return 5
        ...
        >>> @feature_processor(returns=bool, depends_on=[foo])
        ... def bar(foo):
        ...     return foo == 5
        ...
        >>> bar
        <bar>
        >>> bar.dependencies
        [<foo>]
    
    :Parameters:
        returns : `list`(`callable`)
            Types that this feature will return.  This is used to validate
            later.
        depends_on : `list`(`hashable`)
            An ordered list of dependencies that correspond to the *args of the
            decorated function
    """
    def __init__(self, returns, depends_on=None):
        self.return_types = returns
        self.dependencies = depends_on
    
    def __call__(self, process):
        return Feature(process.__name__, process, self.return_types,
                       self.dependencies)
'''
