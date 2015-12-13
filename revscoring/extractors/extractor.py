"""
.. autoclass:: revscoring.Extractor

.. autoclass:: revscoring.extractors.OfflineExtractor
"""

import logging

import yamlconf

from ..datasources import revision
from ..dependencies import Context

logger = logging.getLogger(__name__)


class Extractor(Context):
    """
    Implements a context for extracting features for a revision or a set of
    revisions.
    """

    def extract(self, rev_id, features, context=None, cache=None):
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config, name, section_key="extractors"):
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        elif 'class' in section:
            Class = yamlconf.import_module(section['class'])
            return Class.from_config(config, name)


class OfflineExtractor(Context):
    """
    Implements a context for extracting features for a revision or a set of
    revisions that is 100% offline and will fetch no data.
    """
    def __init__(self):
        super().__init__()
        logger.warning("Loading OfflineExtractor.  You probably want an " +
                       "APIExtractor unless this is the test server.")

    def extract(self, rev_id, features, context=None, cache=None):
        cache = cache or {}
        cache[revision.id] = rev_id
        return self.solve(features, cache=cache)

    @classmethod
    def from_config(cls, config, name, section_key="extractors"):
        cls()
