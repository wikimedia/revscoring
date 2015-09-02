"""
This module implements a set of :class:`~revscoring.features.Feature`
for use in scoring revisions.  :class:`~revscoring.features.Feature`
lists can be provided to a :func:`~revscoring.dependencies.functions.solve`, or
more commonly, to a :class:`~revscoring.extractors.extractor.Extractor` to
obtain simple numerical/boolean vaklues that can be used when modeling revision
scores.  The provided features are split conceptually into a set of modules:

* :mod:`revscoring.features.diff`
* :mod:`revscoring.features.page`
* :mod:`revscoring.features.parent_revision`
* :mod:`revscoring.features.previous_user_revision`
* :mod:`revscoring.features.revision`
* :mod:`revscoring.features.user`

diff
++++
.. automodule:: revscoring.features.diff
    :members:

page
++++
.. automodule:: revscoring.features.page
    :members:

parent_revision
+++++++++++++++
.. automodule:: revscoring.features.parent_revision
    :members:

previous_user_revision
++++++++++++++++++++++
.. automodule:: revscoring.features.previous_user_revision
    :members:

revision
++++++++
.. automodule:: revscoring.features.revision
    :members:

user
++++
.. automodule:: revscoring.features.user
    :members:

modifiers
+++++++++
.. automodule:: revscoring.features.modifiers

feature
+++++++
.. automodule:: revscoring.features.feature
"""

from .feature import Feature

__all__ = [Feature]
