"""
This module implements a set of
:class:`~revscoring.Datasource`
processors that represent the input data for extracting
:class:`~revscoring.Feature` values.  Just like
:class:`~revscoring.Feature` and other
:class:'~revscoring.Dependent' processors,
:class:`~revscoring.Datasource` processors are tended to
be :func:`~revscoring.dependencies.solve`'d as dependencies. The
provided datasources are split conceptually into a set of modules.  Currently,
there is one module: :mod:`~revscoring.datasources.revision_oriented`.

Meta-datasources
++++++++++++++++
Meta-Features are classes that extend :class:`~revscoring.Datasource` and
implement common operations on :class:`~revscoring.Datasource` like
:class:`~revscoring.datasources.meta.filters.filter` and
:class:`~revscoring.datasources.meta.mappers.map`.
See :mod:`revscoring.datasources.meta` for the full list.

Base classes
++++++++++++
.. automodule:: revscoring.datasources.datasource




"""
from .datasource import Datasource

__all__ = [Datasource]
