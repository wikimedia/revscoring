"""
This features module provides access to features of the bytes of content in
revisions.

.. autodata:: revscoring.features.wikitext.revision

Supporting classes
++++++++++++++++++

.. autoclass:: revscoring.features.wikitext.Revision
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: revscoring.features.wikitext.Diff
    :members:
    :inherited-members:
    :member-order: bysource

"""
from .revision_oriented import revision
from .features import Revision, Diff

__all__ = [revision, Revision, Diff]
