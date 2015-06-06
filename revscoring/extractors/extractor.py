"""
.. autoclass:: revscoring.extractors.extractor.Extractor
"""

import yamlconf

from ..dependencies import Context


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
