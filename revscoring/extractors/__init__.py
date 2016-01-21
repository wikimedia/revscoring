"""
This module contains a collection of utilities for extracting
:class:`~revscoring.Feature` and
:class:`~revscoring.Datasource` for a revision.

api
+++
.. automodule:: revscoring.extractors.api

extractor
+++++++++
.. automodule:: revscoring.extractors.extractor

"""
from .extractor import Extractor, OfflineExtractor

__all__ = [Extractor, OfflineExtractor]
