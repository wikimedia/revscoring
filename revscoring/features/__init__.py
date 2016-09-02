"""
This module implements a set of :class:`revscoring.Feature`
for use in scoring revisions.  :class:`revscoring.Feature`
lists can be provided to a :func:`revscoring.dependencies.solve`, or
more commonly, to a :class:`revscoring.Extractor` to obtain simple
numerical/boolean values that can be used when modeling revision
scores.  The provided features are split conceptually into a set of modules:

Feature collections
+++++++++++++++++++

:mod:`~revscoring.features.revision_oriented`
    Basic features of revisions. E.g. ``revision.user.text_matches(r'.*Bot')``
:mod:`~revscoring.features.bytes`
    Features of the number of bytes of content, byte length of characters,
    etc.
:mod:`~revscoring.features.temporal`
    Features of the time between events of a interest. E.g.
    ``revision.user.last_revision.seconds_since``
:mod:`~revscoring.features.wikibase`
    Features of wikibase items and changes made to them. E.g.
    ``revision.diff.property_changed('P31')``
:mod:`~revscoring.features.wikitext`
    Features of wikitext content and differences between revisions. E.g.
    ``revision.diff.uppercase_words_added``

Functions
+++++++++

.. automodule:: revscoring.features.functions

Meta-features
+++++++++++++
Meta-Features are classes that extend :class:`~revscoring.Feature` and
implement common operations on :class:`~revscoring.Datasource` like
:class:`~revscoring.features.meta.aggregators.sum` and
:class:`~revscoring.features.meta.bools.item_in_set`.  See
:mod:`revscoring.features.meta` for the full list.

Modifiers
+++++++++
Modifiers are functions that can be applied to a :class:`revscoring.Feature`
to modify the value.  E.g. :class:`~revscoring.features.modifiers.log`,
:class:`~revscoring.features.modifiers.max` and
:class:`~revscoring.features.modifiers.add`.
See :mod:`~revscoring.features.modifiers` for the full list.

Base classes
++++++++++++

.. automodule:: revscoring.features.feature
"""

from .feature import Feature, Modifier, Constant
from .feature_vector import FeatureVector
from .functions import trim, vectorize_values

__all__ = [Feature, Modifier, Constant, FeatureVector, trim, vectorize_values]
