"""
This features module provides access to features of the bytes of content in
revisions.

.. autodata:: revscoring.features.bytes.revision

Supporting classes
++++++++++++++++++

.. autoclass:: revscoring.features.bytes.Revision
    :members:

"""
from .revision_oriented import revision, Revision

__all__ = [revision, Revision]
