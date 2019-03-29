"""
This features module provides access to features of the bytes of content in
revisions.

.. autodata:: revscoring.features.temporal.revision

Supporting classes
++++++++++++++++++

.. autoclass:: revscoring.features.temporal.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.features.temporal.ParentRevision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.features.temporal.LastUserRevision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.features.temporal.PageCreation
    :members:
    :member-order: bysource

.. autoclass:: revscoring.features.temporal.Page
    :members:
    :member-order: bysource

.. autoclass:: revscoring.features.temporal.User
    :members:
    :member-order: bysource

"""
from .revision_oriented import (LastUserRevision, Page, PageCreation,
                                ParentRevision, Revision, User, revision)

__all__ = [revision, Revision, ParentRevision, LastUserRevision, PageCreation,
           Page, User]
