from math import log as math_log

from .features import Feature


class Modifier(Feature):
    
    def __init__(self, feature):
        self.feature = feature
    
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()
    
    def __getattr__(self, attr):
        return getattr(self.feature, attr)
    
    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.feature) + ")"
    
    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.feature) + ")"
    

class log(Modifier):
    
    def __call__(self, *args, **kwargs):
        value = self.feature(*args, **kwargs)
        return math_log(value)
