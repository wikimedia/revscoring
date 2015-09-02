"""
This module contains a collection of utilities for extracting
:class:`~revscoring.features.feature.Feature` and
:class:`~revscoring.datasources.datasource.Datasource` for a revision.

api
+++
.. automodule:: revscoring.extractors.api

extractor
+++++++++
.. automodule:: revscoring.extractors.extractor

"""
from .extractor import Extractor
from .api import APIExtractor

__all__ = [Extractor, APIExtractor]
