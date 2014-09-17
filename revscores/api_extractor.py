from .util.dependencies import solve


class APIExtractor:
    
    def __init__(self, session, lang=None):
        self.session = session
        self.lang = lang
        
    def extract(self, rev_id, features, cache=None):
        
        cache = cache or {}
        
        # Prime the cache with pre-configured values
        cache.update({'rev_id': rev_id,
                      'session': self.session,
                      'lang': self.lang})
        
        return [solve(feature, cache) for feature in features]
