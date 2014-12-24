from ..dependent import Dependent, depends


class Datasource(Dependent):
    """
    Represents a data source for generating features.  Unlike features,
    datasources do not necessarily generate simple scalar values.
    
    :Parameters:
        name : str
            The name of the feature
        process : `func`
            A function that will generate a data value
        dependencies : `list`(`hashable`)
            An ordered list of dependencies that correspond
            to the *args of `process`
    """
    pass

class datasource_processor:
    """
    Decorator for datasource processor functions.  Functions
    decorated with this decorator will be wrapped as a `Datasource` and can
    expect to be called with their dependencies solved as *args by the `solve()`
    function.
    
    :Example:
        >>> from revscores.datasources import datasource_processor
        >>> @datasource_processor()
        ... def foo():
        ...     return 5
        ...
        >>> @datasource_processor(depends_on=[foo])
        ... def bar(foo):
        ...     return foo == 5
        ...
        >>> bar
        <bar>
        >>> bar.dependencies
        [<foo>]
    
    :Parameters:
        depends_on : `list`(`Dependent`)
            An ordered list of dependencies that correspond to the *args of the
            decorated function
    """
    def __init__(self, depends_on=None):
        self.dependencies = depends_on
    
    def __call__(self, process):
        return Datasource(process.__name__, process, self.dependencies)
