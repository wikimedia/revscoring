"""
This features module provides access to features of the bytes of content in
revisions.

.. autodata:: revscoring.features.bytes.revision

.. autodata:: revscoring.features.bytes.session

Supporting classes
++++++++++++++++++

.. autoclass:: revscoring.features.bytes.Revision
    :members:

.. autoclass:: revscoring.features.bytes.Session
    :members:

"""
from .revision_oriented import Revision, revision
from .session_oriented import Session, session

__all__ = [revision, Revision, session, Session]
