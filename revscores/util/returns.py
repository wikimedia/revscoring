import logging
from functools import wraps

logger = logging.getLogger("revscores.util.returns")

class returns:
    
    def __init__(self, type):
        self.type = type
    
    def __call__(self, f):
        
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if not __debug__:
                return f(*args, **kwargs)
            else:
                return self.type(f(*args, **kwargs))
            
        
        wrapped_f.return_type = self.type
        
        return wrapped_f
