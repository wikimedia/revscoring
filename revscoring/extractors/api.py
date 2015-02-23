from ..dependent import solve_many
from .extractor import Extractor


class APIExtractor(Extractor):
    
    def __init__(self, session, language=None):
        self.session = session
        self.language = language
        
    def extract(self, rev_id, features, cache=None):
        
        cache = cache or {}
        
        # Prime the cache with pre-configured values
        cache.update({'rev_id': rev_id,
                      'session': self.session,
                      'language': self.language})
        
        return solve_many(features, cache=cache)
