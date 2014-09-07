
from .dependencies import solve


class rev_id: pass
class session: pass

class Extractor:
    
    def __init__(self, session):
        self.session = session
        
    def extract(self, rev_id, features):
        
        cache = {
            rev_id: rev_id,
            session: self.session,
        }
        
        for feature in features:
            
        
    def solve(self, Dependent, cache=None):
        
        if cache == None:
            cache = {}
        
        if Dependent in cache:
            return cache[Dependent]
        else:
            args = [self.solve(sub_dep, cache)
                    for sub_dep in dependent.dependencies]
            
            cache[Dependent] = Dependent(*args)
            return cache[Dependent]
