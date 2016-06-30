"""
.. autoclass:: revscoring.Extractor

.. autoclass:: revscoring.extractors.OfflineExtractor
"""

import logging

import yamlconf

from ..datasources import revision_oriented
from ..dependencies import Context

logger = logging.getLogger(__name__)


class Extractor(Context):
    """
    Implements a context for extracting dependents for a revision or a set of
    revisions.
    """

    def extract(self, rev_ids, dependents, context=None, caches=None,
                cache=None, profile=None):
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config, name, section_key="extractors"):
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        elif 'class' in section:
            Class = yamlconf.import_module(section['class'])
            return Class.from_config(config, name)


class OfflineExtractor(Extractor):
    """
    Implements a context for extracting features for a revision or a set of
    revisions that is 100% offline and will fetch no data.
    """
    def __init__(self):
        super().__init__()
        logger.warning("Loading OfflineExtractor.  You probably want an " +
                       "APIExtractor unless this is the test server.")

    def extract(self, rev_ids, dependents, context=None, caches=None,
                cache=None, profile=None):
        caches = caches or {}
        if hasattr(rev_ids, "__iter__"):
            return self._extract_many(rev_ids, dependents, context=context,
                                      caches=caches, cache=cache,
                                      profile=profile)
        else:
            rev_id = rev_ids
            cache = cache or caches
            return self._extract(rev_id, dependents, context=context,
                                 cache=cache, profile=profile)

    def _extract(self, rev_id, dependents, context=None, cache=None,
                 profile=None):
        solve_cache = cache if cache is not None else {}
        solve_cache[revision_oriented.revision.id] = rev_id
        return self.solve(dependents, context=context, cache=solve_cache,
                          profile=profile)

    def _extract_many(self, rev_ids, features, context=None, caches=None,
                      cache=None, profile=None):
        for rev_id in rev_ids:
            yield None, self._extract(rev_id, features, context=context,
                                      cache=caches.get(rev_id, cache),
                                      profile=profile)

    @classmethod
    def from_config(cls, config, name, section_key="extractors"):
        return cls()
