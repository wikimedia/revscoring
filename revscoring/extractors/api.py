from mw import api

import yamlconf

from ..dependent import solve_many
from .extractor import Extractor


class APIExtractor(Extractor):

    def __init__(self, session, language=None):
        self.session = session
        self.language = language

    def extract(self, rev_id, features, insert=None):
        # Prime the cache with pre-configured values
        cache = {'rev_id': rev_id,
                 'session': self.session}

        # If language is available, load utilities into the cache
        if self.language is not None:
            cache.update(self.language.cache())

        # Insert values into cache
        cache.update(insert or {})

        return solve_many(features, cache=cache)

    @classmethod
    def from_config(cls, config, section_key="extractors"):
        section = config[section_key]
        session = api.Session(section['api_url'],
                              user_agent=section['user_agent'])

        language = Language.from_config(config)

        return cls(session, language)
