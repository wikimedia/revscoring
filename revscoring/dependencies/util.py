
class or_none:
    """
    Constructs a callable that will return None if the input is None, but will
    otherwise run a function on incoming data.

    :Parameters:
        func : `function`
            A function to run on non-None inputs
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, val):
        if val is None:
            return None
        else:
            return self.func(val)
