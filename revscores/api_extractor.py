from .util.dependencies import solve


class APIExtractor:
    
    def __init__(self, session, dictionary=None):
        self.session = session
        self.dictionary = dictionary
        
    def extract(self, rev_id, features):
        
        # Prime the cache with pre-configured values
        cache = {
            'rev_id': rev_id,
            'session': self.session,
            'dictionary': self.dictionary
        }
        
        return [solve(feature, cache) for feature in features]
