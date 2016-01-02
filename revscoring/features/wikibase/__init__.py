"""
This features module provides access to features of the bytes of content in
revisions.

.. autodata:: revscoring.features.wikibase.revision

Supporting classes
++++++++++++++++++

.. autoclass:: revscoring.features.wikibase.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.features.wikibase.Diff
    :members:
    :member-order: bysource

"""
from .revision_oriented import revision
from .features import Revision, Diff
from .util import diff_dicts, DictDiff

__all__ = [diff_dicts, DictDiff, revision, Revision, Diff]
